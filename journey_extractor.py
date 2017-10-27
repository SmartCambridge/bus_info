#!/usr/bin/env python3

"""
Walk one or more TNDS timetable files and emit all its 
VehicleJourneys as CSV
"""
import os
import sys
import xml.etree.ElementTree as ET
import csv
import txc_helper

ns = {'n': 'http://www.transxchange.org.uk/'}

csv_writer = csv.writer(sys.stdout)
#csv_writer.writerow(('journey_code',...))

def process(filename):
    """ Process one TNDS data file """

    tree = ET.parse(filename).getroot()

    basename = os.path.splitext(os.path.basename(filename))[0]

    # Counting on there being only one Service, Line and Operator
    # in each file...
    service = tree.find('n:Services/n:Service', ns)
    service_code = service.find('n:ServiceCode', ns).text
    service_description = service.find('n:Description', ns).text
    line_name = service.find('n:Lines/n:Line/n:LineName', ns).text
    service_start = service.find('n:OperatingPeriod/n:StartDate', ns).text
    service_end = service.find('n:OperatingPeriod/n:EndDate', ns).text
    service_op_element = service.find('n:ServiceCode', ns)
    service_op = txc_helper.OperatingProfile.from_et(service_op_element)
    print(service_op)

    operator = tree.find('n:Operators/n:Operator', ns)
    operator_code = operator.find('n:OperatorCode', ns).text

    # For each vehicle journey...
    for journey in tree.findall('n:VehicleJourneys/n:VehicleJourney', ns):

      journey_code = journey.find('n:VehicleJourneyCode', ns).text
      departure_time = journey.find('n:DepartureTime', ns).text
      journey_pattern_ref = journey.find('n:JourneyPatternRef', ns).text
      journey_op_element = journey.find('n:OperatingProfile', ns)
      journey_op = txc_helper.OperatingProfile.from_et(journey_op_element)
      journey_op.defaults_from(service_op)
      print(journey_op)

      # Find corresponding JoureyPattern and JourneyPatternSection
      journey_pattern_section_ref = tree.find("n:Services/n:Service/n:StandardService/n:JourneyPattern[@id='%s']/n:JourneyPatternSectionRefs" % journey_pattern_ref, ns).text
      journey_pattern_section = tree.find("n:JourneyPatternSections/n:JourneyPatternSection[@id='%s']" % journey_pattern_section_ref, ns)

      # Get first and last stop
      fr = journey_pattern_section.find("n:JourneyPatternTimingLink[1]/n:From/n:StopPointRef", ns).text
      to = journey_pattern_section.find("n:JourneyPatternTimingLink[last()]/n:To/n:StopPointRef", ns).text

      csv_writer.writerow((
        service_code,
        service_description,
        service_start,
        service_end,
        line_name,
        operator_code,
        journey_code,
        departure_time,
        fr,
        to))


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print('Processing %s' % filename, file=sys.stderr)
        process(filename)
