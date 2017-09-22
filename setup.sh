#!/bin/bash

virtualenv -p python3 VE

. VE/bin/activate

pip install darkskylib influxdb
