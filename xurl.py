#!/usr/bin/python
import argparse
import re

import requests


def get_parser():
    parser = argparse.ArgumentParser(
        prog="xurl",
        allow_abbrev=False,
        description="extract links from file or url to a file",
    )
    parser.add_argument("location", help="file or url", metavar="LOCATION")
    parser.add_argument("-a", action="store", type=str, help="append URL to links", metavar="URL")
    parser.add_argument("-c", action="append", type=str, help="contain text (REGEX)", metavar="TEXT")
    parser.add_argument("-C", action="append", type=str, help="not contain text (REGEX)", metavar="TEXT")
    parser.add_argument("-q", action="store_true", help="quiet mode (do not print Errors/Warnings/Infos)")

    return parser


def get_content(location, quiet):
    if location.startswith("http"):
        try:
            return requests.get(location).text
        except Exception as e:
            if not quiet:
                print("Error: Could not get page content")
            exit()
    else:
        try:
            with open(location) as file:
                return file.read()
        except Exception as e:
            if not quiet:
                print("Error: Could not get file content")
            exit()


def get_links(content):
    return re.findall(r"""(?<=href=")[^"]*|(?<=href=')[^']*""", content, re.MULTILINE)


def filter_content(regex, link, flag=True):
    return bool(re.search(regex, link)) == flag


def main():
    parser = get_parser()
    args = parser.parse_args()
    quiet = args.q
    links = get_links(get_content(args.location, quiet))
    if links:
        for link in links:
            link = link.strip()
            accepted = True
            for regex in args.c or ():
                if not filter_content(regex, link):
                    accepted = False
                    break
            if not accepted:
                continue
            for regex in args.C or ():
                if not filter_content(regex, link, False):
                    accepted = False
                    break
            if not accepted:
                continue
            elif link:
                print("{}{}".format(args.a if args.a and not link.startswith("http") else "", link))

    else:
        if not quiet:
            print("Error: No links found")
        exit()


if __name__ == "__main__":
    main()
