# All Skills Always Active

✅Every skill you learn works immediately without equipping.
✅It works on a fresh game or mid-playthrough save.
✅Every mutation you research stays active, all of them at once, not just the one in the slot.
❌No skill slot needed.
❌No reset & re-learning ability points with Potion of Clearance needed.

INSTALLATION

1. Copy the modAllSkillsAlwaysActive folder into "...\Steam\steamapps\common\The Witcher 3\mods".
2. Launch & enjoy, no action required even on an existing save. Activates on the first gameload automatically.

HOW TO CHECK IT IS WORKING
- Learn Strong Back without socketing it: your carry weight rises immediately.
- Learn Acquired Tolerance: your maximum toxicity climbs with every alchemy formula you know.
- Research a second mutation: the first one keeps working, and the mutations panel still shows whichever you slotted.

UNINSTALLATION
1. Drink a Potion of Clearance, then save and quit. Debug console command below:
additem('Clearing Potion')
2. Delete the modAllSkillsAlwaysActive folder.

- SIGNS -
Q: Why eg:Igni still casts the normal burst instead of Firestream?
A: Not a bug. Firestream is one of the Seven skills that still require a slot, opt-in on purpose. Socket it, then hold the cast button for the stream /OR/ tap for the normal burst. Good news is since nothing else competes for slots anymore, you have 12 free slots for exactly these 7. Socket them all and literally everything in the game is active at once.
1- Aard: Sweep
2- Igni: Firestream
3- Yrden: Magic Trap
4- Quen: Active Shield
5- Axii: Puppet
6- Gorged on Power
7- Battle Frenzy

-MUTAGENS AND MUTATIONS-  TLDR; MUTAGENS VANILLA, MUTATIONS ALL ACTIVE.

Mutagens work exactly as in vanilla. Mutations no longer do, as of 1.2.0. Neither needs an external tool.

A mutagen's bonus is multiplied by how many same-colour skills you have SOCKETED in that mutagen's group - in vanilla it counts socketed skills, not learned ones. This mod changes which skills are ACTIVE, not what the mutagen math COUNTS: it overrides the game's "is this skill equipped" check, while the synergy calculation still reads the twelve slots directly.

So if your slots sit empty, your mutagen sits at its plain base bonus. That is the vanilla multiplier having nothing to multiply, not the mod failing, and it is why the number moves as your socketing changes. The upside: socketing is now free. Your skills work either way, so the slots became pure mutagen optimisation - put three blue skills in the group holding your blue mutagen for maximum sign intensity. Only the seven behaviour-replacing skills have a real claim on a slot, which still leaves five spare.

Mutations changed in 1.2.0: every mutation you have researched is now active at the same time, instead of only the one sitting in the mutations panel. Everything around them is still vanilla - the grid, the mutagen count that unlocks slots, each mutation's cost, and the panel still showing whichever one you slotted. This is the one place the mod now edits a second game file, playerWitcher.ws, so run Script Merger if another mod you use touches it. If you want the one-at-a-time rule back, stay on 1.1.1.
