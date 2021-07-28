#!/usr/bin/env python3
import argparse, sys, requests, time
from bs4 import BeautifulSoup

DEFAULT_USERAGENT = "linklister <github.com/chfour/linklister>"

def recurse_find(url: str, file, verbose=False, user_agent=DEFAULT_USERAGENT, interval=0.1):
    r = requests.head(url, headers={"User-Agent": user_agent})
    if verbose: print(f"* HEAD {url} | code {r.status_code} type {r.headers.get('content-type', 'unknown')!r}", file=sys.stderr)
    if not r.ok: return
    file.write(f"{url}\n")
    file.flush()

    if r.headers.get("content-type", None).startswith("text/html"):
        r = requests.get(url, headers={"User-Agent": user_agent})
        if verbose: print(f"* GET {url} | code {r.status_code}", file=sys.stderr)
        soup = BeautifulSoup(r.text, features="html5lib")
        links = soup.find_all("a")
        if verbose: print(f"* {len(links)} <a> tags", file=sys.stderr)
        for link in links:
            if link["href"] in ["../", ".."]: continue
            recurse_find(url + link["href"], file, verbose, user_agent, interval)
            time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url", type=str,
                        help="URL to start from")
    parser.add_argument("-o", "--output", type=str, default="-",
                        help="output file to write to, - for stdout, default -")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="stay quiet and don't output anything to stderr")
    parser.add_argument("-u", "--user-agent", type=str, default=DEFAULT_USERAGENT,
                        help=f"set custom user agent, default is '{DEFAULT_USERAGENT}'")
    parser.add_argument("-i", "--interval", type=float, default=0.1,
                        help="time to wait between requests")
    args = parser.parse_args()

    if args.output == "-":
        output = sys.stdout
    else:
        output = open(args.output, "w")

    with output:
        recurse_find(args.start_url, output, verbose=(not args.quiet), user_agent=args.user_agent, interval=args.interval)
