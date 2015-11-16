#!/usr/bin/env python
import sys
import argparse

import xml.etree.ElementTree as ET

# tree = ET.parse('svg')
# root = tree.getroot()
# root
# root.items
# root.items()
# root.getchildren()
# root
# root.getchildren()
# root.text

def parseNode(node, callback, argument=None):
    for item in node.getchildren():
        parseNode(item, callback, argument)
    callback(node, argument)
    # print node.text


# parseNode(root)

#http://stackoverflow.com/questions/17437103/replacing-xml-element-in-python
#tree.write('output.xml')


def gettree(filename):
    tree = ET.parse(filename)
    return tree


def make_argparser():
    parser = argparse.ArgumentParser()

    # parser.add_argument('command', action='store')

    subparsers = parser.add_subparsers(help="parsers for every command")

    extract_terms = subparsers.add_parser('extract')
    extract_terms.add_argument(
        'source', help="Source file", action='store', type=str)
    extract_terms.add_argument(
        'destination', help='Destination filename', action='store', type=str)

    translate = subparsers.add_parser('translate')
    translate.add_argument(
        'source', help='Source file')
    translate.add_argument(
        'dict', help="Dictionary file")
    translate.add_argument(
        'destination', help="Destination file")

    return parser


def dict_callback(node, dictionary):
    dictionary[node.text] = ""

def translate_callback(node, dictionary):
    if not node.text: return
    key = node.text.strip()
    print "'%s' -> '%s' repr='%s'" % (node.text, key, repr(key))
    if dictionary.has_key(key):
        node.text = dictionary[key]
    elif dictionary.has_key(key.encode('utf-8')):
        node.text = dictionary[key.encode('utf-8')]


def main():

    parser = make_argparser()
    args = parser.parse_args()

    tree = gettree(args.source)
    root = tree.getroot()

    if hasattr(args, 'dict'):
        dictionary = dict()
        with open(args.dict, 'rt') as f:
            while True:
                try:
                    source = f.readline().strip()
                    destination = f.readline().strip()
                    print source, destination
                    destination = destination.decode('utf-8')

                    dictionary[source] = destination
                    if source == "":
                        break
                except Exception, e:
                    print e
                    break
        print dictionary
        print dictionary.keys()
        parseNode(root, translate_callback, dictionary)
        tree.write(args.destination)

    else:
        dict_file = open(args.destination, 'wt')
        dictionary = dict()
        parseNode(root, dict_callback, dictionary)
        for key, value in dictionary.items():
            print "[*]",key, value
            if not key:
                continue
            key = key.encode('utf-8')
            try:
                dict_file.write("%s\n%s\n" % (key, value))
            except Exception, e:
                print e
                dict_file.close()
                return
        dict_file.close()

if __name__ == "__main__":
    main()