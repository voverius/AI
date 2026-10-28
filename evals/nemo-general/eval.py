"""nemo-general eval: run cases in real Claude Code sessions, judge them, report metrics.

python3 eval.py run <label> [case ...]   real sessions, normal hooks and plugins
python3 eval.py judge <label>            hook-free judge scores each case's final reply
python3 eval.py report <label>           per-goal metrics
python3 eval.py selftest
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import re
import statistics
import subprocess
import sys
import threading

W = Path(__file__).resolve().parent
SKILL = Path.home() / '.claude/skills/nemo-general/SKILL.md'
SANDBOX = Path(os.environ.get('EVAL_SANDBOX', W / 'sandbox'))
STOP = threading.Event()
CASES = json.loads((W / 'cases.json').read_text())

OPENERS = r'^(great question|sure[,!.]|certainly|of course|absolutely|let me|i\'d be happy|good question)'
CLOSERS = (r'(let me know|hope this helps|want me to|would you like|feel free|in summary|in short,|'
           r'to summarize|bottom line|happy to help|if you\'d like)')
EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿⭐✅]')


def claude(args, prompt, cwd):
    p = subprocess.run(['claude', '-p', *args, '--', prompt], cwd=cwd, capture_output=True,
                       text=True, timeout=600, stdin=subprocess.DEVNULL)
    return p


def run_turn(prompt, session, skill_text):
    args = ['--output-format', 'stream-json', '--verbose', '--include-hook-events',
            '--tools', 'Read,Skill', '--permission-prompts', 'none']
    if session:
        args += ['--resume', session]
    if os.environ.get('EVAL_SETTINGS'):
        args += ['--settings', os.environ['EVAL_SETTINGS']]
    turn = {'prompt': prompt, 'reply': '', 'hooks': [], 'tool_calls': [], 'usage': None, 'error': None}
    try:
        p = claude(args, prompt, SANDBOX)
    except subprocess.TimeoutExpired:
        turn['error'] = 'timeout'
        return turn
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get('subtype') == 'init':
            turn['output_style'] = e.get('output_style')
        if e.get('subtype') == 'hook_response' and e.get('hook_event') == 'UserPromptSubmit' and \
                'Before sending' in e.get('output', ''):
            turn['reminder'] = True
        if e.get('subtype') == 'hook_response' and e.get('hook_event') == 'SessionStart':
            out = e.get('output', '')
            if 'nemo-general' in out:
                turn['hooks'].append({'name': e['hook_name'], 'current_skill': skill_text in json.loads(out)
                                      ['hookSpecificOutput']['additionalContext']})
        for b in (e.get('message') or {}).get('content') or []:
            if isinstance(b, dict) and b.get('type') == 'tool_use':
                turn['tool_calls'].append({'name': b['name'], 'input': b.get('input')})
        if e.get('type') == 'rate_limit_event':
            info = e.get('rate_limit_info', {})
            (W / 'usage.json').write_text(json.dumps(info, indent=1) + '\n')
            weekly = [v.get('utilization', 0) for k, v in (info.get('unifiedWindows') or {}).items() if isinstance(v, dict) and ('day' in k or 'week' in k)]
            if weekly and max(weekly) >= 0.95:
                STOP.set()
        if e.get('type') == 'result':
            turn['reply'] = e.get('result', '')
            turn['usage'] = {'output_tokens': e['usage']['output_tokens']}
            turn['session'] = e.get('session_id')
            if e.get('is_error'):
                turn['error'] = e.get('terminal_reason') or e.get('subtype')
    if p.returncode and not turn['error']:
        turn['error'] = f'exit {p.returncode}: {p.stderr[-300:]}'
    return turn


def run_case(case, out_dir, skill_text):
    if STOP.is_set():
        return case['id'], ['stopped: weekly usage >= 95%']
    turns, session = [], None
    for prompt in case['turns']:
        t = run_turn(prompt, session, skill_text)
        turns.append(t)
        session = t.get('session')
        if t['error']:
            break
    rec = {'case': case['id'], 'skill_sha256': hashlib.sha256(skill_text.encode()).hexdigest(), 'turns': turns}
    (out_dir / f"{case['id']}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
    return case['id'], [t['error'] for t in turns if t['error']]


def mech(reply):
    text = re.sub(r'```.*?```', '', reply, flags=re.S)
    lines = [l for l in text.splitlines() if l.strip()]
    paras = [p for p in re.split(r'\n\s*\n', text) if p.strip() and not re.match(r'\s*([-*|#>]|\d+\.)', p)]
    return {
        'words': len(reply.split()),
        'questions': len(re.findall(r'\?(\s|$)', text)),
        'emoji': len(EMOJI.findall(reply)),
        'longest_para_words': max((len(p.split()) for p in paras), default=0),
        'opener': bool(lines and re.search(OPENERS, lines[0].strip().lower())),
        'closer': bool(lines and re.search(CLOSERS, ' '.join(lines[-2:]).lower())),
        'item_periods': len(re.findall(r'^\s*(?:[-*]|\d+\.) .*\.\s*$', text, re.M)),
        'three_list': any(len(b) == 3 for b in re.findall(r'((?:^\s*(?:[-*]|\d+\.) .*\n?)+)', text, re.M)
                          for b in [re.findall(r'^\s*(?:[-*]|\d+\.) ', b, re.M)]),
    }


JUDGE = """You grade one assistant reply for a user who wants the information they need at a glance and
hates noise. Grade only the FINAL reply, using the earlier turns as context. Return only JSON.

Case expectation (what an ideal final reply does): {expect}

Conversation:
{conversation}

FINAL REPLY:
<<<
{reply}
>>>

Rules:
- "units": split the final reply into units (each sentence, each list item, each table row = 1 unit).
  Count them in "units_total"
- The ideal reply is the minimum that answers: the value, command, action or decision itself.
  Reasons, alternatives, background, caveats or questions the user did not ask for are noise.
  Allowed extras: one clause that flips the decision, warns of real harm, or corrects a wrong premise
  with the fact the user was reaching for
- "deletable": units the user would not miss if removed: intros, restated questions, recaps, closing
  offers, reasons, alternatives, background or caveats nobody asked for
- "echoes": phrases inside any unit that repeat what the user's question already said, e.g. "5 feet
  is" in an answer to "convert 5 feet to meters"
- "missing": information the user needs that is absent or wrong
- "first_line_answers": true if the first line alone gives the answer or main point (for a clarifying
  reply, the question itself)
- "structure_fits": true if the form fits the content, using these user preferences: a few short
  items = one inline sentence; grouped items or a staged plan = small headings with short vertical
  lists; how something works = short numbered steps; why something happens = one sentence; two
  options = list with bold option names; three or more options = table with options as ROWS ordered
  best-first; shell commands = one command per fenced block tagged bash (so the app shows a Run button),
  several steps = short label per step each with its own block; code = fenced block without comments; errors and test output = raw in a code block. No unbroken paragraph
  over about 60 words. False if several key facts or conditions are packed into one paragraph.
  Asking the user for a decision = ### Context, ### Question, ### Options with the recommended option
  first, marked with a check emoji and (recommended). Showing examples or variants = each rendered
  under a short label, separated by ---, no code block or quote around them, no intro or closing
- "concise": true if every unit states its point in as few words as possible. List items must be terse
  fragments: a period at the end of an item, "your", or back-references such as "that server" or "it"
  make this false. False also if any unit
  carries an unrequested reason clause, alternative, explanation or trade-off, even inside a sentence,
  or names, numbers and specifics that do not change the point
- "shape_fits": false if the reply follows a stock template instead of its content, such as a lead-in
  sentence, about three bullets, and a closing sentence or question
- "bold_ok": true if bold marks only the term being defined, an option name, or the key cause.
  False if it marks other phrases, whole sentences, or decorative labels. Emojis make it false, except
  a check emoji marking the recommended option
- "ambiguity_ok": {ambiguity_rule}
- "generalized": {generalization_rule}
- "verdict": "pass" only if deletable, echoes and missing are empty, first_line_answers, structure_fits,
  concise, shape_fits and bold_ok are true, and ambiguity_ok / generalized are true or null.
  Otherwise "fail"
- "reason": one short sentence naming the decisive problem, or "ok"

JSON keys: units_total, deletable, echoes, missing, first_line_answers, structure_fits, concise, shape_fits,
bold_ok, ambiguity_ok, generalized, verdict, reason"""

AMBIG = {True: 'the request is ambiguous in a way that changes the answer: true if the reply asks exactly '
               'one focused question, or states one assumption and answers briefly. Otherwise false',
         False: 'the request is clear: true if the reply asks no clarifying question, otherwise false',
         None: 'null'}
GEN = {True: 'true if the final reply applies the principle behind the earlier feedback or examples, as '
             'described in the expectation, otherwise false',
       None: 'null'}


def judge_case(path, case):
    if STOP.is_set() or weekly_usage() >= 0.95:
        STOP.set()
        return case['id'], 'stopped: weekly usage >= 95%'
    rec = json.loads(path.read_text())
    turns = rec['turns']
    if any(t.get('error') for t in turns):
        return case['id'], 'skipped (run error)'
    conv = '\n\n'.join(f"USER: {t['prompt']}\nASSISTANT: {t['reply']}" for t in turns[:-1]) or '(none)'
    conv += f"\n\nUSER: {turns[-1]['prompt']}"
    prompt = JUDGE.format(expect=case['expect'], conversation=conv, reply=turns[-1]['reply'],
                          ambiguity_rule=AMBIG[case.get('ambiguous')],
                          generalization_rule=GEN[case.get('generalization') or None])
    p = claude(['--settings', '{"disableAllHooks":true}', '--output-format', 'json', '--tools', '',
                '--no-session-persistence'], prompt, SANDBOX)
    try:
        raw = json.loads(p.stdout)['result']
        rec['judge'] = json.loads(re.search(r'\{.*\}', raw, re.S).group(0))
    except (json.JSONDecodeError, KeyError, AttributeError):
        return case['id'], 'judge error'
    path.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
    return case['id'], rec['judge']['verdict']


def weekly_usage():
    try:
        info = json.loads((W / 'usage.json').read_text())
    except (OSError, json.JSONDecodeError):
        return 0
    return max([v.get('utilization', 0) for k, v in (info.get('unifiedWindows') or {}).items()
                if isinstance(v, dict) and ('day' in k or 'week' in k)] or [0])


def pct(xs):
    xs = [x for x in xs if x is not None]
    return f"{100 * sum(xs) / len(xs):.0f}% (n={len(xs)})" if xs else 'n/a'


def report(label, split=None):
    by_id = {c['id']: c for c in CASES}
    recs = [json.loads(p.read_text()) for p in sorted((W / 'results' / label).glob('*.json'))]
    screen = set((W / 'screen.txt').read_text().split()) if split == 'screen' else None
    recs = [r for r in recs if (not split or (r['case'] in screen if screen else by_id[r['case']].get('split', 'train') == split))
            and not any(t.get('error') for t in r['turns'])]
    replies = [t['reply'] for r in recs for t in r['turns']]
    m = [mech(x) for x in replies]
    j = [r['judge'] for r in recs if 'judge' in r]
    snr = [1 - len(x['deletable']) / x['units_total'] for x in j if x['units_total']]
    hooks = [t['hooks'] for r in recs for t in r['turns']]
    skill = SKILL.read_text()
    rows = [
        ('1 signal', 'mean SNR (judge, final replies)', f"{statistics.mean(snr):.2f}" if snr else 'n/a'),
        ('1 signal', 'final replies with 0 deletable units', pct([not x['deletable'] for x in j])),
        ('1 signal', 'mean words / reply (all turns)', f"{statistics.mean(x['words'] for x in m):.0f}"),
        ('1 signal', 'non-depth final replies over 50 words', pct([len(r['turns'][-1]['reply'].split()) > 50
                                                                  for r in recs if not r['case'].startswith('depth')])),
        ('1 signal', 'replies with filler opener or closer', pct([x['opener'] or x['closer'] for x in m])),
        ('2 glance', 'first line answers (judge)', pct([x['first_line_answers'] for x in j])),
        ('1 signal', 'concise units (judge)', pct([x.get('concise') for x in j])),
        ('1 signal', 'final replies echoing the question (judge)', pct([bool(x.get('echoes')) for x in j])),
        ('2 glance', 'structure fits (judge)', pct([x['structure_fits'] for x in j])),
        ('2 glance', 'no stock template (judge)', pct([x.get('shape_fits') for x in j])),
        ('2 glance', 'bold on key words only (judge)', pct([x.get('bold_ok') for x in j])),
        ('2 glance', 'replies with a paragraph > 60 words', pct([x['longest_para_words'] > 60 for x in m])),
        ('2 glance', 'replies with an exactly-3-item list', pct([x['three_list'] for x in m])),
        ('2 glance', 'replies with periods ending list items', pct([x['item_periods'] > 0 for x in m])),
        ('2 glance', 'replies with emoji', pct([x['emoji'] > 0 for x in m])),
        ('3 ambiguity', 'handled correctly (judge)', pct([x['ambiguity_ok'] for x in j])),
        ('4 generalize', 'applied principle (judge)', pct([x['generalized'] for x in j])),
        ('5 enforce', 'turns where hook injected current skill', pct([any(h['current_skill'] for h in hs) for hs in hooks])),
        ('5 enforce', 'turns with nemo-general output style', pct([t.get('output_style') == 'nemo-general' for r in recs for t in r['turns']])),
        ('5 enforce', 'turns with cut-pass reminder', pct([bool(t.get('reminder')) for r in recs for t in r['turns']])),
        ('5 enforce', 'final replies passing every check (judge)', pct([x['verdict'] == 'pass' for x in j])),
        ('6 cost', 'skill size (approx tokens, chars/4)', str(len(skill) // 4)),
        ('6 cost', 'mean output tokens / reply', f"{statistics.mean(t['usage']['output_tokens'] for r in recs for t in r['turns'] if t['usage']):.0f}"),
    ]
    print(f"| Goal | Metric | {label} |\n| --- | --- | --- |")
    for g, k, v in rows:
        print(f'| {g} | {k} | {v} |')
    print()
    for r in recs:
        jd = r.get('judge', {})
        print(f"- {r['case']}: {jd.get('verdict', '?')} - {jd.get('reason', '')}")


def selftest():
    a = mech('Sure! Here it is.\n\nLet me know if you want more.')
    assert a['opener'] and a['closer'] and a['questions'] == 0
    b = mech('1000 bytes. Which one do you mean?\n\n- a\n- b')
    assert not b['opener'] and not b['closer'] and b['questions'] == 1 and b['longest_para_words'] == 7
    assert mech('ok ✅')['emoji'] == 1
    assert mech('- a.\n- b\n')['item_periods'] == 1
    print('selftest ok')


if __name__ == '__main__':
    cmd, *rest = sys.argv[1:]
    if cmd == 'selftest':
        selftest()
    elif cmd == 'report':
        report(*rest)
    elif cmd == 'usage':
        print(weekly_usage())
    elif cmd == 'run':
        label, ids = rest[0], set(rest[1:])
        out = W / 'results' / label
        out.mkdir(parents=True, exist_ok=True)
        SANDBOX.mkdir(exist_ok=True)
        text = SKILL.read_text()
        with ThreadPoolExecutor(4) as ex:
            for cid, errs in ex.map(lambda c: run_case(c, out, text), [c for c in CASES if not ids or c['id'] in ids]):
                print(cid, errs or 'ok', flush=True)
    elif cmd == 'judge':
        by_id = {c['id']: c for c in CASES}
        paths = [p for p in sorted((W / 'results' / rest[0]).glob('*.json')) if not rest[1:] or p.stem in rest[1:]]
        with ThreadPoolExecutor(4) as ex:
            for cid, v in ex.map(lambda p: judge_case(p, by_id[p.stem]), paths):
                print(cid, v, flush=True)
