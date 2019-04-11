#!/bin/bash

echo "Enter the ICAO to filter"

read icao

echo "$(date '+%s')"

./dump1090 --net | tee logs/raw/$(date '+%s').log | /usr/bin/python3 adsb_reader.py "$icao" | tee logs/parsed/$(date '+%s').log
