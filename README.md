# linklister

A "quick and dirty" script to list files on an HTTP server by crawling through file listings.
Useful for [open directories](https://www.reddit.com/r/opendirectories/).

## options

`linklister.py [-h] [-o OUTPUT] [-q] [-u USERAGENT] start_url`

* `-h`, `--help`: show help message
* `-o OUTPUT`, `--output OUTPUT`: output file, can be `-` for stdout and that's also the default
* `-q`, `--quiet`: be quiet and don't print anything to stderr
* `-u USER_AGENT`, `--user-agent USER_AGENT`: set the user agent to something other than `linklister <github.com/chfour/linklister>`
* `-i INTERVAL`, `--interval INTERVAL`: time in seconds to wait before requests, default is 0.1 sec
