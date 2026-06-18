# Capture lesson
> Distill the just-completed conformance work into an AC-keyed field note (and,
> where design-specific, a design-repo note). Use right after an AC-driven
> feature's tests pass — the moment the lesson is real (a green test proves it
> load-bearing) and still fresh.

Follow [`pna-toolkit/SKILL.md` § Capturing a conformance lesson](../../pna-toolkit/SKILL.md):

1. **Identify the AC(s)** the just-green / just-merged work bears on — from the
   diff and the tests, not from memory.
2. **Split generalizable from design-specific.** The generalizable lesson → an
   AC-keyed field note at `docs/field-notes/<AC-ID>.md` (per
   [`docs/field-notes/README.md`](../../docs/field-notes/README.md)); the
   design-specific "how we did it" stays in the design's own repo.
3. **Draft from this session + the diff + the negative tests.** Fill the entry
   format; link each negative invariant to the test that pins it. Keep it short.
4. **Honest decline.** If there's no generalizable lesson, say so in one line —
   never manufacture a note.

Then surface the drafted note for the user to edit before committing.
