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
    return raw.decode('utf-16').replace('\r\n', '\n').split('\n')


def write_ws(path, lines):
    io.open(path, 'wb').write(b'\xff\xfe' + '\r\n'.join(lines).encode('utf-16-le'))


def load_edits():
    return json.load(io.open(EDITS, encoding='utf-8'))


def find_all(hay, needle):
    if not needle:
        return []
    return [i for i in range(len(hay) - len(needle) + 1) if hay[i:i + len(needle)] == needle]


def swap(lines, edits, taking, putting):
    out = list(lines)
    missed = []
    for edit in edits:
        found = find_all(out, edit['before'] + edit[taking])
        if len(found) != 1:
            where = 'no longer matches' if not found else 'matches ' + str(len(found)) + ' places'
            missed.append(edit['name'] + ': its anchor ' + where +
                          (' in ' + edit['function'] if edit['function'] else ''))
            continue
        start = found[0] + len(edit['before'])
        out[start:start + len(edit[taking])] = edit[putting]
    return out, missed


def apply(base, edits):
    return swap(base, edits, 'remove', 'insert')


def strip(modded, edits):
    return swap(modded, edits, 'insert', 'remove')


def verify():
    edits = load_edits()
    modded = read_ws(SCRIPT)
    base, wrong = strip(modded, edits)
    if wrong:
        for line in wrong:
            sys.stderr.write(line + '\n')
        sys.stderr.write('tools/edits.json no longer describes the script; update it in the same commit as the change\n')
        return 1
    rebuilt, missed = apply(base, edits)
    if missed:
        for line in missed:
            sys.stderr.write(line + '\n')
        return 1
    if rebuilt != modded:
        sys.stderr.write('grafting the edits back on does not reproduce the script they came from\n')
        return 1
    sys.stdout.write('the edit set turns a ' + str(len(base)) + ' line base into the shipped script exactly, '
                     'across ' + str(len(edits)) + ' edits\n')
    return 0


def main(argv):
    rest = [a for a in argv[1:] if not a.startswith('--')]

    if '--vanilla' in argv:
        if len(rest) != 1:
            sys.stderr.write('name one file to write the base to\n')
            return 1
        base, wrong = strip(read_ws(SCRIPT), load_edits())
        if wrong:
            for line in wrong:
                sys.stderr.write(line + '\n')
            return 1
        write_ws(rest[0], base)
        sys.stdout.write('wrote a ' + str(len(base)) + ' line base to ' + rest[0] + '\n')
        return 0

    if '--apply' in argv:
        if len(rest) != 2:
            sys.stderr.write('name the base script to graft onto and the file to write\n')
            return 1
        edits = load_edits()
        grafted, missed = apply(read_ws(rest[0]), edits)
        for line in missed:
            sys.stderr.write(line + '\n')
        if missed:
            sys.stderr.write(str(len(missed)) + ' of ' + str(len(edits)) +
                             ' edits could not be placed; the base has moved and they need reseating by hand\n')
            return 1
        write_ws(rest[1], grafted)
        sys.stdout.write('grafted ' + str(len(edits)) + ' edits onto ' + rest[0] +
                         ' and wrote ' + rest[1] + '\n')
        return 0

    if '--verify' in argv or len(argv) == 1:
        return verify()

    sys.stderr.write('usage: graft.py [--verify] | --vanilla OUT | --apply BASE OUT\n')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
