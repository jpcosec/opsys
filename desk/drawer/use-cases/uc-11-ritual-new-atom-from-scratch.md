# UC-11: Ritual — "I need to write a new atom"

The user has a concept they want to capture as an atom. They don't remember the exact conventions — frontmatter, tags, 5WH1+ field, reference format.

**Interaction flow:**

1. `deskops atoms new "Why we use pydantic over dataclasses"` → scaffolds a new atom file
2. Opens the file: template is pre-filled with ID, tags section, answer section
3. User writes the answer, adds tags, saves
4. `deskops atoms validate my-new-atom` → checks frontmatter, tags, link format
5. `deskops graph build && deskops graph missing` → integrates into knowledge model
6. Done.

**What this user is trying to do:**
Lower the barrier to creating good atoms. They want the tool to handle the boilerplate and conventions so they can focus on the content.

**When this breaks:**
- Scaffold creates a file in the wrong location
- Template is missing required fields
- `validate` is too strict (rejects valid atoms) or too lax (accepts garbage)
- No undo — scaffolding the wrong thing creates cleanup work
- User has to remember the atom ID syntax — tool should auto-generate it
- New atom isn't automatically picked up by the next `graph build`
