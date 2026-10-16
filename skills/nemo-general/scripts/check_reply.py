"""Validate a final reply without writing files or changing the draft."""

import json
import re
import sys


def validate(payload):
    if (not isinstance(payload, dict) or not isinstance(payload.get('text'), str)
            or not payload['text'].strip()
            or payload.get('mode', 'reply') not in ('reply', 'detail')):
        return ['Provide nonempty text and mode reply or detail as a JSON object.']
    text = payload['text']
    mode = payload.get('mode', 'reply')
    prose = re.sub(r'(`+).*?\1', 'code', text, flags=re.DOTALL)
    prose = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', prose)
    prose = re.sub(r'\b(?:Dr|Mr|Mrs|Ms|Prof|e\.g|i\.e|vs)\.',
                   lambda match: match[0].replace('.', ''), prose)
    prose = re.sub(r'^\s*(?:[-*+] |\d+[.)] )', '', prose, flags=re.MULTILINE)
    prose = re.sub(r'''([.!?])[*_"'\u2019\u201d)\]]+(?=\s|$)''', r'\1', prose)
    sentences = re.split(r'(?<=[.!?])\s+|\n+', prose.strip())
    errors = []
    if mode == 'reply' and re.search(r'\n\s*\n', text.strip()):
        errors.append('Use one paragraph, or a compact list when it is clearer.')
    if mode == 'reply' and re.search(r'^\s*(?:```|~~~)', text, re.MULTILINE):
        errors.append('Ordinary replies must not include unrequested code blocks.')
    if mode == 'reply' and len(sentences) > 3:
        errors.append('Use at most three sentences, including evidence and limitations.')
    if mode == 'reply' and any(len(sentence.split()) > 35 for sentence in sentences):
        errors.append('Use at most 35 words per sentence. Select essential facts instead of run-ons.')
    if any(character in prose for character in (';', '\u2014', '\u2013')):
        errors.append('Prose must not contain semicolons, em dashes or en dashes.')
    return errors


if __name__ == '__main__':
    try:
        payload = json.load(sys.stdin)
        errors = validate(payload)
    except (ValueError, UnicodeError):
        errors = ['Input must be valid JSON.']
    result = {'ok': not errors, 'errors': errors}
    if not errors:
        result['text'] = payload['text']
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(1 if errors else 0)
