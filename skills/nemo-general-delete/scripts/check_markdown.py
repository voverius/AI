"""Check saved Markdown spacing without rewriting or printing document contents."""
import argparse
import json
from pathlib import Path
import re
import sys


HEADING = re.compile(r' {0,3}#{1,6}(?:[ \t]|$)')
FENCE = re.compile(r' {0,3}(`{3,}|~{3,})(.*)$')
ITEM = re.compile(r' {0,3}(?:[-+*]|[0-9]{1,9}[.)])(?:[ \t]+|$)')
BREAK = re.compile(r' {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})')
DEFINITION = re.compile(
    r' {0,3}\[[^\]]+\]:[ \t]*(?:<[^<>]*>|[^ \t<>]+)'
    r'''(?:[ \t]+(?:"[^"]*"|'[^']*'|\([^)]*\)))?[ \t]*''')
SETEXT = re.compile(r' {0,3}=+[ \t]*')


def check(text, fragment=False, frontmatter=False):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    if lines[-1] == '':
        lines.pop()
    errors = []

    def error(line, rule):
        errors.append({'line': line, 'rule': rule})

    frontmatter = bool((not fragment or frontmatter) and lines and lines[0] == '---' and
                       any(line in ('---', '...') for line in lines[1:]))
    if not fragment:
        if not frontmatter and (not text.startswith('\n') or text.startswith('\n\n')):
            error(1, 'file_boundary')
        if not text.endswith('\n\n') or text.endswith('\n\n\n'):
            error(max(1, len(lines)), 'file_boundary')

    fence = None
    list_indent = None
    kinds = []
    for index, line in enumerate(lines):
        kind = 'text' if line.strip(' \t') else 'blank'
        if frontmatter:
            kind = 'syntax'
            if index and line in ('---', '...'):
                frontmatter = False
        elif fence:
            kind = 'syntax'
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) +
                            '{' + str(fence[1]) + r',}[ \t]*', line):
                fence = None
        elif (match := FENCE.fullmatch(line)) and not (
                match[1][0] == '`' and '`' in match[2]):
            fence = (match[1][0], len(match[1]))
            kind = 'syntax'
        elif HEADING.match(line):
            kind = 'heading'
            previous = index - 1
            while previous >= 0 and kinds[previous] == 'blank':
                previous -= 1
            if previous >= 0 and kinds[previous] in ('text', 'item', 'continuation') and (
                    index - previous != 2):
                error(index + 1, 'heading_spacing')
            if index + 1 < len(lines) and not lines[index + 1].strip(' \t'):
                error(index + 1, 'heading_spacing')
        elif (BREAK.fullmatch(line) or DEFINITION.fullmatch(line) or
              (SETEXT.fullmatch(line) and index and kinds[-1] == 'text')):
            kind = 'syntax'
        elif ITEM.match(line):
            kind = 'item'
            list_indent = len(line) - len(line.lstrip(' '))
            previous = index - 1
            while previous >= 0 and kinds[previous] == 'blank':
                previous -= 1
            if previous < index - 1 and previous >= 0 and kinds[previous] in (
                    'item', 'continuation'):
                error(index + 1, 'list_spacing')
        elif (line.strip(' \t') and list_indent is not None and index and
              kinds[-1] in ('item', 'continuation') and
              len(line) - len(line.lstrip(' ')) > list_indent):
            kind = 'continuation'
        elif line.startswith(('    ', '\t')):
            kind = 'syntax'
        kinds.append(kind)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', type=Path)
    parser.add_argument('--fragment', action='store_true',
                        help='Check an authorized excerpt without file-boundary rules')
    parser.add_argument('--frontmatter', action='store_true',
                        help="The fragment starts at the file's frontmatter, not a thematic break")
    args = parser.parse_args()
    try:
        inputs = [(str(path), path.read_text(encoding='utf-8')) for path in args.paths] if args.paths else [
            ('stdin', sys.stdin.read())]
    except (OSError, UnicodeError):
        print(json.dumps({'ok': False, 'error': 'read_error'}))
        return 2
    results = [{'path': name, 'errors': check(text, args.fragment, args.frontmatter)}
               for name, text in inputs]
    ok = not any(result['errors'] for result in results)
    print(json.dumps({'ok': ok, 'results': results}))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
