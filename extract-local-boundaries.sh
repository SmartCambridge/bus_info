#!/bin/bash

# Download a copy of the digital vector boundaries for Counties and
# Unitary Authorities in England and Wales in GeoJSON, and extract the
# Cambridgeshire # (objectid == 127) and surrounding authority Boundaries

set -e

# From https://data.gov.uk/dataset/11302ddc-65bc-4a8f-96a9-af5c456e442c/counties-and-unitary-authorities-december-2016-full-clipped-boundaries-in-england-and-wales
src='http://geoportal1-ons.opendata.arcgis.com/datasets/687f346f5023410ba86615655ff33ca9_3.geojson'

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
