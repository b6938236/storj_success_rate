# Success Rate Tool

This script calculates success rates for audits, downloads, uploads and repair traffic using Python 3.

This is an implementation of ReneSmeekes [successrate.sh](https://github.com/ReneSmeekes/storj_success_rate).
This iterates over the log file once, resulting in high savings in execution time, especially when processing large log files.
This script will likely work on Windows, but the text coloring will be interpreted incorrectly.

## How to use it

chmod +x successrate.py  
./successrate.py  
or  
python successrate.py  
or  
python3 successrate.py  

Usage is otherwise identical to [successrate.sh](https://github.com/ReneSmeekes/storj_success_rate).

Once optional argument is accepted, which can either be a docker container name or a path to the log file. If no argument is specified, the logs will be retrieved from a docker container named _storagenode_.
