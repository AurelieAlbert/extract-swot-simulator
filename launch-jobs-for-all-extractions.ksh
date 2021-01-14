#!/bin/bash                


for region in MEDWEST NANFL; do
    for phase in science_phase calval_phase; do
        cp tmp-job-launch-extract.ksh job-launch-extract-${region}-${phase}-karin.ksh
        sed -i "s/REG/${region}/g" job-launch-extract-${region}-${phase}-karin.ksh
        sed -i "s/PHASE/${phase}/g" job-launch-extract-${region}-${phase}-karin.ksh
        sed -i "s/DATA/karin/g" job-launch-extract-${region}-${phase}-karin.ksh
        chmod +x job-launch-extract-${region}-${phase}-karin.ksh
        qsub job-launch-extract-${region}-${phase}-karin.ksh
    done
done