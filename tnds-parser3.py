#!/usr/bin/env python3

"""
Walk one or more TNDS timetable files and emit their contained
routes as dot files
"""
import os
import sys
import xml.etree.ElementTree as ET
from graphviz import Digraph
import html

ns = {'n': 'http://www.transxchange.org.uk/'}


def display_stop(tree,ref):
    """ Given a StopPointRef of an AnnotatedStopPoint, return a description """
    stop = tree.find("n:StopPoints/n:AnnotatedStopPointRef[n:StopPointRef='%s']" % ref, ns)
    try:
        ref = html.escape(ref)
        indicator = html.escape(stop.find('n:Indicator', ns).text)
        cn = html.escape(stop.find('n:CommonName', ns).text)
        locality = html.escape(stop.find('n:LocalityName', ns).text)
        result = "<b>%s</b>" % ref
        if indicator or cn:
            result = "%s<br/>" % result
            if indicator:
                result = "%s%s" % (result, indicator)
            if cn:
                result = "%s %s" % (result, cn)
        result = "< %s<br/>%s >" % (result,locality)
        return result
    except AttributeError:
        return ref


def process(filename):
    """ Process one TNDS data file """

    tree = ET.parse(filename).getroot()

    basename = os.path.splitext(os.path.basename(filename))[0]

    graph_attrs = {'fontname': 'Helvetica'}
    node_attrs = {'shape': 'box'}
    edge_attrs = {}
    colors = ['/set19/1', '/set19/2', '/set19/3', '/set19/4', '/set19/5',
              '/set19/6', '/set19/7', '/set19/8', '/set19/9']

    graphs = {}
    route_ctr = 0

    # For each route...
    for route in tree.findall('n:Routes/n:Route', ns):
      private_code = route.find('n:PrivateCode', ns).text
      route_section_ref = route.find('n:RouteSectionRef', ns).text

      # Choose a colour for this route
      route_color = colors[route_ctr % len(colors)]
      route_ctr += 1;

      # ...for each RouteLink in that RouteSection for that Route
      route_section = tree.find("n:RouteSections/n:RouteSection[@id='%s']" % route_section_ref, ns)
      for link in route_section.findall('n:RouteLink', ns):

        from_stop = link.find('n:From/n:StopPointRef', ns).text
        to_stop = link.find('n:To/n:StopPointRef', ns).text
        direction = link.find('n:Direction', ns).text

        # Make a new graph if we haven't seen this direction before
        # (1 graph per direction else it just gets too confusing)
        if direction not in graphs:
          graphs[direction] = Digraph(graph_attr=graph_attrs,
            node_attr=node_attrs,
            edge_attr=edge_attrs)
          graphs[direction].attr(label='\\n\\n%s %s' % (basename,direction))
          graphs[direction].attr(fontsize='20')

        graphs[direction].node(from_stop,display_stop(tree,from_stop))
        graphs[direction].node(to_stop,display_stop(tree,to_stop))
        graphs[direction].edge(from_stop, to_stop, color=route_color)

    for direction in graphs:
      print(graphs[direction].render('%s-%s' % (basename,direction), cleanup=True))


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print('Processing %s' % filename, file=sys.stderr)
        process(filename)
