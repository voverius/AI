
# Format and distribution
Use the [Agent Skills overview](https://agentskills.io/home) and
[specification](https://agentskills.io/specification) as the format authority.
Consult current specification details when adding unfamiliar metadata or compatibility features.

- Package a `SKILL.md` with YAML frontmatter containing `name` and `description`
- Name: 1–64 lowercase letters/numbers/hyphens; match the directory
- Description: non-empty, at most 1,024 characters; explain capability and activation conditions
- Add optional metadata only for an actual need. Host-specific invocation settings are not portable 
  standard fields; verify their behaviour on the target host
- Keep references directly reachable from the entry. Resolve each resource relative to its 
  containing file and verify it in the distributed package
- Bundle scripts or assets only when execution or output needs them. Validate scripts 
  independently of prose

Use an available format validator and inspect its coverage. Also check referenced resources and 
declared dependencies. Syntax validation does not establish correct routing or task results.

Keep maintained source separate from installation. Use the established installer; avoid manual 
copies and development-directory fallbacks. Verify global discovery where required and ensure 
installed resources work without a project-local copy. A supported format does not establish 
compatibility with every host.

Additional primary guidance, consulted as needed:
[authoring](https://agentskills.io/skill-creation/best-practices),
[activation](https://agentskills.io/skill-creation/optimizing-descriptions),
[evaluation](https://agentskills.io/skill-creation/evaluating-skills).
