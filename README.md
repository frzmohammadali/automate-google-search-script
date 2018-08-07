# automate-google-search-script
This is a script witten in python and selenium to automate search keywords on google and click on desired site to increase google search console CTR

## Usage help
First clone the repository and install require libraries with pip using the command `pip install -r requirement.txt` then run the command: `$ python automate_search_google.py --help`

## Usage sample
`$ python automate_search_google.py "['keyword 1','keyword 2']" mysite.com 500 -v`
#### command description:
  - `"['keyword 1','keyword 2']"` is *list of keywords to search*
  - `mysite.com` is *Url of your desired website to be clicked*
  - `500` is *maximum successful click count you want*
  - `-v` is *browser visibility flag. if present the browser become visible*

## logs
All the execution logs can be found in file 'log.txt' after each run of the script.

# Note: this script has been written for educational purpose not commercial. You use it on your own risk.
