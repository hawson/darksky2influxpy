# darksky2influxpy
Pull data from darksky.net, and put it into influxdb, suitable for later
pulling and graphing in Grafana, etc.

    https://github.com/hawson/darksky2influxpy

The project https://github.com/SvenSommer/darksky2influxdb, does what
I'd like, but is written in nodejs.  I'm wanted something in Python,
and nothing fit the bill.  So all credit to that project for inspiration.


Setup is mostly simple, when run from a virtualene.  There are two required modules:
    darkskylib
    influxdb

The super-simple "setup.sh" script should install these for you (it
makes an virtualenv, and install the two modules).

You also need an API key from darksky.net:  https://darksky.net/dev

The API key you recieve should be placed in a file "key.txt". Just the
key on a single line is sufficient.

Both the current weather, and 48-hour forecast at that point in time
are collected and put into sets of measurements in influxdb.

Also edit the "config" dictionary in dark_import.py to make a connection
to your local influxdb install.  The database will need to be configured
ahead of time, of course.


