#!/bin/bash

# Download a copy of the digital vector boundaries for Counties and
# Unitary Authorities in England and Wales in GeoJSON, and extract the
# Cambridgeshire # (objectid == 127) and surrounding authority Boundaries

set -e

# From https://data.gov.uk/dataset/cd97a8df-e2fe-4f3d-a60f-1f871a317d31/counties-and-unitary-authorities-december-2016-full-extent-boundaries-in-england-and-wales
src='http://geoportal1-ons.opendata.arcgis.com/datasets/687f346f5023410ba86615655ff33ca9_1.geojson'

script='{ features:
    [ .features[] |
        select(
            .properties.objectid == 127 or
            .properties.objectid ==  31 or
            .properties.objectid == 148 or
            .properties.objectid == 141 or
            .properties.objectid == 133 or
            .properties.objectid ==  55 or
            .properties.objectid ==  54 or
            .properties.objectid == 136 or
            .properties.objectid == 142 or
            .properties.objectid ==  17 or
            .properties.objectid == 140
        )
    ]
}'

dest='cambridgeshire_and_surrounding.geojson'

curl "${src}" | jq "${script}" > "${dest}"
