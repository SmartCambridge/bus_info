#!/usr/bin/env python3

"""

"""
import os
import sys
import xml.etree.ElementTree as ET
import re

ns = {'n': 'http://www.transxchange.org.uk/'}


def process_node(node, results):

    if node.tag not in results:
      results[node.tag] = {'_': set()}
    for attrib in node.attrib:
      results[node.tag]['_'].add(attrib)
    for child in node:
      process_node(child, results[node.tag])


def print_results(result, indent):

    for key in result:
      if key == '_':
        continue
      printstring = re.sub(r'\{.*/}','',key)
      print("%s%s" % (indent, printstring), end='')
      for attrib in result[key]['_']:
        print(" @%s" % attrib, end='')
      print()  
      print_results(result[key], indent + '    ')


if __name__ == '__main__':
    results = {}
    base = sys.argv[1]
    for file in os.listdir(os.fsencode(base)):
        filename = os.path.join(base, os.fsdecode(file))
        if filename.endswith(".xml"):
            try:
                print("Processing %s" % filename, file=sys.stderr)
                tree = ET.parse(filename).getroot()
                process_node(tree, results)
            except xml.etree.ElementTree.ParseError as e:
                print(e)
    print_results(results, '')