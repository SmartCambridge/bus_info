#!/usr/bin/env python3

"""
Walk one or more TNDS timetable files and emit their contained
routes as dot files
"""
import os
import sys
import xml.etree.ElementTree as ET

ns = {'n': 'http://www.transxchange.org.uk/'}


def process(filename):
    """ Process one TNDS data file """

    directions = set()

    tree = ET.parse(filename).getroot()

    basename = os.path.splitext(os.path.basename(filename))[0]

    # Counting on there being only one Service, Line and Operator
    # in each file...

    service_description = tree.find('n:Services/n:Service/n:Description', ns).text
    line_name = tree.find('n:Services/n:Service/n:Lines/n:Line/n:LineName', ns).text

    print("<h2>%s - %s (%s)</h2>" % (line_name, service_description, basename))
    print("<ul>")

    # For each route...
    for route in tree.findall('n:Routes/n:Route', ns):
      route_section_ref = route.find('n:RouteSectionRef', ns).text

      # ...for each RouteLink in that RouteSection for that Route
      route_section = tree.find("n:RouteSections/n:RouteSection[@id='%s']" % route_section_ref, ns)
      for link in route_section.findall('n:RouteLink', ns):
        directions.add(link.find('n:Direction', ns).text)

    # Draw each graph (i.e. for each identified direction)
    for direction in sorted(directions):
      print("<li><a href=%s-%s.pdf>%s</a></li>" % (basename, direction, direction))

    print("</ul>")

if __name__ == '__main__':
    print('''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
  <head>
    <title>Bus line diagrams</title>
    <meta name = "viewport" content = "width = 600" />
    <link rel="stylesheet" href="../../jw35-default.css"
          type="text/css" media="all" />
  </head>

  <body>

    <h1>Bus Line diagrams</h1>

    <p>Automatically-generated diagrams of East Anglia bus lines derived 
    from the <a href="http://www.travelinedata.org.uk/">TNDS data made 
    available by TravelLine</a>.</p>
''')

    for filename in sys.argv[1:]:
        process(filename)

    print('''
  </body>

</html>
''')