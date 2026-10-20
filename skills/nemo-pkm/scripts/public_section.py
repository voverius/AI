"""Expose a library file's public prefix without returning its protected suffix."""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile


class SectionError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise SectionError('invalid_arguments')


def heading_identity(line):
    line = line.removesuffix(b'\n').removesuffix(b'\r')
    match = re.fullmatch(rb' {0,3}(#{1,6})(?:[ \t]+(.*))?', line)
    if not match:
        return None
    title = (match.group(2) or b'').rstrip(b' \t')
    title = re.sub(rb'(?:^|[ \t]+)#+$', b'', title)
    return match.group(1), title


def public_prefix(stream, heading):
    prefix = bytearray()
    for chunk in stream:
        # Binary iteration splits at LF only. Recognize CR without normalizing bytes.
        for match in re.finditer(rb'[^\r\n]*(?:\r\n|\r|\n|$)', chunk):
            line = match.group()
            if heading_identity(line) == heading:
                return bytes(prefix), True
            prefix.extend(line)
    return bytes(prefix), False


def scoped_path(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise SectionError('outside_root')
    if not path.is_file():
        raise SectionError('io_error')
    return path


def atomic_replace(path, public, suffix):
    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, name = tempfile.mkstemp(dir=path.parent, prefix='.public-section-')
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(public)
            stream.write(suffix)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def run(argv):
    parser = Parser(description=__doc__)
    parser.add_argument('operation', choices=['view', 'replace'])
    parser.add_argument('--root', required=True)
    parser.add_argument('--heading', required=True)
    parser.add_argument('--public-file')
    parser.add_argument('--expected-public-sha256')
    parser.add_argument('file')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve(strict=True)
    if not root.is_dir():
        raise SectionError('invalid_root')
    if '\n' in args.heading or '\r' in args.heading:
        raise SectionError('invalid_heading')
    heading = heading_identity(args.heading.encode('utf-8'))
    if heading is None:
        raise SectionError('invalid_heading')
    path = scoped_path(root, args.file)
    with path.open('rb') as stream:
        public, found = public_prefix(stream, heading)
        if args.operation == 'replace':
            stream.seek(len(public))
            suffix = stream.read()
    public_text = public.decode('utf-8')
    if args.operation == 'replace':
        if args.public_file is None or args.expected_public_sha256 is None:
            raise SectionError('invalid_arguments')
        if not found:
            raise SectionError('boundary_missing')
        if hashlib.sha256(public).hexdigest() != args.expected_public_sha256:
            raise SectionError('stale_public_hash')
        source = scoped_path(root, args.public_file)
        if source.samefile(path):
            raise SectionError('same_file')
        replacement = source.read_bytes()
        if public_prefix(io.BytesIO(replacement), heading)[1]:
            raise SectionError('replacement_boundary')
        replacement.decode('utf-8')
        if replacement and not replacement.endswith((b'\r', b'\n')):
            raise SectionError('replacement_needs_newline')
        if replacement == public:
            return {'status': 'unchanged',
                    'public_sha256': hashlib.sha256(public).hexdigest()}
        atomic_replace(path, replacement, suffix)
        return {'status': 'replaced',
                'public_sha256': hashlib.sha256(replacement).hexdigest()}
    return {'public_text': public_text, 'boundary_found': found,
            'public_sha256': hashlib.sha256(public).hexdigest()}


def main(argv=None):
    try:
        result = run(argv)
    except SectionError as error:
        result = {'status': 'error', 'error': str(error)}
    except UnicodeError:
        result = {'status': 'error', 'error': 'invalid_public_utf8'}
    except (OSError, RuntimeError):
        result = {'status': 'error', 'error': 'io_error'}
    print(json.dumps(result))
    if result.get('status') == 'error':
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
