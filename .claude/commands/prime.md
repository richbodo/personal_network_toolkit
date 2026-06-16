# Prime
> Read-only orientation: understand the codebase and where you are, then
> summarize. Do NOT switch branches, pull, or create a worktree while priming —
> just orient. (See CLAUDE.md § Worktrees for when to branch.)

## Run
git ls-files
git status -sb          # current branch + ahead/behind + dirty state
git worktree list       # sibling worktrees other agents may be using
just

## Read
README.md
spec/PNA_Spec.md
pna-toolkit/SKILL.md
docs/users-guide.md
CLAUDE.md

## Before summarizing
- Note your current branch. If any sibling worktree from `git worktree list`
  looks like it's on a related feature/bug, flag the possible overlap.
- The reference designs (fellows_local_db, prm) are sibling checkouts one level
  up — see CLAUDE.md § Sibling repositories. Don't restate worktree policy;
  CLAUDE.md owns it.
