#!/usr/bin/env python3
"""Check standard project navigation without modifying files."""
import re
import string
import sys
from collections import deque
from pathlib import Path
from urllib.parse import unquote, urlsplit


def without_fenced_code(text):
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        if fence:
            character, length = fence
            if re.fullmatch(r' {0,3}' + re.escape(character) +
                            '{' + str(length) + r',}[ \t]*', line.rstrip('\r\n')):
                fence = None
            continue
        opening = re.match(r'^ {0,3}(`{3,}|~{3,})([^\r\n]*)', line)
        if opening and not (opening[1][0] == '`' and '`' in opening[2]):
            fence = opening[1][0], len(opening[1])
        else:
            lines.append(line)
    return ''.join(lines)


def destination_at(text, start):
    angled = text[start:start + 1] == '<'
    position = start + int(angled)
    destination = []
    depth = 0
    while position < len(text):
        character = text[position]
        if (character == '\\' and position + 1 < len(text)
                and text[position + 1] in string.punctuation):
            destination.append(text[position + 1])
            position += 2
            continue
        if angled:
            if character == '>':
                return ''.join(destination)
            if character in '\r\n':
                return None
        else:
            if character.isspace() or (character == ')' and depth == 0):
                break
            if character == '(':
                depth += 1
            elif character == ')':
                depth -= 1
        destination.append(character)
        position += 1
    if angled or depth:
        return None
    return ''.join(destination) or None


def unescaped_matches(pattern, text):
    for match in re.finditer(pattern, text):
        position = match.start()
        slashes = 0
        while position and text[position - 1] == '\\':
            slashes += 1
            position -= 1
        if slashes % 2 == 0:
            yield match


def link_paths(text):
    text = without_fenced_code(text)
    text = re.sub(r'`[^`\n]*`', '', text)
    definitions = {}
    for match in re.finditer(r'(?m)^ {0,3}\[([^\]\n]+)\]:\s*', text):
        target = destination_at(text, match.end())
        if target is not None:
            definitions.setdefault(' '.join(match[1].split()).casefold(), target)
    paths = []
    for match in unescaped_matches(r'\[[^\]]*\]\(\s*', text):
        target = destination_at(text, match.end())
        if target:
            paths.append(target)
    labels = [match[2] or match[1] for match in unescaped_matches(
        r'\[([^\]]+)\]\[([^\]]*)\]', text
    )]
    labels.extend(match[1] for match in unescaped_matches(r'\[([^\]]+)\](?![:(\[])', text))
    for label in labels:
        target = definitions.get(' '.join(label.split()).casefold())
        if target:
            paths.append(target)
    return paths


def check(root):
    errors = []
    for name in ('AGENTS.md', 'README.md', 'docs/index.md'):
        if not (root / name).is_file():
            errors.append(f'Missing {name}')
    if not (root / 'inbox').is_dir():
        errors.append('Missing inbox/')
    targets = {}
    pages = [root / 'README.md']
    for role in ('docs', 'outputs', 'handovers'):
        pages.extend(sorted((root / role).rglob('*.md')))
    for page in pages:
        if not page.is_file():
            continue
        found = set()
        for value in link_paths(page.read_text()):
            value = value.strip().strip('<>')
            if not value or value.startswith('#') or urlsplit(value).scheme:
                continue
            target = (page.parent / Path(unquote(value.split('#')[0])).expanduser()).resolve()
            found.add(target)
            if not target.exists():
                errors.append(f'{page.relative_to(root)}: missing link target {value}')
        targets[page.resolve()] = found
    readme_targets = targets.get((root / 'README.md').resolve(), set())
    if (root / 'docs/index.md').resolve() not in readme_targets:
        errors.append('README must link docs/index.md')
    for name in ('inbox', 'sources', 'outputs', 'handovers'):
        folder = root / name
        if folder.is_dir() and (name == 'inbox' or any(folder.iterdir())):
            if folder.resolve() not in readme_targets:
                errors.append(f'README must link populated role {name}/')
    allowed = {(root / name).resolve() for name in ('AGENTS.md', 'docs/index.md')}
    for target in readme_targets:
        if target.is_file() and target not in allowed and root in target.parents:
            errors.append(f'README lists a project file: {target.relative_to(root)}')
    queue = deque([(root / 'docs/index.md').resolve()])
    reached = set()
    while queue:
        page = queue.popleft()
        if page in reached:
            continue
        reached.add(page)
        queue.extend(targets.get(page, set()))
    for page in (root / 'docs').rglob('*.md'):
        if page.resolve() not in reached:
            errors.append(f'Unreachable subject: {page.relative_to(root)}')
    return errors


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: check_navigation.py PROJECT_ROOT')
    selected = Path(sys.argv[1]).expanduser().absolute()
    root = selected.resolve()
    if not root.is_dir():
        raise SystemExit('Project root must be an existing directory')
    errors = check(root)
    print('\n'.join(errors) if errors else 'Navigation checks passed')
    raise SystemExit(bool(errors))
