import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EDITS = os.path.join(HERE, 'edits.json')
SCRIPT = os.path.join(ROOT, 'modAllSkillsAlwaysActive', 'content', 'scripts',
                      'game', 'gameplay', 'ability', 'playerAbilityManager.ws')


def read_ws(path):
    raw = io.open(path, 'rb').read()
    if not raw.startswith(b'\xff\xfe'):
        raise ValueError(path + ' does not start with a UTF-16 little-endian mark')
    text = raw.decode('utf-16')
    if b'\xff\xfe' + text.encode('utf-16-le') != raw:
        raise ValueError(path + ' does not survive being read and written back unchanged')
    return text.split('\r\n')


def write_ws(path, lines):
    io.open(path, 'wb').write(b'\xff\xfe' + '\r\n'.join(lines).encode('utf-16-le'))


def load_edits():
    return json.load(io.open(EDITS, encoding='utf-8'))


def find_all(hay, needle):
    if not needle:
        return []
    return [i for i in range(len(hay) - len(needle) + 1) if hay[i:i + len(needle)] == needle]


def strip(lines, edits):
    out = list(lines)
    placed = []
    for edit in edits:
        found = find_all(out, edit['before'] + edit['body'])
        if len(found) != 1:
            return None, [edit['name'] + ' was not found exactly once in the modded script']
        placed.append((found[0] + len(edit['before']), edit))
    for start, edit in sorted(placed, reverse=True):
        del out[start:start + len(edit['body'])]
    return out, []


def apply(lines, edits):
    out = list(lines)
    missed = []
    for edit in edits:
        found = find_all(out, edit['before'])
        if len(found) != 1:
            where = 'no longer matches' if not found else 'matches ' + str(len(found)) + ' places'
            missed.append(edit['name'] + ': its anchor ' + where +
                          (' in ' + edit['function'] if edit['function'] else ''))
            continue
        start = found[0] + len(edit['before'])
        out[start:start] = edit['body']
    return out, missed


def verify():
    edits = load_edits()
    modded = read_ws(SCRIPT)
    vanilla, wrong = strip(modded, edits)
    if wrong:
        for line in wrong:
            sys.stderr.write(line + '\n')
        sys.stderr.write('tools/edits.json no longer describes the script; update it in the same commit as the change\n')
        return 1
    rebuilt, missed = apply(vanilla, edits)
    if missed:
        for line in missed:
            sys.stderr.write(line + '\n')
        return 1
    if rebuilt != modded:
        sys.stderr.write('grafting the edits back on does not reproduce the script it came from\n')
        return 1
    sys.stdout.write('the edit set rebuilds the script exactly, from a base of ' +
                     str(len(vanilla)) + ' lines\n')
    return 0


def main(argv):
    if '--verify' in argv or len(argv) == 1:
        return verify()

    if '--vanilla' in argv:
        rest = [a for a in argv[1:] if not a.startswith('--')]
        if len(rest) != 1:
            sys.stderr.write('name one file to write the base to\n')
            return 1
        vanilla, wrong = strip(read_ws(SCRIPT), load_edits())
        if wrong:
            for line in wrong:
                sys.stderr.write(line + '\n')
            return 1
        write_ws(rest[0], vanilla)
        sys.stdout.write('wrote a ' + str(len(vanilla)) + ' line base to ' + rest[0] + '\n')
        return 0

    if '--apply' in argv:
        rest = [a for a in argv[1:] if not a.startswith('--')]
        if len(rest) != 2:
            sys.stderr.write('name the base script to graft onto and the file to write\n')
            return 1
        base = read_ws(rest[0])
        grafted, missed = apply(base, load_edits())
        for line in missed:
            sys.stderr.write(line + '\n')
        if missed:
            sys.stderr.write(str(len(missed)) + ' of ' + str(len(load_edits())) +
                             ' edits could not be placed; the base has moved and they need reseating by hand\n')
            return 1
        write_ws(rest[1], grafted)
        sys.stdout.write('grafted ' + str(len(load_edits())) + ' edits onto ' + rest[0] +
                         ' and wrote ' + rest[1] + '\n')
        return 0

    sys.stderr.write('usage: graft.py [--verify] | --vanilla OUT | --apply BASE OUT\n')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
