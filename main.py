#!/usr/bin/python3
__version__ = str(1.4)
__author__ = "bc03"
program_info = f"Simple Server inspector regards : {__author__}"
platforms = ["darwin", "ios", "android", "windows", "linux"]
browsers = ["chrome", "firefox"]


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description=program_info)
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
    )
    parser.add_argument("url", help="Link to the website/API - %(default)s")
    parser.add_argument(
        "-g",
        "--get",
        help="Use GET method to send json data in path - %(default)s",
        metavar="path",
    )
    parser.add_argument(
        "-p",
        "--post",
        help="Use POST method to send json data in path - %(default)s",
        metavar="path",
    )
    parser.add_argument(
        "-c",
        "--cookies",
        help="Path to cookies file formated in json - %(default)s",
        metavar="path",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to save the response' contents - %(default)s",
        metavar="filepath",
    )
    parser.add_argument(
        "-t",
        "--trials",
        help="Number of times to send request - %(default)s",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-he",
        "--headers",
        help="Path to header files formatted in json - %(default)s",
        metavar="filepath",
    )
    parser.add_argument(
        "-tbl",
        "--table",
        help="Table format for displaying contents - %(default)s",
        metavar="[html,grid]+",
        choices=["html", "grid", "fancy_grid", "orgtbl", "pretty"],
    )
    parser.add_argument(
        "-wr",
        "--write-mode",
        help="File mode for saving response - %(default)s",
        dest="write_mode",
        default="w",
        choices=["a", "wb", "ab"],
        metavar="[a,wb,ab]",
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="Time to sleep between requests sent - %(default)s ",
        type=float,
        default=0,
    )
    parser.add_argument(
        "-tm",
        "--timeout",
        help="Maximum time while requesting - %(default)s",
        default=15,
        type=int,
    )
    parser.add_argument(
        "--browser",
        help="Browser name to be used - %(default)s",
        choices=browsers,
        default="firefox",
        metavar="|".join(browsers),
    )
    parser.add_argument(
        "--platform",
        help="OS name to be used - %(default)s",
        choices=platforms,
        default="linux",
        metavar="|".join(platforms),
    )
    parser.add_argument(
        "-thr", "--thread", help="Threads amount at once - %(default)s", type=int
    )
    parser.add_argument(
        "--binary",
        help="Specifies to handle response contents as binary data - %(default)s",
        action="store_true",
    )
    parser.add_argument(
        "--show",
        help="Displays the response contents - %(default)s",
        action="store_true",
        dest="all",
    )
    parser.add_argument(
        "--prettify",
        help="Formats the response in readable format - %(default)s",
        action="store_true",
    )
    parser.add_argument(
        "--new",
        help="Overwrites file with same name - output - %(default)s",
        action="store_true",
    )
    return parser.parse_args()


args = get_args()
import cloudscraper
import colorama as col
from sys import argv
from tabulate import tabulate
from time import sleep
from requests import Session
import requests

res = col.Fore.RESET
r = col.Fore.RED
b = col.Fore.BLUE
y = col.Fore.YELLOW
c = col.Fore.CYAN
g = col.Fore.GREEN
w = col.Fore.WHITE
m = col.Fore.MAGENTA
sess_ion = Session()


def exit_t(e="exiting..."):
    print(y + "ERROR : " + r + str(e) + res)
    from sys import exit

    exit()


def verify_write_mode():
    if args.binary:
        rp = "wb"
    else:
        rp = "w"
    return rp


def save_data(data):
    if args.output:
        try:
            with open(
                args.output, verify_write_mode() if args.new else args.write_mode
            ) as fp:
                fp.write(data)
        except Exception as e:
            print(f"[*] Failed to save data - {e}")


class output:
    def __init__(self):
        self.out = lambda a, b: print(f"[*] {str(a)+str(b)+res}")

    def info(self, msg):
        self.out(c, msg)

    def warn(self, msg):
        self.out(y, msg)

    def error(self, msg):
        self.out(r, msg)


class handler:
    def __init__(self):
        self.out = output()
        link = args.url
        if not "http" in link:
            if "localhost" in link or "192." in link or "10." in link or "127." in link:
                link = "http://" + link
            else:
                link = "https://" + link
        self.link = link

    def data(self):
        try:
            pasr = {"url": self.link, "timeout": args.timeout}
            # req = requests
            req = cloudscraper.create_scraper(
                browser={
                    "browser": args.browser,
                    "platform": args.platform,
                    "desktop": True,
                },
            )
            from json import loads

            get_content = lambda fnm: loads(open(fnm).read())

            if args.headers:
                pasr["headers"] = get_content(args.headers)

            if args.cookies:
                pasr["cookies"] = get_content(args.cookies)

            if args.post:
                pasr["data"] = get_content(args.post)
                resp = req.post(**pasr)

            elif args.get:
                pasr["params"] = get_content(args.get)
                resp = req.get(**pasr)

            else:
                resp = req.get(**pasr)

        except Exception as e:
            exit_t(e)
        else:
            print(m + "Source : " + r + resp.url)
            return resp

    def header_info(self, resp):
        for key, value in resp.headers.items():
            sorted = f"{key.capitalize()} : {g}{value}{res}"
            if key.lower() in ["server"]:
                self.out.warn(f"SERVER : {b+value+res}")
            else:
                self.out.info(sorted)
            # save_data(sorted)

    def main(self):
        try:
            resp = self.data()
        except Exception as e:
            exit_t(e)
        st_code = f'Status code : {g+str(resp.status_code)+" - "+y+resp.reason+res}'
        self.out.warn(st_code)
        if args.table:
            data = []
            for k, v in resp.headers.items():
                data.append([g + k.upper(), c + v])
            self.out.info(
                "Header info!\n"
                + tabulate(
                    data, headers=[y + "Header", y + "Info"], tablefmt=args.table
                )
            )
        else:
            self.header_info(resp)
        if args.all or args.output:
            # if not args.table:
            # self.header_info(resp)
            if args.prettify:
                try:
                    import json
                    dta = json.dumps(resp.json(),indent=5)
                except:
                    from bs4 import BeautifulSoup as bts
                    dta = bts(resp.text, "html.parser").prettify()
            else:
                dta = resp.content if args.binary else resp.text
            if args.all:
                self.out.info(f"{r} CONTENT {res}\n" + w + dta + res)
            if args.output:
                save_data(dta)


if __name__ == "__main__":
    try:
        run = handler()
        if args.thread:
            from threading import Thread as thr

            x = 0
            while x < args.trials + 1:
                t1 = thr(
                    target=run.main,
                )
                t1.start()
                x += 1
                if x % args.thread == 0:
                    t1.join()
                    sleep(args.interval)
        else:
            for _ in range(args.trials):
                run.main()
                try:
                    wait = sleep(args.interval) if args.interval else None
                except Exception as e:
                    exit_t(
                        str(
                            e,
                        )
                    )
                print("", end="\n")
    except Exception as e:
        exit_t(str(e))
# 12312204536
