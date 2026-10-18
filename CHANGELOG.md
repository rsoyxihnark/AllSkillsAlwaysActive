# Changelog

## 2.1.1

- The description no longer covers the game before the Remaster or its old skill tree, and now lists the six skills that still need a slot.
- The description now says where to look up the code of a skill you want to switch off, instead of pointing at a console command that only writes to the game's log.
- The description now explains the two harmless warnings that name this mod when the game lists script errors.
- The mod's scripts now carry short notes for other modders on the few things that could only be confirmed by testing in the game.
- The mod can now be rebuilt straight from the Remaster's own game scripts, without converting them first.

## 2.1.0

- The mod now switches on the game's debug console, so it opens with the key left of 1 without editing any game file.
- The description now says how to open the debug console and that it stays on after you remove the mod.

## 2.0.0

- The mod now runs on the Remastered game, so anyone still on the game before the Remaster should stay on 1.2.5.
- Every skill in the Remaster's new skill tree now works without a slot, the same as the skills of the old tree.
- The Remaster's own Firestream, Puppet and Battle Frenzy stay slot skills, like the versions before them.
- Every mutation you have researched still runs at once on the Remaster.
- The description now says which game each version is for, what happens to your skill points on a save from before the Remaster, and how to get one mutation at a time back.
- The mod comparison now says it was written for the game before the Remaster, gives this mod's new skill count, and no longer thanks or credits the other mods.
- The checks now also catch the Remaster's Firestream, Puppet or Battle Frenzy being made to work without a slot by mistake.
- The mod's recorded changes now rebuild it exactly onto the Remaster's own game scripts.

## 1.2.5

- The description now says what to do when the game refuses to start and the script errors name another mod, such as Map Quest Objectives.
- The description now names the one file to delete to clear that clash without a merging tool, which keeps every skill working and gives up only all mutations at once.

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
