#!/usr/bin/env python3
"""Check standard project navigation without modifying files."""
import re
import sys
from collections import deque
from pathlib import Path
from urllib.parse import unquote, urlsplit


def check(root):
    errors = []
    for name in ('AGENTS.md', 'README.md', 'docs/index.md'):
        if not (root / name).is_file():
            errors.append(f'Missing {name}')
    if not (root / 'inbox').is_dir():
        errors.append('Missing inbox/')
    targets = {}
    pages = [root / 'README.md', *sorted((root / 'docs').rglob('*.md'))]
    for page in pages:
        if not page.is_file():
            continue
        text = re.sub(r'(?ms)^```.*?^```[^\n]*', '', page.read_text())
        found = set()
        for value in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text):
            value = value.strip().strip('<>')
            if not value or value.startswith('#') or urlsplit(value).scheme:
                continue
            target = (page.parent / unquote(value.split('#')[0])).resolve()
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
    if selected.parent.resolve() != (Path.home() / 'Projects').resolve():
        raise SystemExit('Use ~/Projects/<project>, not the implementation repository')
    root = selected.resolve()
    if not root.is_dir():
        raise SystemExit('Project root must be an existing directory')
    errors = check(root)
    print('\n'.join(errors) if errors else 'Navigation checks passed')
    raise SystemExit(bool(errors))
