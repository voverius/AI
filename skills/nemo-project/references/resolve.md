
# Resolve the project
- New projects go in `~/Projects/<project>/`, the domain location for a new knowledge root
- A project that already lives elsewhere is valid legacy work. Use that root and do not require
  migration
- Select it from the user's request and its local contract
- Implementation repositories stay outside that root, including when that repository is the tool's
  working directory. That repository's local instructions govern repository work, not the knowledge
  project's identity
- If several projects fit, ask which one before reading subjects or writing
- If the named root is missing, report it. Create one only for an authorized bootstrap
- Resolve symbolic links before treating two paths as separate projects. Keep one knowledge root
- Do not create a parallel tree or move existing work unless migration is requested
- Once, on selection: real path, readable directory, writability for a requested write, and
  orientation from README or the project contract. Recheck only when the root, access, or operation
  changes
- On failure, report the path and the failed check. Do not switch directories silently
- For an authorized creation, verify the existing parent is writable, create the directory, then
  check the result. An empty root needs explicit setup intent
- Writes follow the global agent rules. The tool default may still be an external repository, and an
  earlier command does not change that default. Write project files under the selected root

