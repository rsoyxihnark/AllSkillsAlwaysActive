# All Skills Always Active

✅Every skill you learn works immediately without equipping.
✅It works on a fresh game or mid-playthrough save.
✅Every mutation you research runs at once, no more picking one and losing the rest.
❌No skill slot needed.
❌No reset & re-learning ability points with Potion of Clearance needed.

INSTALLATION

1. Copy the modAllSkillsAlwaysActive folder into "...\Steam\steamapps\common\The Witcher 3\mods".
2. Launch & enjoy, no action required even on an existing save. Activates on the first gameload automatically.

HOW TO CHECK IT IS WORKING
- Learn Strong Back without socketing it: your carry weight rises immediately.
- Learn Acquired Tolerance: your maximum toxicity climbs with every alchemy formula you know.
- Research a second mutation: the first one keeps working too. Both are on.

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

- TURNING A SKILL OFF -
Q: Heavy Artillery halves my bombs, Fast Metabolism fights my Metamorphosis build. Can I switch one off without a Potion of Clearance?
A: Yes, and it is the game's own command, nothing to install. Open the debug console and type:
skillblock(S_Perk_20, true)
That skill stops applying and stays off, through saves and reloads, until you turn it back on the same way:
skillblock(S_Perk_20, false)
You keep the skill and you keep the points you spent, it just stops doing anything. The three people ask about most:
S_Perk_20 - Heavy Artillery
S_Alchemy_s15 - Fast Metabolism
S_Alchemy_s03 - Delayed Recovery
Want a different one? Type logskills() in the console and it prints every skill's name.

-MUTAGENS AND MUTATIONS-  TLDR; MUTAGENS UNTOUCHED, ALL YOUR MUTATIONS RUN AT ONCE.

Mutagens work exactly as in vanilla, untouched. Mutations got better in 1.2.0: all of them run at once now. Neither needs an external tool.

A mutagen's bonus is multiplied by how many same-colour skills you have SOCKETED in that mutagen's group - in vanilla it counts socketed skills, not learned ones. This mod changes which skills are ACTIVE, not what the mutagen math COUNTS: it overrides the game's "is this skill equipped" check, while the synergy calculation still reads the twelve slots directly.

So if your slots sit empty, your mutagen sits at its plain base bonus. That is the vanilla multiplier having nothing to multiply, not the mod failing, and it is why the number moves as your socketing changes. The upside: socketing is now free. Your skills work either way, so the slots became pure mutagen optimisation - put three blue skills in the group holding your blue mutagen for maximum sign intensity. Only the seven behaviour-replacing skills have a real claim on a slot, which still leaves five spare.

Vanilla makes you pick one mutation and live with it. Since 1.2.0 you do not: research Euphoria and Metamorphosis and you get both, running together, permanently. Every mutation you have researched is on, all the time.

Nothing else about them changed. Same grid, same research costs, same mutagen count to unlock slots, and the panel still shows whichever one you slotted. That slot just stopped being a limit on what actually runs.

Heads up: this is the only thing in the mod that needs a second game file, playerWitcher.ws. If another mod you use touches that file, read the next section. Want the old one-at-a-time rule back? Stay on 1.1.1.

- SCRIPT ERRORS ON STARTUP -
Q: The game will not start and the errors name a mod I did not expect, something like "'wmkMapMenu' is not a member of 'W3PlayerWitcher'". What is that?
A: Two mods are shipping the same game file, playerWitcher.ws. The game loads exactly one copy of any script file, so the copy that loses takes that mod's additions down with it, and every line in that mod which used them stops compiling. Map Quest Objectives is the one this comes up with most. Any map, HUD or quest mod that adds something to Geralt can do it.

Two ways out. Both work, pick whichever you prefer:

1. Run Script Merger and let it merge playerWitcher.ws. This mod changes two things in that file and nothing else, OnCombatStart and IsMutationActive, and a map or HUD mod touches neither of them, so the merge goes through by itself and you keep both mods whole.

2. Or delete this one file:
...\The Witcher 3\mods\modAllSkillsAlwaysActive\content\scripts\game\player\playerWitcher.ws
Nothing else in the mod needs it. Every skill still works without a slot, the catch up on a save already in progress still works, and the seven slot skills still behave the same. The only thing you give up is all mutations at once, which goes back to the vanilla one at a time. No tools and no merging, because the mod has stopped shipping the file they were fighting over.

Q: Why can the mod not just leave that file alone and put the change somewhere else?
A: There is nowhere else to put it. Both things that decide whether a mutation counts as active live inside playerWitcher.ws, and the game gives a mod no way to change one function on its own: you ship the whole file or you change nothing in it. Every mod that adds something to Geralt is in the same position, which is why they collide in the first place.
