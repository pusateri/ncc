# Nutanix Cluster Check (NCC) log parser

This package is written in Python version 3 and expects to have python3 binary in the path.

    usage: ncc_parse [-c <case number>] [-f text|html] <logfile>
    
## Development installation

This will link to the version in the current directory and allow you to update it by simply refreshing from github.

    python3 setup.py develop


## Normal installation

This will copy the current version into a system directory and freeze at that version until 'install' is run again.

    python3 setup.py install