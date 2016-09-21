# coding: utf8

'''
getting the most occured pinyin of a chinese char in all words,
set it as the default (and only ony) pinyin and prints
'''

# pylint: disable=C0103


def load_py(mapping_file):
    with open(mapping_file, 'r') as f:
        d = {}
        for line in f.read().splitlines():
            if not line:
                continue
            py, ch = line.decode('utf8').split()
            if ch in d:
                d[ch].add(py)
            else:
                d[ch] = set([py])
    return d


def load_phrase(mapping_file):
    with open(mapping_file, 'r') as f:
        d = {}
        for line in f.read().splitlines():
            if not line:
                continue
            py, ch = line.split()
            d[ch.decode('utf8')] = tuple(py.split('\''))
    return d


def gen_occurance(word_pys):
    counts = {}
    for word, pys in word_pys.items():
        for ch, py in zip(word, pys):
            if ch in counts:
                if py in counts[ch]:
                    counts[ch][py] += 1
                else:
                    counts[ch][py] = 1
            else:
                counts[ch] = {py: 1}
    return counts


def main():
    ch2pys = load_py('data/gbkpy.org')
    phrase2py = load_phrase('data/pyPhrase.org')
    py_counts = gen_occurance(phrase2py)
    new_ch2py = {}
    for ch, pys in ch2pys.items():
        if len(pys) == 1:
            new_ch2py[ch] = pys.pop()
            continue
        if ch not in py_counts:
            new_ch2py[ch] = pys.pop()
            continue
        max_count = 0
        for py in pys:
            count = py_counts[ch].get(py, 0)
            if count > max_count:
                new_ch2py[ch] = py
                max_count = count
    for ch in sorted(new_ch2py, key=lambda ch: (new_ch2py[ch], ch)):
        print ('%s %s' % (new_ch2py[ch], ch)).encode('utf8')


if __name__ == '__main__':
    main()
