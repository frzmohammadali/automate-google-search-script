# automate-google-search-script
This is a script written in python and selenium to automate search keywords on google and click on desired site to increase google search console CTR

## Description
This script uses `tor browser` proxy to simulate real users searching google. In order to get the script up and running, you need to download [tor browser bundle from here](https://www.torproject.org/projects/torbrowser.html.en#downloads "Download Tor Browser Bundle") and install it on your pc. Then go to the next step to run the script.

## Usage help
First clone the repository and install require libraries with pip using the command `pip install -r requirement.txt` then run the command: `$ python automate_search_google.py --help`

## Usage sample
First start `tor browser` then run below command:\
`$ python automate_search_google.py "['keyword 1','keyword 2']" mysite.com 500 -v`
#### command description:
  - `"['keyword 1','keyword 2']"` is *list of keywords to search*
  - `mysite.com` is *Url of your desired website to be clicked*
  - `500` is *maximum successful click count you want*
  - `-v` is *browser visibility flag. if present the browser become visible*

## logs
All the execution logs can be found in file 'log.txt' after each run of the script.

# Note: this script has been written for educational purpose not commercial. You use it on your own risk.
