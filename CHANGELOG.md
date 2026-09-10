# Changelog

## 1.2.4

- A skill you switch off now stays off through saves and reloads, instead of switching itself back on the next time you load.
- The description now shows how to switch a single skill off and on again with the game's own console.

## 1.2.3

- The description now explains the mutation change in plain terms, instead of a line that read as though mutations had stopped working.
- A version the checks cannot read is now reported plainly, instead of stopping the build with an error of its own.
- Files left behind by an earlier build no longer make the checks fail.

## 1.2.2

- The mod comparison now reads as a list instead of one run-on block, both in the download and on the page.

## 1.2.1

- The description now says what mutagens and mutations each do under this mod, and no longer says mutations are untouched.
- The download now carries the changelog and a written comparison against the similar mods examined, so both can be read without opening the page.
- A change to the description can no longer ship without the changelog saying what changed in it.

## 1.2.0

- Every mutation you have researched is now active at once, rather than only the one you have equipped in the mutations panel.
- Every mutation that does something the moment a fight starts now does it, instead of only the first one taking effect.
- The mod now changes playerWitcher.ws as well as playerAbilityManager.ws, so run Script Merger if another mod you use touches that file.
- The changes this mod makes to the game's own scripts are now kept as a recorded set, so it can be rebuilt onto a newer version of those scripts instead of being redone by hand.
- That recorded set is now checked against the game's untouched scripts, so a rebuild reproduces the mod exactly rather than doubling up a line.

## 1.1.1

- Internal comment tidy up.

## 1.1.0

- Every skill you have already learned switches itself on the first time you load a save, so a playthrough already under way needs no Potion of Clearance.
- A learned skill that is neither always active nor socketed now has its bonus taken back off as you load, so nothing lingers after you come across from another always-active mod.
- A skill the game blocks for a quest stays blocked, and comes back on by itself once the block lifts.
- The game log now names the version of All Skills Always Active you are running.
