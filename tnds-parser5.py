#!/usr/bin/env python3

"""
Walk one or more TNDS timetable files and emit a summary of
their contained routes just showing stops at the route start
end stops as dot files
"""

import os
import sys
import xml.etree.ElementTree as ET
from graphviz import Digraph
from datetime import datetime

ns = {'n': 'http://www.transxchange.org.uk/'}


def display_stop(tree, ref):
    """ Given a StopPointRef of an AnnotatedStopPoint, return a description """
    stop = tree.find(
      "n:StopPoints/n:AnnotatedStopPointRef[n:StopPointRef='%s']" % ref, ns
    )
    result = r'%s\n' % ref
    if stop.find('n:Indicator', ns) is not None:
        result = "%s%s" % (result, stop.find('n:Indicator', ns).text)
    if stop.find('n:CommonName', ns) is not None:
        result = "%s %s" % (result, stop.find('n:CommonName', ns).text)
    if stop.find('n:LocalityName', ns) is not None:
        result = "%s, %s" % (result, stop.find('n:LocalityName', ns).text)
    return result


def process(filename, index):
    """ Process one TNDS data file """

    tree = ET.parse(filename).getroot()

    basename = os.path.splitext(os.path.basename(filename))[0]

    graph_attrs = {'fontname': 'Helvetica'}
    node_attrs = {'shape': 'box', 'fontname': 'Helvetica'}
    edge_attrs = {'fontsize': '9', 'fontname': 'Helvetica'}
    colors = ['/dark28/1', '/dark28/2', '/dark28/3', '/dark28/4',
              '/dark28/5', '/dark28/6', '/dark28/7', '/dark28/8']

    graphs = {}
    serial_counter = {}
    route_serial = {}

    # Counting on there being only one Service, Line and Operator
    # in each file...

    service_description = tree.find(
      'n:Services/n:Service/n:Description', ns
    ).text
    operator_name = tree.find(
      'n:Operators/n:Operator/n:OperatorShortName', ns
    ).text
    line_name = tree.find(
      'n:Services/n:Service/n:Lines/n:Line/n:LineName', ns
    ).text

    print("<h2>%s - %s (%s)</h2>" %
          (line_name, service_description, basename), file=index)
    print("<ul>", file=index)

    # First, for each route find the route section start/end stop ids...
    terminal_stops = set()
    for route in tree.findall('n:Routes/n:Route', ns):
        route_id = route.get('id')
        route_section_ref = route.find('n:RouteSectionRef', ns).text

        # ...for each RouteLink in that RouteSection for that Route
        route_section = tree.find(
          "n:RouteSections/n:RouteSection[@id='%s']" % route_section_ref, ns
        )
        terminal_stops.add(route_section.find("n:RouteLink[1]/n:From/n:StopPointRef", ns).text)
        terminal_stops.add(route_section.find("n:RouteLink[last()]/n:To/n:StopPointRef", ns).text)

    # Then for each route...
    for route in tree.findall('n:Routes/n:Route', ns):
        route_id = route.get('id')
        route_section_ref = route.find('n:RouteSectionRef', ns).text

        # ...for each RouteLink in that RouteSection for that Route
        route_section = tree.find(
          "n:RouteSections/n:RouteSection[@id='%s']" % route_section_ref, ns
        )

        first_link_stop = route_section.find("n:RouteLink[1]/n:From/n:StopPointRef", ns).text
        last_link_stop = route_section.find("n:RouteLink[last()]/n:To/n:StopPointRef", ns).text

        first = None

        for link in route_section.findall('n:RouteLink', ns):

            from_stop = link.find('n:From/n:StopPointRef', ns).text
            to_stop = link.find('n:To/n:StopPointRef', ns).text
            direction = link.find('n:Direction', ns).text

            if first == None:
                first = from_stop

            if to_stop not in terminal_stops:
                continue

            # Make a new graph if we haven't seen this direction before
            # (1 graph per direction else it just gets too confusing)
            if direction not in graphs:
                graphs[direction] = Digraph(graph_attr=graph_attrs,
                                            node_attr=node_attrs,
                                            edge_attr=edge_attrs,
                                            name='%s %s %s' %
                                            (line_name, direction,
                                             service_description))
                graphs[direction].attr(label=r'\n%s %s %s\n%s\n%s' %
                                       (operator_name, line_name, direction,
                                        service_description, basename))
                graphs[direction].attr(fontsize='20')

            # Form a sequence number for this route in this direction
            if direction not in route_serial:
                route_serial[direction] = {}
            if route_id not in route_serial[direction]:
                if direction not in serial_counter:
                    serial_counter[direction] = 0
                else:
                    serial_counter[direction] += 1
                route_serial[direction][route_id] = serial_counter[direction]
            route_no = route_serial[direction][route_id]

            route_color = colors[route_no % len(colors)]

            # Label first and last links differently
            label = str(route_no + 1)
            if first == first_link_stop and to_stop == last_link_stop:
                label = ('<<font face="helvetica-bold">%d (only)</font>>' %
                         (route_no + 1))
            elif first == first_link_stop:
                label = ('<<font face="helvetica-bold">%d (first)</font>>' %
                         (route_no + 1))
            elif to_stop == last_link_stop:
                label = ('<<font face="helvetica-bold">%d (last)</font>>' %
                         (route_no + 1))

            graphs[direction].node(first,
                                   display_stop(tree, first))
            graphs[direction].node(to_stop,
                                   display_stop(tree, to_stop))
            graphs[direction].edge(first,
                                   to_stop,
                                   color=route_color,
                                   label=label)

            first = to_stop;

    # Draw each graph (i.e. for each identified direction)
    for direction in sorted(graphs):
        # text = '<<table>'
        # for id, counter in route_serial[direction].items():
        #   text = '%s<tr><td>%s</td><td>%s</td></tr>' % (text, counter, id)
        # text = text + '</table>>'
        # graphs[direction].node('key', text)
        print(graphs[direction].render(
          '%s-%s' % (basename, direction), cleanup=True
        ))
        print("<li><a href=%s-%s.pdf>%s</a></li>" %
              (basename, direction, direction), file=index)

    print("</ul>", file=index)


if __name__ == '__main__':

    index = open('index.html', 'w')

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
''', file=index)

    print("<p>Last updated %s</p>" % (datetime.now()), file=index)

    for filename in sys.argv[1:]:
        print('Processing %s' % filename, file=sys.stderr)
        process(filename, index)

    print('''
  </body>

</html>
''', file=index)
