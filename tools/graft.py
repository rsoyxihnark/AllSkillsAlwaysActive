import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EDITS = os.path.join(HERE, 'edits.json')
MOD = os.path.join(ROOT, 'modAllSkillsAlwaysActive')


def read_ws(path):
    raw = io.open(path, 'rb').read()
    if not raw.startswith(b'\xff\xfe'):
        raise ValueError(path + ' does not start with a UTF-16 little-endian mark')
    return raw.decode('utf-16').replace('\r\n', '\n').split('\n')


def write_ws(path, lines):
    folder = os.path.dirname(path)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)
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


def check():
    wrong = []
    for entry in load_edits():
        shipped = os.path.join(MOD, entry['file'])
        if not os.path.isfile(shipped):
            wrong.append(entry['file'] + ' is described by tools/edits.json but the mod does not ship it')
            continue
        modded = read_ws(shipped)
        base, undescribed = strip(modded, entry['edits'])
        if undescribed:
            wrong.extend(entry['file'] + ': ' + line for line in undescribed)
            wrong.append('tools/edits.json no longer describes ' + entry['file'] +
                         '; update it in the same commit as the change')
            continue
        rebuilt, missed = apply(base, entry['edits'])
        wrong.extend(entry['file'] + ': ' + line for line in missed)
        if not missed and rebuilt != modded:
            wrong.append('grafting the edits onto the base does not reproduce ' + entry['file'])
    return wrong


def main(argv):
    rest = [a for a in argv[1:] if not a.startswith('--')]
    entries = load_edits()

    if '--vanilla' in argv:
        if len(rest) != 1:
            sys.stderr.write('name the folder to write the base scripts into\n')
            return 1
        for entry in entries:
            base, wrong = strip(read_ws(os.path.join(MOD, entry['file'])), entry['edits'])
            if wrong:
                for line in wrong:
                    sys.stderr.write(entry['file'] + ': ' + line + '\n')
                return 1
            write_ws(os.path.join(rest[0], entry['base']), base)
            sys.stdout.write('wrote a ' + str(len(base)) + ' line base to ' +
                             os.path.join(rest[0], entry['base']) + '\n')
        return 0

    if '--apply' in argv:
        if len(rest) != 2:
            sys.stderr.write('name the folder of base scripts to graft onto and the folder to write\n')
            return 1
        failed = False
        for entry in entries:
            source = os.path.join(rest[0], entry['base'])
            if not os.path.isfile(source):
                sys.stderr.write(entry['base'] + ' is not in ' + rest[0] + '\n')
                failed = True
                continue
            grafted, missed = apply(read_ws(source), entry['edits'])
            for line in missed:
                sys.stderr.write(entry['file'] + ': ' + line + '\n')
            if missed:
                sys.stderr.write(str(len(missed)) + ' of ' + str(len(entry['edits'])) +
                                 ' edits could not be placed in ' + entry['file'] +
                                 '; the base has moved and they need reseating by hand\n')
                failed = True
                continue
            write_ws(os.path.join(rest[1], entry['file']), grafted)
            sys.stdout.write('grafted ' + str(len(entry['edits'])) + ' edits into ' + entry['file'] + '\n')
        return 1 if failed else 0

    if '--verify' in argv or len(argv) == 1:
        wrong = check()
        for line in wrong:
            sys.stderr.write(line + '\n')
        if wrong:
            return 1
        total = sum(len(e['edits']) for e in entries)
        sys.stdout.write('the edit set rebuilds ' + str(len(entries)) + ' shipped scripts exactly, across ' +
                         str(total) + ' edits\n')
        return 0

    sys.stderr.write('usage: graft.py [--verify] | --vanilla OUTDIR | --apply BASEDIR OUTDIR\n')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
