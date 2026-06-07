# UC-01: Fresh start — getting oriented

Someone clones the repo, runs `deskops init`, and wants to understand what this project is about without reading every file.

**Interaction flow:**

1. Run `deskops about` → sees a summary of what deskops is, what desk is, what sldb is
2. Run `deskops faq` → sees common Q&A, starts building a mental model
3. Run `deskops atoms list` → sees all atom IDs and titles, starts browsing
4. Run `deskops atoms show atom-deskops` → reads an atom without opening a file
5. Run `deskops graph build` → builds a knowledge graph of the desk
6. Run `deskops graph neighbors atom-deskops` → sees what connects to what

**What this user is trying to do:**
Get a lay of the land. They want answers to "what is this?", "how does it work?", "where do I start?" without digging through folders manually. The CLI is their map.

**When this breaks:**
- `init` doesn't scaffold a working desk
- `graph build` fails silently or produces an empty snapshot
- atoms list shows nothing or wrong content
- The mental model from `faq` doesn't match what `atoms list` shows
