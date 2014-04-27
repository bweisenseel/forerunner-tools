#!/bin/bash

for fname in $*
do
    fname=`basename ${fname} .TCX`
    echo "Processing ${fname}.TCX"
    gpsbabel -i gtrnctr,sport=other -f ${fname}.TCX -o kml -F ${fname}.kml || exit 2
    zip ${fname}.kmz ${fname}.kml || exit 3
    rm ${fname}.kml || echo "Failed to remove file ${fname}.kml"
    /users/bweisenseel/Documents/personal/forerunner-tools/examples/chart_speed.py ${fname}.TCX ${fname}_spd.png || echo "Failed to chart speed from ${fname}.TCX"
    /users/bweisenseel/Documents/personal/forerunner-tools/examples/chart_altitude.py ${fname}.TCX ${fname}_alt.png || echo "Failed to chart altitude from ${fname}.TCX"
    /users/bweisenseel/Documents/personal/forerunner-tools/examples/chart_heartrate.py ${fname}.TCX ${fname}_hr.png || echo "Failed to chart heart rate from ${fname}.TCX"
done
