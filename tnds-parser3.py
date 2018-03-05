#!/usr/bin/env python3

"""
Walk one or more TNDS timetable files and emit their contained
routes as dot files
"""
import os
import sys
import xml.etree.ElementTree as ET
from graphviz import Digraph

ns = {'n': 'http://www.transxchange.org.uk/'}


def display_stop(tree,ref):
    """ Given a StopPointRef of an AnnotatedStopPoint, return a description """
    stop = tree.find("n:StopPoints/n:AnnotatedStopPointRef[n:StopPointRef='%s']" % ref, ns)
    result = r'%s\n' % ref
    if stop.find('n:Indicator', ns) is not None:
        result = "%s%s" % (result, stop.find('n:Indicator', ns).text)
    if stop.find('n:CommonName', ns) is not None:
        result = "%s %s" % (result, stop.find('n:CommonName', ns).text)
    if stop.find('n:LocalityName', ns) is not None:
        result = "%s, %s" % (result, stop.find('n:LocalityName', ns).text)
    return result


def process(filename):
    """ Process one TNDS data file """

    tree = ET.parse(filename).getroot()

    basename = os.path.splitext(os.path.basename(filename))[0]

    graph_attrs = {'fontname': 'Helvetica'}
    node_attrs = {'shape': 'box'}
    edge_attrs = {'fontsize': '9'}
    colors = ['/dark28/1', '/dark28/2', '/dark28/3', '/dark28/4',
              '/dark28/5', '/dark28/6', '/dark28/7', '/dark28/8']

    graphs = {}
    serial_counter = {}
    route_serial = {}

    # Counting on there being only one Service, Line and Operator
    # in each file...

    service_description = tree.find('n:Services/n:Service/n:Description', ns).text
    operator_name = tree.find('n:Operators/n:Operator/n:OperatorShortName', ns).text
    line_name = tree.find('n:Services/n:Service/n:Lines/n:Line/n:LineName', ns).text

    # For each route...
    for route in tree.findall('n:Routes/n:Route', ns):
      route_id = route.get('id')
      private_code = route.find('n:PrivateCode', ns).text
      route_section_ref = route.find('n:RouteSectionRef', ns).text

      # ...for each RouteLink in that RouteSection for that Route
      route_section = tree.find("n:RouteSections/n:RouteSection[@id='%s']" % route_section_ref, ns)
      first_link_id = route_section.find("n:RouteLink[1]" , ns).get('id')
      last_link_id = route_section.find("n:RouteLink[last()]" , ns).get('id')
      for link in route_section.findall('n:RouteLink', ns):

        from_stop = link.find('n:From/n:StopPointRef', ns).text
        to_stop = link.find('n:To/n:StopPointRef', ns).text
        direction = link.find('n:Direction', ns).text

        # Make a new graph if we haven't seen this direction before
        # (1 graph per direction else it just gets too confusing)
        if direction not in graphs:
          graphs[direction] = Digraph(graph_attr=graph_attrs,
            node_attr=node_attrs,
            edge_attr=edge_attrs,
            name='%s %s %s' % (line_name, direction, service_description))
          graphs[direction].attr(label=r'\n%s %s %s\n%s\n%s' % (operator_name, line_name, direction, service_description, basename))
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
        if link.get('id') == first_link_id:
          label = "%d (first)" % (route_no + 1)
        elif link.get('id') == last_link_id:
          label = "%d (last)" % (route_no + 1)

        graphs[direction].node(from_stop,display_stop(tree,from_stop))
        graphs[direction].node(to_stop,display_stop(tree,to_stop))
        graphs[direction].edge(from_stop, to_stop, color=route_color, label=label)

    # Draw each graph (i.e. for each identified direction)
    for direction in graphs:
      print(graphs[direction].render('%s-%s' % (basename,direction), cleanup=True))


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print('Processing %s' % filename, file=sys.stderr)
        process(filename)
