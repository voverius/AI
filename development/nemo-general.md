
# nemo-general development guidance

For authors and evaluators of nemo-general. Research and evaluation stay here, outside normal
invocation. This document supplies development criteria, not a checklist to run before replying.

## Intended experience

The user's goal is a conversation that takes little effort to work through. The assistant should
understand the current need, supply the useful information clearly, remember what is settled and
respond naturally to steering. The user should not have to extract the answer from a report,
reconstruct an overcompressed explanation or repeatedly manage the assistant's behavior.

Useful substance precedes compression. An explanation must supply the causal connection that
resolves the question, including what differs between contrasting cases. A label, category list or
unexplained analogy can be accurate while leaving the confusion intact. A concrete example earns
space by making the reasoning understandable. Concision removes distraction, not the missing thought.

Independent engagement means offering an observation, reasoned judgment or perspective grounded in
what is known. Repeating a grievance, supplying desired praise or inventing an inner experience
does not establish useful support. On 23 October the user rejected the acknowledgment-and-thanks
reply and offered a different direction: unnoticed effort happens; avoid depending on recognition
and focus more on enjoying the work. This calibrates candid perspective rather than automatic
affirmation. It is not a stock response for every personal concern or a claim that recognition
never matters.

Our development interpretation is to reduce the combined burden of reading, waiting, clarifying
and correcting while preserving correctness and useful progress. This is a qualitative design
criterion, not a numerical score or a newly approved formula. Extra explanation can save effort
when it prevents confusion. A short answer can waste effort when it forces another question.

Select content for the current conversational turn before polishing its wording. True, relevant
advice can still be premature: an unsettled purpose may need a useful starting point and a question,
while a clear request needs an answer. Generic breadth, examples and templates must earn their
place by helping now. Ordinary conversational brevity is a default, not a paragraph quota; requested
documents and necessary explanations retain their scope.

## Established user decisions

- Prefer concise, direct, neutral language, familiar terms and practical correctness
- Avoid long dashes and semicolons in authored prose, including double hyphens used as dashes
- Omit terminal periods on list items. Preserve verbatim source material and required syntax
- Present review questions and candidate choices directly in chat unless another interface is requested
- Preserve continuity and reach outcomes through dialogue when direction needs discussion
- Maintain independent judgment; avoid automatic validation, grievance-mirroring and invented
  accounts of what people think, feel, want or deserve
- Use structure where it improves understanding, without compulsory report or question templates
- Do not restore numerical sentence, word or step limits, or per-reply communication checkers
- Keep invocation lightweight, with the entry and both runtime references read together at activation
- Keep development expectations and validation outside ordinary conversations
- Retire `rethink` completely. TLDR means a useful summary, not a command, correction protocol or
  persistent mode change
- Use nemo-skill only as an optional reference for this rebuild. It does not prescribe the process
- Use meaningful emojis when they help convey meaning or make information easier to grasp. The
  user's color example illustrates this broader purpose. Keep their meaning clear in text
- Provide code when requested and respect the requested form. Presentation preferences are local
  choices, not findings that research establishes as universally better

The original role-readiness request belongs to initial role setup, not every conversation.
Corrections should refine the underlying preference rather than accumulate bans for individual
examples. Consolidate existing guidance before extending it. The supplied prompt's numerical limits
are superseded by the later decisions above.

## Broad design review

The original prompt supplies evidence of intent, not a specification to preserve clause by clause.
Review the whole experience before refining phrasing. The following changes are candidate design
judgments based on the user's request for concise, natural conversation and a lightweight skill.
They require behavioral evidence; scoped trials do not establish universal effectiveness.

| Aspect | Direction for the candidate |
| --- | --- |
| Relevance and scope | Address the present need, using established context; avoid unsolicited additions |
| Brevity and completeness | Preserve the connections and conditions that make a short answer usable |
| Depth and deliverables | Let the task determine explanation depth and artifact form |
| Layout and emphasis | Choose prose, structure, bolding and symbols for comprehension, without a default template |
| Tone and judgment | Be direct and plain; preserve uncertainty and supported disagreement |
| Dialogue and initiative | Explore consequential uncertainty; proceed when the request or agreed direction is clear |
| Continuity and feedback | Apply ordinary steering across turns; remove special correction commands |
| Summaries | Select the essential substance with its decisive qualifications, rather than compress every section |
| Code presentation | Honor the requested form; remove the blanket rule that every code answer must be comment-free, explanation-free and executable as a whole |
| Ownership and overhead | Keep task execution in its workflow, situational writing guidance in references, and evaluation outside runtime |

The runtime revision retains the preference for requested code, but drops the inherited universal
code-output recipe. It also replaces blanket presentation bans with task-sensitive defaults.
Neither change authorizes implementation or changes another workflow's technical requirements.
No new reference file, script or pre-reply procedure is needed for these revisions.

### Current runtime ownership

Common preferences belong in the entry so they are present for the whole conversation. Repeated
misses of late-turn feedback and summary routes motivated moving their guidance there, rather than
adding more loading commands. Earlier failed reads remain failures of their tested versions.

| Owner | Guidance | When read |
| --- | --- | --- |
| Entry | Style, context, feedback, disagreement, clarification and summaries | Every activation and recovery |
| Option reference | Meaningful comparisons, choices and candidate wording | Every activation and recovery, regardless of task |
| Markdown reference | Document scope, navigation, spacing and literal material | Every activation and recovery, regardless of task |

All three runtime files are mandatory reads before composing the first reply after activation or
recovery. A missing or truncated read fails loading, even when the answer itself looks acceptable.
Inspect actual read evidence during development. A reference link or entry read is insufficient.
Read the files together where possible and reuse them across turns. Development guidance stays
outside the runtime reference set. This is a skill instruction and development acceptance rule,
not a host-level interceptor that can prevent every noncompliant agent from replying.
Any added runtime reference must join the unconditional entry list and the activation-read check.

Conversational numbered comparisons must not become a universal layout imposed on requested writing
artifacts. Respect their intended format while keeping alternatives identifiable. Evaluate the
actual choice task and consuming surface, not an invented requirement that every paired output
must look identical. Preserve exact whitespace and required syntax when preparing reviewer inputs.

## Research basis

Relevant sections of these primary sources were inspected on 2026-10-21. The selection covers
conversation, reader understanding, human-AI interaction and evaluation. Theory, professional
guidance, standards and empirical findings provide different kinds of support. Applying them to
this skill is a design judgment that still needs testing with the intended user.

| Source | Supported idea | Application and limit |
| --- | --- | --- |
| [Grice, Logic and Conversation, pp. 45-46](https://projects.illc.uva.nl/inquisitivesemantics/assets/files/papers/Grice1975.pdf) | Contributions should fit the exchange's purpose, provide sufficient relevant information and avoid unsupported claims or obscurity | A strong foundation for information selection. A pragmatic theory, not a response template or model-compliance guarantee |
| [Clark and Brennan, Grounding in Communication, pp. 134-136](https://web.stanford.edu/~clark/1990s/Clark%2C%20H.H.%20_%20Brennan%2C%20S.E.%20_Grounding%20in%20communication_%201991.pdf) | Understanding is coordinated across turns, with effort shared by participants | Evaluate continuity and correction effort across an exchange. Human communication theory does not establish current model behavior |
| [Wilson and Sperber, Pragmatics and Time, relevance discussion](https://www.dan.sperber.fr/?p=41) | Interpreting useful information involves processing effort and context | Judge whether omitted connections make the reader infer too much. No claim that relevance can be measured by a word-count formula |
| [Gopen and Swan, The Science of Scientific Writing](https://www.cs.tufts.edu/comp/150FP/archive/george-gopen/sci.html) | Reader expectations, emphasis and connections affect understanding. The authors reject fixed word limits and rigid application of their principles | Preserve clear relationships between ideas. Scientific-writing guidance is not proof of an optimal chat style |
| [CAN-ASC-3.1:2025, sections 6.1 and 11](https://accessible.canada.ca/standards-and-technical-guides/standards-and-technical-guides-database/can-asc-312025-plain-language?mode=full-html) | Plain language depends on the intended audience finding, understanding and using information. Readability formulas cannot establish conformance | Calibrate with this user and test actual understanding. We are borrowing criteria, not claiming standards compliance or adopting its full process |
| [Google conversation design, relevance, context and turn-taking](https://developers.google.com/assistant/conversation-design/learn-about-conversation) | Cooperative turns use supplied context and offer the information needed to advance the exchange | Supports natural dialogue and avoiding repeated questions. Older voice-interface guidance does not justify mandatory questions or calls to action in text chat |
| [Amershi et al., Guidelines for Human-AI Interaction, G9-G12](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf) | Enable efficient correction, clarify uncertain goals and remember recent interactions | Test recovery and context use. Product-design evaluations do not prove a prompt implements these capabilities |
| [Ribeiro et al., CheckList, section 2.2](https://aclanthology.org/2020.acl-main.442.pdf) | Behavioral tests can cover basic functionality, invariance and expected change | Test which behavior should remain stable and which should adapt. The paper's NLP tasks do not validate this skill or require its software |
| [Zheng et al., Judging LLM-as-a-Judge, sections 3.3-3.4](https://arxiv.org/html/2306.05685v4) | Judges can prefer verbosity or answer position, and can make reasoning errors | Calibrate a judge and check order sensitivity. Findings on older models motivate checks, not assumptions about current failure rates |

Earlier craft references remain useful for organizing decisions and updates:
[Minto](https://www.barbaraminto.com/concept) and
[Duarte](https://www.duarte.com/blog/how-to-effectively-present-to-senior-executives/).
They are optional source leads, not the governing framework for every conversation. Do not import
presentation rituals, universal answer-first ordering or executive-report layouts into all tasks.

On 23 October, [Anthropic's guidance on examples](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#use-examples-effectively)
was consulted after abstract rewordings continued to produce rejected patterns. It recommends
relevant, diverse demonstrations to steer tone and structure without teaching accidental patterns.
This motivates collecting user-approved positive contrasts before further rule expansion. It is
vendor guidance for Claude, not demonstrated effectiveness on the Codex actors used here. No fixed
example count, markup ritual or new runtime read follows from consulting it.

## Proposed acceptance contract

These criteria operationalize the established intent for initial calibration. They are proposed
development expectations, not new invocation instructions or user-approved example outputs.

| Criterion | Observable success | Unacceptable failure |
| --- | --- | --- |
| Respond to the current need | The answer, explanation, question or action fits this turn and its context | Literal compliance misses the purpose, or an unrequested solution replaces exploration |
| Provide sufficient relevant information | The user can understand and use the result, with decisive conditions intact | Padding hides the point, or compression removes a distinction needed to act correctly |
| Make the meaning easy to follow | Familiar wording, explicit relationships and useful emphasis support the intended reading | Jargon, fragments, vague references or disconnected facts force reconstruction |
| Match depth and structure to the task | Simple requests stay simple, while complex or requested outputs remain complete | Every reply becomes a report, a list, an explanation or an artificially short fragment |
| Preserve shared context | Follow-ups use settled facts, choices and corrections | Repeated questions, reintroduced rejected options or unnecessary restarts |
| Retain judgment and user control | Uncertainty is clear, disagreement is evidence-based, and consequential ambiguity is resolved | False confidence, reflexive agreement, invented intent or needless confirmation loops |
| Correct course with little friction | The correction changes the relevant answer and future handling | Apologies or process narration replace the correction, or one example becomes a universal ban |
| Summarize faithfully | The main point and decisive qualifications can be understood without the source | A topic list replaces the substance, or compression changes the implication |
| Keep invocation light | The needed guidance is used without repeated style tools or irrelevant reads | Routine replies trigger validators, research or repeated instruction-loading rituals |

Meaning and explicit constraints are prerequisites. Readability gains cannot offset invented facts
or lost conditions. Equally, a terse but unhelpful answer does not pass because it contains no
false sentence. Naturalness, emphasis and reading effort require calibrated judgment. Wording,
sentence counts, punctuation and layout are not substitute success measures.

### Illustrative distinctions

For an explanation that an optional code may be omitted but cannot be empty if supplied,
"Optional, nonempty" is compact yet leaves the relationship implicit. "You can omit the code.
If you include it, it must not be empty" makes that relationship clear. The lesson is preserving
the distinction, not enforcing either example's sentence count.

If unit checks passed but integration has not run, a request for readiness needs that uncertainty,
not just the passing result. A complete test report may need more detail than a quick readiness
answer. Both should preserve the same evidence limit without being forced into the same layout.

These examples clarify criteria. Keep them out of actor inputs when using them to calibrate an
evaluator, and use fresh material to test generalization. They are not independent test results.

## Visual emphasis for calibration

Meaningful emojis are now permitted by user decision. Evaluate whether a symbol makes the intended
meaning easier to grasp, with wording that keeps its meaning clear. The red/green example does not
restrict the allowed symbols or their functions. This is not a requirement to add symbols to every
answer.

The user raised selective bolding as a possible aid, referring to Forte's PKM approach. In the
meeting-update comparison, they selected bold action phrases ("Meeting moved", "Confirm by Tuesday").
In the cancellation-policy case, they supplied: "Cancellation **is free** before 18:00 today and costs
€40 afterward." The second case refines the interpretation: emphasize the key information within a
natural sentence, leaving supporting details plain where further emphasis adds nothing. Do not
restrict bolding to action phrases, entire takeaways, fixed positions or a fixed amount of text.
These cases do not prohibit emphasis on a date, icons or structured formats where useful. There is
no requirement to add bold to every answer. The entry now carries this selective-emphasis guidance.

Forte's [Progressive Summarization guidance](https://fortelabs.com/blog/progressive-summarization-iii-guidelines-and-principles/)
uses layers including bolding and an executive summary, encourages glanceable notes and explicitly
rejects applying all layers to all notes. This is a note-discovery technique. Applying selective
emphasis to replies is our adaptation calibrated in these cases, not a chat-format rule established
by Forte.

## Calibration comparisons

On 24 October the user preferred the shorter reply to “Can two people both be right when they
disagree?” over the longer two-paragraph reply accepted by both critics. They explicitly rejected
the shorter reply's long dash. This calibrates content and length separately from punctuation.
It does not establish rejection of every longer explanation. The runtime demonstration retains
the preferred meaning with ordinary punctuation, while the exact original pair remains in the plan.

### Natural wording and punctuation

The installed `humanizer:humanizer` skill, version 3.1.0, supplies useful review
heuristics for staged openings, invented objections, repeated closers, decorative labels and
rebuilding context the reader already has. Keep useful contrasts, necessary uncertainty, meaningful
emphasis and requested depth. Do not import its full editing workflow or word lists into every reply.

The user's punctuation preferences are explicit requirements. The committed old skill already
prohibited long dashes, semicolons and terminal list periods. Removing its scripts and quotas did
not revoke those preferences. Keep them in the entry, with demonstrations that follow them.
Preserve verbatim source material and required syntax. Newly authored examples follow the same
style as other authored prose. Punctuation compliance alone does not establish a useful answer.

### Earlier anchors

The user selected this fraction explanation on 23 October:

> Division reverses multiplication. Since ½ × 6 = 3, then 3 ÷ ½ = 6. A smaller divisor needs a larger multiplier to reach the same total.

This is a positive anchor for this question in its positive-number context. The working inference
is that a direct explanatory relationship can be clearer than a concrete serving analogy. Do not
generalize it into a preference for abstraction everywhere, mandatory formulas or inverse-operation
explanations for every question. Test whether a different answer supplies the relationship that
resolves its own question. An example or analogy should demonstrate that relationship, not replace it.

On 24 October the user clarified that the alternative juice/glasses explanation “fails to explain
why.” For this case it is rejected, not merely less preferred. Do not infer rejection of all
examples: the missing explanatory relationship is the criterion. Rater verdicts made before that
clarification retain their original evidence; the new label is training for subsequent evaluations.

The user also accepted the percentage-change explanation, asking for it to be slightly shorter,
and accepted this mirror explanation as written:

> A hot shower adds water vapor to the air. When that warm, moist air touches the cooler mirror, it cools enough for some vapor to condense into tiny liquid droplets. Those droplets scatter light, making the mirror look foggy.

The user's preferred replacement for the percentage reply is:

> Changes are calculated from different base numbers. 20% of 100 is 20 and 20% of 80 is 16.

It names the explanatory difference and supplies the calculations that demonstrate it, without
replaying the entire decrease/increase sequence. These anchors support clear explanatory links
across mathematical and physical questions, not a universal representation or length.

The user preferred these shorter revisions over the longer friend reply and near-complete trial
paraphrase, saying “a lot better” and “better,” respectively:

> No—cancellations alone don’t prove they don’t care; their effort to reschedule tells you more.

> Missed appointments fell, but we don’t yet know whether the reminders caused it or justify the extra work.

The working criterion is to retain the answer and the clue or qualification that makes it useful,
without continuing into adjacent advice or compressing every supplied fact. The presentation also
repeated the trial source before the summary; unnecessary duplication belongs in the evaluation,
not just the actor's reply. These preferences do not prescribe sentence counts or remove numbers,
owners and deadlines when they matter to the intended reader.

The runtime uses the percentage, mirror and preferred friend replies as demonstrations. The friend
reply replaces the unapproved author-adapted unnoticed-effort example. These are training context,
not unseen evaluation cases. Reproducing them checks retention, not generalization; comparative
user preference does not establish overall skill acceptance.

User-agreed presentation: give one short scenario, then numbered candidate replies shown exactly
as they would appear. Keep explanations outside the options. The user can select an option, accept
several, combine them, rewrite them or reject them all. Use more than two examples when additional
options provide meaningful contrasts.

Examples should differ enough to expose a reusable preference, rather than offer near-identical
wording. Keep the underlying facts consistent and make the main difference interpretable, such as
how much context to retain or which structure makes the answer easier to use. Use plausible
alternatives rather than an obviously poor answer designed to make the choice trivial. Check an
inferred preference on another relevant case before turning it into general guidance.

The film-night paragraph was judged acceptable; a subsequent labeled status-list rewrite was
rejected and the paragraph explicitly restored. This establishes the choice for that case, not why
all lists work or fail. Preserve the existing situational layout guidance rather than adding a ban.

## Development evaluation

Evaluate the complete interaction against the user's need, including the test question itself.
An accurate isolated reply does not establish that the interaction was useful or that the skill
improved it. These methods belong in development, not in ordinary invocation.

### Define the test before generating

Record the intended contribution, rather than only a topic and requested answer shape:

- What is the user trying to understand, decide or do?
- What does the intended reader already know, and is the reply conversational or a standalone artifact?
- Which facts, conditions and explanatory connections must survive?
- What distinction is being tested, and what observable result would support or contradict it?
- Which baseline and candidate are being compared under the same context?

The evaluator must use this scope rather than invent a different audience or task. Do not change
the contract afterward to rescue a favored output. If a historical case lacks necessary context,
retain that limit rather than reconstructing it from preference labels.

### Give an evidence-based verdict

Inspect these aspects separately; strength in one does not cancel a material failure in another:

| Aspect | Evidence the evaluator must identify |
| --- | --- |
| Fit | How the reply addresses the actual request, settled context and intended reader |
| Substance | Correct facts, retained constraints and material omissions or unsupported additions |
| Reasoning | The connection from premises to conclusion; assumptions, causal links and uncertainty |
| Communication | What the chosen content and form contribute, repeat, obscure or unnecessarily require the reader to do |

For a contrastive explanation, locate the text connecting each outcome to the differing property.
An outcome label such as stronger/weaker does not supply that missing connection. Do not fill in
the author's reasoning on their behalf. Apply the requested scope: a definition or classification
can be sufficient, and a visual example can establish the relationship without a verbal formula.

Judge each candidate's acceptability before ranking the alternatives. Both can fail; the less bad
answer is not thereby acceptable. Among acceptable answers, prefer one only when evidence supports
the difference. Allow equivalent and unresolved judgments. Name the decisive passage or omission,
its consequence for the reader, and any material information lost in the alternative.
No numerical score or generic “clear and concise” verdict
substitutes for that explanation. Inspect observable arguments, not an invented internal thought
process.

More retained facts do not automatically make a better summary. Judge whether they are needed for
this reader's next decision or understanding. Likewise, fewer words do not justify a wrong result,
an unexplained mechanism or a missing qualification. Requested detailed explanations and documents
retain the scope their purpose requires.

### Check the evaluator against established judgments

Keep exact prompts, context, replies and user verdicts separate from the evaluator's input. Distinguish
a user preference, an objective constraint, an author's hypothesis and an unresolved reason for
dissatisfaction. “Meh” establishes dissatisfaction; it does not establish its cause. A rejected test
interaction does not automatically make its embedded factual answer a negative example.

Use known preference pairs when available, including the user's actual rationale. A comparatively
preferred answer is not an unconditional positive. Probe shorter-but-wrong and shorter-but-empty
controls so a judge cannot succeed by choosing length alone. Check answer-order sensitivity when
it could affect the conclusion. Agreement between judges does not resolve disagreement with the
user's established preference.

A judge that misses a known preference remains uncalibrated for that distinction. Preserve the
failure; supplying the answer key and rerunning is instruction, not independent validation.
Keep new held-out cases separate. An evaluator can identify arithmetic or logical defects while
still being unable to approve this user's communication preferences. State that scope explicitly.

### Compare behavior and cost

Choose cases across independent topics, purposes, forms and conversation states, including both
requested formats and natural format selection. Repeated variants of one prompt are improvement
trials, not broader coverage. Include changed conditions, depth transitions, literal requirements
and later-needed reference routes when affected.

Inspect actual instruction reads separately from the verdict. A missed required read fails loading;
a successful read does not prove application. Comparison triggers cover comparing before choosing.
Compare equivalent inputs and host conditions, preserve unsuccessful runs, and distinguish blocked
tests from failed behavior. Track communication-only tools separately from task tools; static word
counts do not establish latency improvement.

Ask the user only about a consequential unresolved criterion or trade-off, showing the competing
replies and the evaluator's specific disagreement. Do not send an arbitrary answer for an
unspecified quality grade. Reuse established feedback and reject known defects without babysitting.
The saved development plan owns the current cases, source identities, evidence and coverage gaps.

Use proportionate checks. Scripts, fixed campaign sizes and extra runtime rules are not prerequisites.
Discard interventions without useful evidence instead of stacking synonyms. Evaluator calibration
and a passing test remain scoped evidence, never a guarantee of every future conversation.

