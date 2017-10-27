#!/usr/bin/env python3

import os
import sys
import xml.etree.ElementTree as ET

ns = {'n': 'http://www.transxchange.org.uk/'}


def process(filename):
    """ Process one TNDS data file """

    tree = ET.parse(filename).getroot()

    # Counting on there being only one Service, Line and Operator
    # in each file...
    code = tree.find('n:Services/n:Service/n:ServiceCode', ns).text
    description = tree.find('n:Services/n:Service/n:Description', ns).text
    line_id = tree.find('n:Services/n:Service/n:Lines/n:Line', ns).get('id')
    line_name = tree.find('n:Services/n:Service/n:Lines/n:Line/n:LineName', ns).text
    period = tree.find('n:Services/n:Service/n:OperatingPeriod', ns)
    start = period.find('n:StartDate', ns).text
    end = period.find('n:EndDate', ns).text

    if start != '2017-10-10' or end != '2018-04-13':
      print(start, end, code, line_id, line_name)


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        #print('Processing %s' % filename, file=sys.stderr)
        process(filename)
