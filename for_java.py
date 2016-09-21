#!/usr/bin/env python3
# coding: utf8

import json


def convert_array(name, array, indent_size, type_name, item_format):
    output = []
    indent = ' ' * indent_size
    output.append('%sprivate static final %s[] %s = new %s[]{'
                  % (indent, type_name, name, type_name))
    indent_size += 4
    indent = ' ' * indent_size
    for idx, item in enumerate(array):
        if idx & 15 == 0:
            if idx == 0:
                output.append('\n')
            else:
                output.append(',\n')
            output.append(indent)
        else:
            output.append(', ')
        output.append(item_format % item)
    output.append('};\n')
    return output


def to_java():
    with open('pinyin.org', 'rb') as ifile:
        lines = ifile.read().strip().decode('utf8').splitlines()

    pairs = sorted([tuple(reversed(line.split())) for line in lines])

    output = ['public PinyinUtil {\n']
    indent_size = 4
    output.extend(convert_array(
        'chars', [ord(pair[0]) for pair in pairs], indent_size, 'int', '%d'))

    phonetic_indice = []
    phonetics = []
    for _, phonetic in pairs:
        try:
            index = phonetics.index(phonetic)
        except ValueError:
            index = len(phonetics)
            phonetics.append(phonetic)
        phonetic_indice.append(index)

    output.extend(convert_array('phonetic_indice', phonetic_indice, indent_size, 'short', '%d'))

    output.extend(convert_array('phonetics', phonetics, indent_size, 'String', '"%s"'))

    output.append('\n}')
    print ''.join(output)
    # ok, this is not gonna work since java have a 64k limit


def to_json():
    with open('pinyin.org', 'rb') as ifile:
        lines = ifile.read().strip().decode('utf8').splitlines()

    pairs = sorted([tuple(reversed(line.split())) for line in lines])

    data = {'chars': [ord(pair[0]) for pair in pairs]}

    phonetic_indice = []
    phonetics = []
    for _, phonetic in pairs:
        try:
            index = phonetics.index(phonetic)
        except ValueError:
            index = len(phonetics)
            phonetics.append(phonetic)
        phonetic_indice.append(index)

    data['phonetic_indice'] = phonetic_indice
    data['phonetics'] = phonetics
    print json.dumps(data, separators=(',', ':'))


def main():
    to_json()


if __name__ == '__main__':
    main()
