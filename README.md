# Reload Checker Tool

A tool that helps combine Smogon scouts (typically in a team tournament environment) to quickly check if a given opponent is reloading a team revealed at some other point prior.
Type the opposing team's six Pokemon, press Enter, and see the matching team sheet(s) and who they came from.

## First-time setup (one time only)

1. Get the files. On the GitHub page click the big green Code button, then Download ZIP.
   Right-click the ZIP and choose Extract All (do not run it from inside the ZIP).
2. Install Python (skip if you already have it): go to https://www.python.org/downloads/,
   download, run the installer, and tick "Add python.exe to PATH" on the first screen.
   I assume that if you're on Linux you can handle downloading Python lol.
4. The current file contents of `teams.txt` is just an example. You need to add your own
   scouts for the tool to be useful to your team.
5. Gather replays and use the tool at https://fulllifegames.com/Tools/ReplayScouter/#/ to
   format them. After scouting with the tool, set the grouping to "Text Representation,"
   and copy-paste that output to the bottom of `teams.txt` to update it for your use-cases.
6. Provide your teammates with the updated version of `teams.txt` so their tool will operate
   correctly.

## Every match

1. Double-click **run.bat** in the folder it extracted to.
2. Type or paste the six opposing Pokemon separated by commas, then press Enter:
   Amoonguss,Celesteela,Hippowdon,Hydreigon,Slowbro,Tyranitar
3. Read the result. The prompt comes back immediately, so you can search again.
   Windows may show a blue "Windows protected your PC" box the first time.
   Click More info, then Run anyway.

## Rules

* Capitalization, spaces around commas, and order don't matter. You DO need to include spaces in
  the middle of names. E.g. `Tapu lele` not `TapuLele`
* You must enter exactly 6 Pokemon. Only teams with exactly those 6 are shown.
* Each result shows its source (the name at the top of that section of `teams.txt`)
  and how many replays are linked.
* Team preview shows base forms (`Aerodactyl`, `Ogerpon-Wellspring`), while replays often list
  battle forms (`Aerodactyl-Mega`, `Ogerpon-Wellspring-Tera`). By default these count as the same Pokemon.
  To turn that off, open `main.py` in Notepad and change
  `IGNORE_BATTLE_FORMS = True` to `False`.
* Sheets with many replay links show the first 3 and a "+N more" count. Change
  `MAX_REPLAYS_SHOWN` in `main.py` (0 = show all).

## Adding teams / sources

Paste each source's whole block onto the end of `teams.txt`, in this layout:

    SourceName:

    Pokemon1, Pokemon2, Pokemon3, Pokemon4, Pokemon5, Pokemon6:
    https://replay.pokemonshowdown.com/first-replay
    https://replay.pokemonshowdown.com/another-replay-of-the-same-team

    (the team sheet, blank line between Pokemon)
    
**IMPORTANT:** This formatting is from https://fulllifegames.com/Tools/ReplayScouter/#/. 
               After scouting with the tool, set the grouping to "Text Representation," and copy-paste 
               that output to the bottom of `teams.txt` to update it for your use-cases.

- The line ending in a colon with no commas is the source name. It applies to every team below
  it until the next source name.
- The line of six names ending in a colon is what gets searched. Every team needs one.
- A team can have one or many replay links.
- Any source name and any number of sources works.
- Restart the program after editing the file.


=== If you have any issues or need further assistance, feel free to reach me on Discord at @ani\_wan\_kenobi ===
