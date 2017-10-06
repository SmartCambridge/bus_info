#!/usr/bin/env python3

"""
Walk one or more TNDS timetable files and extract ordered stop lists
based on the SequenceNo attribute TimingLink To and From entities
"""

# !!!
# BEWARE that this code uses both 'root' (of XML tree) and 'route'
# (of a bus) as the names for variables!
# !!!

import sys
import pprint
import xml.etree.ElementTree as ET

ns = {'n': 'http://www.transxchange.org.uk/'}


def display_stop(root,ref):
    """ Given a StopPointRef of an AnnotatedStopPoint, return a description """
    stop = root.find("n:StopPoints/n:AnnotatedStopPointRef[n:StopPointRef='%s']" % ref, ns)
    try:
        result = "%s %s" % (ref, stop.find('n:LocalityName', ns).text)
        if stop.find('n:Indicator', ns) is not None:
            result = "%s, %s" % (result, stop.find('n:Indicator', ns).text)
        if stop.find('n:CommonName', ns) is not None:
            result = "%s %s" % (result, stop.find('n:CommonName', ns).text)
        return result
    except AttributeError:
        return ref


def display_route(root,id):
    """ Given a ID of a Route, return a description """
    route = root.find("n:Routes/n:Route[@id='%s']" % id, ns)
    try:
      return "%s %s" % (
          id,
          route.find('n:Description', ns).text)
    except AttributeError:
        return id


def display_service(root, code):
    """ Given a ServiceCode, return a description """
    service = root.find("n:Services/n:Service[n:ServiceCode='%s']" % code, ns)
    try:
        return "%s %s" % (
            code,
            service.find('n:Description', ns).text)
    except AttributeError:
        return code


def process(root):
    """ Process one TNDS data tree """
    results = {}

    # For each service...
    for service in root.findall('n:Services/n:Service', ns):
      service_id = service.find('n:ServiceCode', ns).text

      # ... for each JourneyPattern in that service ...
      for pattern in service.findall('n:StandardService/n:JourneyPattern', ns):
          direction = pattern.find('n:Direction', ns).text
          #route_id = pattern.find('n:RouteRef', ns).text
          route_id = 'N/A'

          # ... for each Journey Pattern Timing Link in that Journey Pattern ...
          section_id = pattern.find('n:JourneyPatternSectionRefs', ns).text
          for timing_link in root.findall("n:JourneyPatternSections/n:JourneyPatternSection[@id='%s']/n:JourneyPatternTimingLink" % section_id, ns):
                  # For each of From and To
                  for point in (timing_link.find('n:From', ns), timing_link.find('n:To', ns)):
                      stop_point = point.find('n:StopPointRef', ns).text
                      sequence = point.get('SequenceNumber')
                      # Populate results structure
                      # results[service_id][route_id][direction][sequence] = stop_point
                      if service_id not in results:
                          results[service_id] = {}
                      if route_id not in results[service_id]:
                          results[service_id][route_id] = {}
                      if direction not in results[service_id][route_id]:
                          results[service_id][route_id][direction] = {}
                      if sequence not in results[service_id][route_id][direction]:
                          results[service_id][route_id][direction][sequence] = stop_point
                      # Warn if this sequence number has been used with a different stop point
                      elif results[service_id][route_id][direction][sequence] != stop_point:
                          print("Re-defined sequence number:", file=sys.stderr)
                          print("  Service: %s" % service_id, file=sys.stderr)
                          print("  Route: %s" % route_id, file=sys.stderr)
                          print("  Direction: %s" % direction, file=sys.stderr)
                          print("  Sequence: %s" % sequence, file=sys.stderr)
                          print("  Was: %s" % results[service_id][route_id][direction][sequence], file=sys.stderr)
                          print("  Is: %s" % stop_point, file=sys.stderr)

    for service in results.keys():
        print("Service: %s" % display_service(root,service))
        for route in results[service].keys():
            print("  Route: %s" % display_route(root,route))
            for direction in results[service][route]:
                print("    Direction: %s" % direction)
                for sequence in sorted(results[service][route][direction].keys(), key=int):
                    point = results[service][route][direction][sequence]
                    print("      %s: %s" % (sequence, display_stop(root, point)))


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print('Processing %s' % filename, file=sys.stderr)
        root = ET.parse(filename).getroot()
        process(root)
