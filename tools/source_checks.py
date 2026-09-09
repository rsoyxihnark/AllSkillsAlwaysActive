import io, os, re, sys

import graft

MOD = 'modAllSkillsAlwaysActive'
SCRIPT = MOD + '/content/scripts/game/gameplay/ability/playerAbilityManager.ws'
VERSION_FILE = MOD + '/content/scripts/local/allSkillsAlwaysActive.ws'
README = 'README.md'
CHANGELOG = 'CHANGELOG.md'

VERSION_FUNCTION = 'AllSkillsAlwaysActiveVersion'
AUTO_ACTIVE_COUNT = 73
DASHES = '\u2013\u2014\u2012\u2015'

SLOT_ONLY = [
    ('S_Magic_s01', 'Sweep'),
    ('S_Magic_s02', 'Firestream'),
    ('S_Magic_s03', 'Magic Trap'),
    ('S_Magic_s04', 'Active Shield'),
    ('S_Magic_s05', 'Puppet'),
    ('S_Perk_14', 'Gorged on Power'),
    ('S_Perk_19', 'Battle Frenzy'),
]


def read_utf16(path):
    raw = io.open(path, 'rb').read()
    if not raw.startswith(b'\xff\xfe'):
        raise ValueError(path + ' does not start with a UTF-16 little-endian mark')
    text = raw.decode('utf-16')
    if b'\xff\xfe' + text.encode('utf-16-le') != raw:
        raise ValueError(path + ' does not survive being read and written back unchanged')
    return text


def newline_report(path, text):
    bare = text.replace('\r\n', '')
    if '\n' in bare or '\r' in bare:
        return path + ' carries a line ending that is not a carriage return and line feed'
    return None


def strip_comments(text):
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '/' and i + 1 < n and text[i + 1] == '/':
            while i < n and text[i] != '\n':
                i += 1
        elif c == '/' and i + 1 < n and text[i + 1] == '*':
            i += 2
            while i + 1 < n and not (text[i] == '*' and text[i + 1] == '/'):
                i += 1
            i += 2
        elif c in '"\'':
            quote = c
            out.append(c)
            i += 1
            while i < n and text[i] != quote:
                if text[i] == '\\' and i + 1 < n:
                    out.append(text[i])
                    i += 1
                out.append(text[i])
                i += 1
            if i < n:
                out.append(text[i])
                i += 1
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def declared_version(code):
    found = re.search(
        r'function\s+' + VERSION_FUNCTION + r'\s*\(\s*\)\s*:\s*string\s*\{\s*return\s*"([^"]*)"\s*;',
        code, re.S)
    if not found:
        return None
    return found.group(1)


def text_files():
    for root, dirs, names in os.walk('.'):
        dirs[:] = [d for d in dirs if d != '.git']
        for name in sorted(names):
            path = os.path.join(root, name)
            if path.endswith('.ws'):
                yield path, read_utf16(path)
                continue
            try:
                yield path, io.open(path, encoding='utf-8').read()
            except (UnicodeDecodeError, OSError):
                continue


def changelog_sections(text):
    out, version, said = [], None, []
    for line in text.split('\n'):
        head = re.match(r'^##\s+(.+?)\s*$', line)
        if head:
            if version is not None:
                out.append((version, said))
            version, said = head.group(1), []
            continue
        entry = re.match(r'^-\s+(.*\S)\s*$', line)
        if entry and version is not None:
            said.append(entry.group(1))
    if version is not None:
        out.append((version, said))
    return out


def main(argv):
    script = read_utf16(SCRIPT)
    version_source = read_utf16(VERSION_FILE)
    code = strip_comments(script)
    version_code = strip_comments(version_source)
    version = declared_version(version_code)

    if '--version' in argv:
        if not version:
            sys.stderr.write(VERSION_FILE + ' declares no version\n')
            return 1
        sys.stdout.write(version + '\n')
        return 0

    wrong = []

    for path, text in [(SCRIPT, script), (VERSION_FILE, version_source)]:
        bad = newline_report(path, text)
        if bad:
            wrong.append(bad)

    if not version:
        wrong.append(VERSION_FILE + ' declares no version through ' + VERSION_FUNCTION)
    elif not re.match(r'^\d+\.\d+\.\d+$', version):
        wrong.append('the version ' + version + ' is not three numbers separated by full stops')

    elsewhere = [p for p, t in text_files()
                 if os.path.relpath(p, '.').replace(os.sep, '/') != VERSION_FILE
                 and re.search(r'"' + re.escape(version) + r'"', t)]
    if elsewhere:
        wrong.append('the version is written into the source in more than one place: ' + ', '.join(elsewhere))

    if VERSION_FUNCTION + '()' not in code:
        wrong.append(SCRIPT + ' never reads the version back, so the game log cannot say which version is loaded')

    pushed = re.findall(r'activeSkills\.PushBack\(\s*([A-Za-z0-9_]+)\s*\)', code)
    if len(pushed) != AUTO_ACTIVE_COUNT:
        wrong.append('the always-active list holds ' + str(len(pushed)) +
                     ' skills and this check expects ' + str(AUTO_ACTIVE_COUNT) +
                     '; change the number here when the list changes on purpose')
    seen, twice = set(), []
    for skill in pushed:
        if skill in seen:
            twice.append(skill)
        seen.add(skill)
    if twice:
        wrong.append('the always-active list names these skills more than once: ' + ', '.join(sorted(set(twice))))

    shown_to_players = io.open(README, encoding='utf-8').read().lower()
    for skill, shown in SLOT_ONLY:
        if skill in seen:
            wrong.append(shown + ' (' + skill + ') replaces a default behaviour, so it stays slot-based '
                         'and may not sit in the always-active list')
        if shown.lower() not in shown_to_players:
            wrong.append(README + ' does not name ' + shown + ', which still needs a skill slot')

    equipped = re.search(r'function\s+IsSkillEquipped\s*\([^)]*\)\s*:\s*bool\s*\{(.*?)\n\t\}', code, re.S)
    if not equipped:
        wrong.append(SCRIPT + ' no longer declares IsSkillEquipped, which is what makes a learned skill count as active')
    elif 'activeSkills.Contains' not in equipped.group(1):
        wrong.append('IsSkillEquipped no longer consults the always-active list, so no skill would work without a slot')

    modded = graft.read_ws(SCRIPT)
    base, undescribed = graft.strip(modded, graft.load_edits())
    if undescribed:
        wrong.extend(undescribed)
        wrong.append('tools/edits.json no longer describes the script, so the mod could not be rebuilt '
                     'onto a fresh base; update it in the same commit as the change')
    else:
        rebuilt, missed = graft.apply(base, graft.load_edits())
        wrong.extend(missed)
        if not missed and rebuilt != modded:
            wrong.append('grafting the edits back onto the base does not reproduce the script they came from')

    sections = changelog_sections(io.open(CHANGELOG, encoding='utf-8').read())
    if not sections:
        wrong.append(CHANGELOG + ' carries no version section')
    else:
        top, said = sections[0]
        if top.lower() != 'unreleased':
            if version and top != version:
                wrong.append(CHANGELOG + ' opens with ' + top + ' and the source carries ' + version +
                             '; the two have to agree before a version ships')
            if not said:
                wrong.append(CHANGELOG + ' opens with ' + top + ' and writes nothing under it')

    for path, text in text_files():
        for line_number, line in enumerate(text.replace('\r\n', '\n').split('\n'), 1):
            for dash in DASHES:
                if dash in line:
                    wrong.append(path + ' line ' + str(line_number) + ' carries a dash that is not a hyphen')
                    break

    if wrong:
        for line in wrong:
            sys.stderr.write(line + '\n')
        return 1
    sys.stdout.write('the source says what this project says it says\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
