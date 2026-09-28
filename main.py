"""Pokemon Team Finder
Type the opposing team's six Pokemon (comma-separated) and instantly see every
team sheet in teams.txt whose roster is EXACTLY those six Pokemon.

teams.txt layout (repeat the whole block for each source/user):

    SourceName:

    Poke1, Poke2, Poke3, Poke4, Poke5, Poke6:
    https://replay...            <- one or more replay links
    https://replay...

    (Pokemon blocks)
"""

import re
import sys
import unicodedata
from pathlib import Path

TEAMS_FILE = Path(__file__).resolve().parent / "teams.txt"
TEAM_SIZE = 6

# Team preview only shows the base form ("Aerodactyl", "Ogerpon-Wellspring"),
# but replay-based headers list the in-battle form ("Aerodactyl-Mega",
# "Ogerpon-Wellspring-Tera"). True = treat these as the same species.
# False = strictly literal matching.
IGNORE_BATTLE_FORMS = True
BATTLE_FORM_WORDS = ("mega", "primal", "tera")  # add more words here if needed

# Teams can have dozens of replay links. Show only the first few (the rest are
# counted). Set to 0 to show every link.
MAX_REPLAYS_SHOWN = 3

NO_SOURCE = "unknown source"


def species_key(name):
    """Comparison key for a Pokemon name: ignores capitalization, accents,
    spaces/hyphens/punctuation and word order ('rotom wash' == 'Rotom-Wash')."""
    text = unicodedata.normalize("NFKD", name)
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    words = re.findall(r"[a-z0-9]+", text)
    if IGNORE_BATTLE_FORMS:
        if "mega" in words:  # Charizard-Mega-X / -Y
            words = [w for w in words if w not in ("x", "y")]
        words = [w for w in words if w not in BATTLE_FORM_WORDS]
    return " ".join(sorted(words))


def is_team_header(line):
    """'Name, Name, Name, Name, Name, Name:'  (colon at end, contains commas)."""
    return (line.endswith(":") and "," in line
            and not line.startswith("-") and "@" not in line)


def is_source_header(line):
    """'SourceName:'  (colon at end, no commas)."""
    return (line.endswith(":") and "," not in line and len(line) > 1
            and not line.startswith("-") and "@" not in line)


def is_url(line):
    return line.strip().lower().startswith(("http://", "https://"))


def load_teams(path):
    """Read teams.txt once.
    Returns (index, known_species, source_counts).
    index: sorted tuple of species keys -> list of {"source", "lines"}."""
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()

    teams = []
    source = NO_SOURCE
    current = None
    for line in lines:
        stripped = line.strip()
        if is_team_header(stripped):
            current = {"source": source, "names": stripped[:-1].split(","),
                       "lines": [line]}
            teams.append(current)
        elif is_source_header(stripped):
            source = stripped[:-1].strip()
            current = None  # the previous team ends here
        elif current is not None:
            current["lines"].append(line)

    index, known, sources, seen = {}, set(), {}, set()
    for team in teams:
        while team["lines"] and not team["lines"][-1].strip():
            team["lines"].pop()  # drop trailing blank lines
        # Skip a sheet pasted twice under the same source (identical text).
        fingerprint = (team["source"], tuple(l.strip() for l in team["lines"]))
        if fingerprint in seen:
            continue
        seen.add(fingerprint)

        keys = [k for k in (species_key(n) for n in team["names"]) if k]
        known.update(keys)
        index.setdefault(tuple(sorted(keys)), []).append(
            {"source": team["source"], "lines": team["lines"]})
        sources[team["source"]] = sources.get(team["source"], 0) + 1
    return index, known, sources


def render(team):
    """Original text of the sheet, capping the number of replay links shown."""
    out, seen, hidden, insert_at = [], 0, 0, None
    for line in team["lines"]:
        if is_url(line):
            seen += 1
            if MAX_REPLAYS_SHOWN and seen > MAX_REPLAYS_SHOWN:
                hidden += 1
                continue
            out.append(line)
            insert_at = len(out)
        else:
            out.append(line)
    if hidden:
        out.insert(insert_at, f"(+{hidden} more replay{'s' if hidden != 1 else ''})")
    return "\n".join(out), seen


def main():
    try:
        sys.stdout.reconfigure(errors="replace")  # never crash on odd characters
    except Exception:
        pass

    if not TEAMS_FILE.exists():
        print(f"Could not find {TEAMS_FILE.name} next to main.py.")
        return

    index, known, sources = load_teams(TEAMS_FILE)
    total = sum(sources.values())
    listing = ", ".join(f"{name} ({n})" for name, n in sources.items())
    print(f"Pokemon Team Finder - {total} team sheets loaded.")
    print(f"Sources: {listing}\n")

    while True:
        try:
            raw = input("Enter opposing team: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return

        names = [n.strip() for n in raw.split(",") if n.strip()]
        if not names:
            continue
        if len(names) != TEAM_SIZE:
            print(f"Need exactly {TEAM_SIZE} Pokemon (you entered {len(names)}). Try again.\n")
            continue

        keys = [species_key(n) for n in names]
        matches = index.get(tuple(sorted(keys)), [])

        if not matches:
            print("\nNo exact match found.")
            unknown = [n for n, k in zip(names, keys) if k not in known]
            if unknown:
                print("Not in teams.txt at all (typo?): " + ", ".join(unknown))
            print()
            continue

        count = len(matches)
        print(f"\n{count} matching team sheet{'s' if count != 1 else ''} found.\n")
        for i, team in enumerate(matches, 1):
            text, replays = render(team)
            label = f" TEAM {i} | {team['source']}"
            if replays:
                label += f" | {replays} replay{'s' if replays != 1 else ''}"
            label += " "
            bar = "=" * 6
            banner = f"{bar}{label}{bar}"
            print(banner + "\n")
            print(text)
            print("\n" + "=" * len(banner) + "\n")


if __name__ == "__main__":
    main()
