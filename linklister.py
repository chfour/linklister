#!/usr/bin/env python3
import argparse, sys, requests
from bs4 import BeautifulSoup

USER_AGENT = "linklister"

def recurse_find(url: str, file, verbose=False):
    r = requests.head(url, headers={"user-agent": USER_AGENT})
    if verbose: print(f"* HEAD {url} | code {r.status_code} type {r.headers.get('content-type', 'unknown')!r}", file=sys.stderr)
    if not r.ok: return
    file.write(f"{url}\n")

    if r.headers.get("content-type", None).startswith("text/html"):
        r = requests.get(url, headers={"user-agent": USER_AGENT})
        if verbose: print(f"* GET {url} | code {r.status_code}", file=sys.stderr)
        soup = BeautifulSoup(r.text, features="html5lib")
        links = soup.find_all("a")
        print(f"* {len(links)} <a> tags")
        for link in links:
            if link["href"] in ["../", ".."]: continue
            recurse_find(url + link["href"], file, verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url", type=str,
                        help="URL to start from")
    parser.add_argument("-o", "--output", type=str, default="-",
                        help="output file to write to, - for stdout, default -")
    args = parser.parse_args()

    if args.output == "-":
        output = sys.stdout
    else:
        output = open(args.output, "w")

    with output:
        recurse_find(args.start_url, output, verbose=True)
