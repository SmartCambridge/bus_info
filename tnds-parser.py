#!/usr/bin/env python3

import xmltodict
import sys
import collections
import pprint

stop_points = {}
routes = {}
journey_pattern_sections = {}

def display_stop(ref):
    stop = stop_points[ref]
    return "%s %s, %s %s" % (ref, stop['LocalityName'], stop['Indicator'], stop['CommonName'])

def display_route(ref):
    route = routes[ref]
    return "%s %s" % (ref, route['Description'])

def as_list(thing):
    if isinstance(thing, collections.Sequence) and not isinstance(thing, str):
        return thing
    return [thing]

for filename in sys.argv[1:]:
    with open(filename, 'rb') as file:
        content = xmltodict.parse(file)
 
        sps = as_list(content['TransXChange']['StopPoints']['AnnotatedStopPointRef'])
        for sp in sps:
            stop_points[sp['StopPointRef']] = sp
        pprint.pprint(stop_points)

        rs = as_list(content['TransXChange']['Routes']['Route'])
        for r in rs:
            routes[r['@id']] = r
        pprint.pprint(routes)

        jpss = as_list(content['TransXChange']['JourneyPatternSections']['JourneyPatternSection'])
        for jps in jpss:
            journey_pattern_sections[jps['@id']] = as_list(jps['JourneyPatternTimingLink'])
        pprint.pprint(jps)

        #pprint.pprint(content)
        jps = as_list(content['TransXChange']['Services']['Service']['StandardService']['JourneyPattern'])
        for jp in jps:

            print("Journey Pattern:", jp['@id'])
            print("Direction: ", jp['Direction'])
            print("Route: ", display_route(jp['RouteRef']))
            print("JourneyPatternSection: ", jp['JourneyPatternSectionRefs'])
            print()
            for jptl in journey_pattern_sections[jp['JourneyPatternSectionRefs']]:
                fr = jptl['From']
                to = jptl['To']
                print('From: %2s %16s %s %s' % (fr['@SequenceNumber'], fr['Activity'], fr['TimingStatus'], display_stop(fr['StopPointRef'])))
                print('To:   %2s %16s %s %s' % (to['@SequenceNumber'], to['Activity'], to['TimingStatus'], display_stop(to['StopPointRef'])))
            print()
            print()
