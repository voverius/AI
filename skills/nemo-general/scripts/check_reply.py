"""Validate a final reply without writing files or changing the draft."""

import json
import re
import sys


def mask_code(text):
    lines = []
    fence = None
    for line in text.splitlines():
        if fence:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*', line):
                fence = None
        else:
            opening = re.match(r' {0,3}(`{3,}|~{3,})[^\n]*$', line)
            if opening:
                fence = opening[1]
                lines.append('code')
            else:
                lines.append(line)
    return re.sub(r'(`+).*?\1', 'code', '\n'.join(lines), flags=re.DOTALL)


def validate(payload):
    if (not isinstance(payload, dict) or not isinstance(payload.get('text'), str)
            or not payload['text'].strip()
            or payload.get('mode', 'reply') not in
            ('reply', 'fact', 'progress', 'report', 'comparison', 'review', 'detail')):
        return ['Provide nonempty text and a supported reply mode as JSON.']
    text = payload['text'].strip()
    mode = payload.get('mode', 'reply')
    ordinary = mode in ('reply', 'fact', 'progress', 'report')
    prose = mask_code(text)
    prose = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', prose)
    unquoted = re.sub(r'(?m)^[ \t]*>[^\n]*(?:\n|$)', '', prose)
    prose = re.sub(r'\b(?:Dr|Mr|Mrs|Ms|Prof|e\.g|i\.e|vs)\.',
                   lambda match: match[0].replace('.', ''), prose)
    prose = re.sub(r'^[ \t]*(?:[-*+] |\d+[.)] )', '\n', prose, flags=re.MULTILINE)
    prose = re.sub(r'''([.!?])[*_"'\u2019\u201d)\]]+(?=\s|$)''', r'\1', prose)
    table_pattern = (
        r'(?m)^\|[^\n]+\|[ \t]*\n\|(?:[ \t]*:?-{3,}:?[ \t]*\|){2,}[ \t]*\n'
        r'(?:\|[^\n]+\|[ \t]*(?:\n|$))+')
    tables = list(re.finditer(table_pattern, prose))
    errors = []
    if mode == 'review':
        if not re.fullmatch(r'\*\*[^?\n]+\?\*\*', text.splitlines()[0]):
            errors.append('Start a review with one focused question in bold.')
        question_prose = re.sub(r'''"[^"\n]*"|\u201c[^\u201d\n]*\u201d|(?<!\w)'[^'\n]*'(?!\w)''',
                                '', unquoted)
        if question_prose.count('?') != 1:
            errors.append('Ask one review question, excluding quoted source questions.')
        if not re.search(r'(?m)^\*\*Suggestion(?::\*\*|\*\*:)\s+\S', unquoted):
            errors.append('Label the review recommendation with **Suggestion:**.')
    if mode == 'comparison':
        count = payload.get('count')
        if type(count) is not int or count < 1:
            errors.append('Comparison mode requires a positive integer count from the request.')
        else:
            alternatives = re.split(r'(?m)^[ \t]*---[ \t]*$', prose)
            if len(alternatives) != count or any(not part.strip() for part in alternatives):
                errors.append('Provide exactly the requested alternatives separated by --- lines.')
    for table in tables:
        rows = table[0].strip().splitlines()
        widths = [len(re.split(r'(?<!\\)\|', row.strip()[1:-1])) for row in rows]
        if len(set(widths)) != 1:
            errors.append('Use matching columns in table headers, separators and rows.')
    sentence_prose = re.sub(table_pattern, '', prose)
    sentence_prose = re.sub(r'\n[ \t]+', ' ', sentence_prose)
    sentence_prose = re.sub(r'(?<!\n)\n(?!\n)', ' ', sentence_prose)
    sentences = [part for part in re.split(r'(?<=[.!?])\s+|\n+', sentence_prose.strip()) if part]
    report = mode == 'report' and re.fullmatch(
        r'[^\n]+\n[ \t]*\n(?:[-*+] [^\n]+(?:\n[ \t]+[^\n]+)*(?:\n|$)){1,3}', text)
    units = ([line for line in re.split(r'\n+', re.sub(r'\n[ \t]+', ' ', prose).strip())
              if line] if report else sentences)
    if mode == 'report' and not report:
        errors.append('Use the completion-report layout: plain opener, blank line and labeled bullets.')
    if report:
        opener = prose.splitlines()[0].strip()
        if (re.search(r'\*\*|__', text.splitlines()[0])
                or len(re.split(r'(?<=[.!?])\s+', opener)) != 1
                or not re.search(r'[.!?]$', opener)):
            errors.append('Use one plain, unbolded opening sentence for a completion report.')
        for line in re.findall(r'^[-*+] [^\n]+(?:\n[ \t]+[^\n]+)*', text, re.MULTILINE):
            label = re.match(r'[-*+] \*\*[^*\s:]+(?::\*\*|\*\*:) ', line)
            if not label:
                errors.append('Start each completion-report bullet with one bold word and a colon.')
            elif re.search(r'\*\*|__', line[label.end():]):
                errors.append('Keep completion-report text after the label unbolded.')
    if ordinary and re.search(r'^\s*(?:```|~~~)', text, re.MULTILINE):
        errors.append('Ordinary replies must not include unrequested code blocks.')
    if ordinary and len(units) > (4 if report else 3):
        errors.append('Use at most three sentences or items, plus the completion-report opener.')
    if ordinary and any(len(unit.split()) > 35 for unit in units):
        errors.append('Use at most 35 words per sentence. Select essential facts instead of run-ons.')
    if mode == 'fact' and (len(sentences) != 1 or tables or report
                           or re.match(r'(?:[-*+] |\d+[.)] )', text)):
        errors.append('Answer a simple factual question in one direct sentence.')
    if mode == 'progress':
        if (re.search(r'\n[ \t]*\n', text) or tables or report
                or re.search(r'(?m)^(?:[-*+] |\d+[.)] |#{1,6} )', text)):
            errors.append('Use one compact paragraph for a routine progress update.')
        if re.match(r"I(?:\s|['\u2019])", text):
            errors.append('Start routine progress with the action or finding, not its narrator.')
    if any(character in prose for character in (';', '\u2014', '\u2013')):
        errors.append('Prose must not contain semicolons, em dashes or en dashes.')
    return errors


if __name__ == '__main__':
    try:
        if len(sys.argv) > 2:
            raise ValueError('Expected one JSON argument or JSON on stdin.')
        payload = json.loads(sys.argv[1]) if len(sys.argv) == 2 else json.load(sys.stdin)
        errors = validate(payload)
    except (ValueError, UnicodeError):
        errors = ['Input must be valid JSON.']
    result = {'ok': not errors, 'errors': errors}
    if not errors:
        result['text'] = payload['text']
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(1 if errors else 0)
