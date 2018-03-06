#!/usr/bin/env python3


'''
Given a set of directories, one for each TNDS region and containing
the unpacked XML from the corresponding zip file, extract the origin
and destination stop of every route, look up their position in NAPTAN
and emit the result as a JavaScript data file for display on a map.
'''

import os
import sys
import xml.etree.ElementTree as ET
import json
import psycopg2

ns = {'n': 'http://www.transxchange.org.uk/'}

all_results = {}

# Assumes a local Postgresql database 'icp' containing a 'naptan' table
conn = psycopg2.connect("dbname='icp' host='localhost'")
cur = conn.cursor()

def process_file(filename, codes):
    ''' Process one TNDS data file '''

    tree = ET.parse(filename).getroot()

    # Counting on there being only one Service, Line and Operator
    # in each file...

    for route in tree.findall('n:Routes/n:Route', ns):
        route_section_ref = route.find('n:RouteSectionRef', ns).text
        route_section = tree.find("n:RouteSections/n:RouteSection[@id='%s']" % route_section_ref, ns)
        first_stop = route_section.find("n:RouteLink[1]/n:From/n:StopPointRef" , ns).text
        last_stop = route_section.find("n:RouteLink[last()]/n:To/n:StopPointRef" , ns).text
        #print(first_stop, last_stop)
        codes.add(first_stop)
        codes.add(last_stop)

    # Rather than emitting route origin/destination, this emits every
    # stop. It works, but the redulting amount of data is too big
    # for LEaflet to handle without going really slowly
    #for stop in tree.findall('n:StopPoints/n:AnnotatedStopPointRef/n:StopPointRef', ns):
    #    codes.add(stop.text)


def process_region(base, region, results):
    ''' Process all the files for one region'''

    codes = set()
    for file in os.listdir(os.path.join(base, region)):
      filename = os.path.join(base, region, os.fsdecode(file))
      if not filename.endswith('.xml'):
          continue
      #print('Processing %s' % filename, file=sys.stderr)
      process_file(filename, codes)

    query = "select Latitude, Longitude from naptan where ATCOCode = %s"
    for code in codes:
      #print(code, file=sys.stderr)
      cur.execute(query, (code,))
      row = cur.fetchone()
      if row:
        results.append(row)
      else:
        print('Failed to locate %s' % code, file=sys.stderr)


def process():
    '''
    Process a directory full of directories, one for each region. Note
    that region names are hard-coded and will need to be updated if the
    files distributed by TransportDirect change
    '''

    all_results = {}

    base = sys.argv[1]
    for region in ('EA', 'EM', 'L', 'NCSD', 'NE', 'NW', 'S', 'SE', 'SW', 'W', 'WM', 'Y'):
      #for region in ('EA', ):
      print("Region %s" % region, file=sys.stderr)
      results = []
      process_region(base, region, results)
      all_results[region] = results

    #print(all_results)

    print('var regions =')
    print(json.dumps(all_results, indent=2))


if __name__ == '__main__':
    process()

