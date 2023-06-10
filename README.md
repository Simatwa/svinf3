<h1 align="Center">svinf3</h1>
<p align="center">
<a href='#'><img src="https://img.shields.io/static/v1?logo=github&label=Github&message=Passing&color=green" alt="github" /></a>
<a href='LICENSE'><img src='https://img.shields.io/static/v1?logo=MIT&label=License&message=MIT&color=purple' alt='license'/></a>
<a href='#'><img  src='https://visitor-badge.glitch.me/badge?page_id=Simatwa.svinf3&left_color=red&right_color=green' alt='Visitors'/></a>
<a href="https://wakatime.com/badge/github/Simatwa/svinf3"><img src="https://wakatime.com/badge/github/Simatwa/svinf3.svg" alt="wakatime"></a>
</p>

> Server inspector
## [Dependencies](requirements.txt)

- colorama
- cloudscraper
- tabulate
- requests

## Installation and usage

### Installation

- Execute the following commands at the terminal 

```bash
$ git clone https://github.com/Simatwa/svinf3.git
$ cd svinf3
$ bash install.sh 
   #or
$ sudo bash install.sh
```

### Usage

`$ svinf3 {url}`

- For futher info run `svinf3 -h`.

```
usage: svinf3 [-h] [-v] [-g path] [-p path] [-c path]
              [-o filepath] [-t TRIALS] [-he filepath]
              [-tbl [html,grid]+] [-wr [a,wb,ab]]
              [-i INTERVAL] [-tm TIMEOUT]
              [--browser chrome|firefox]
              [--platform darwin|ios|android|windows|linux]
              [-thr THREAD] [--binary] [--show]
              [--prettify] [--new]
              url

Simple Server inspector regards : bc03

positional arguments:
  url                   Link to the website/API - None

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and
                        exit
  -g path, --get path   Use GET method to send json data
                        in path - None
  -p path, --post path  Use POST method to send json data
                        in path - None
  -c path, --cookies path
                        Path to cookies file formated in
                        json - None
  -o filepath, --output filepath
                        Path to save the response'
                        contents - None
  -t TRIALS, --trials TRIALS
                        Number of times to send request -
                        1
  -he filepath, --headers filepath
                        Path to header files formatted in
                        json - None
  -tbl [html,grid]+, --table [html,grid]+
                        Table format for displaying
                        contents - None
  -wr [a,wb,ab], --write-mode [a,wb,ab]
                        File mode for saving response - w
  -i INTERVAL, --interval INTERVAL
                        Time to sleep between requests
                        sent - 0
  -tm TIMEOUT, --timeout TIMEOUT
                        Maximum time while requesting -
                        15
  --browser chrome|firefox
                        Browser name to be used - firefox
  --platform darwin|ios|android|windows|linux
                        OS name to be used - linux
  -thr THREAD, --thread THREAD
                        Threads amount at once - None
  --binary              Specifies to handle response
                        contents as binary data - False
  --show                Displays the response contents -
                        False
  --prettify            Formats the response in readable
                        format - False
  --new                 Overwrites file with same name -
                        output - False 
  ```
