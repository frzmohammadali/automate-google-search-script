import os
import sys
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from threading import Thread
from queue import Queue
import argparse
import urllib.parse

chrome_driver_executable_path = ''
if getattr(sys, 'frozen', False):
    # publish one file
    chrome_driver_executable_path = sys._MEIPASS + r'\resource\chromedriver.exe'
else:
    # source
    chrome_driver_executable_path = os.getcwd() + r'\resource\chromedriver.exe'

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
capa['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

attempt = 0
successful_attempt = 0
final_sleep = 0
timeout_ex = 0
other_ex = 0
recaptcha_ex = 0


def main_script(keyword, site_url, max_successful_clicks, browser_visibility_flag):
    global attempt
    global successful_attempt
    global final_sleep
    global timeout_ex
    global other_ex
    global recaptcha_ex

    while successful_attempt < max_successful_clicks:

        options = Options()
        if not browser_visibility_flag:
            options.add_argument('--headless')
        options.add_argument("--js-flags=--expose-gc")
        options.add_argument("--enable-precise-memory-info")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-default-apps")
        options.add_argument("disable-infobars")
        options.add_argument('--disable-contextual-search')
        options.add_argument("--disable-notifications")
        options.add_argument('--incognito')
        options.add_argument('--disable-application-cache')
        options.add_argument('--no-sandbox')
        options.add_argument('--disk-cache-size=0')
        options.add_argument('–-disable-restore-session-state')
        options.add_argument('--disable-extensions')
        options.add_argument('test-type')
        options.add_argument('--silent')
        options.add_argument('--log-level=3')
        options.add_argument("--proxy-server=socks5://127.0.0.1:9150")

        driver = None

        try:
            driver = webdriver.Chrome(
                executable_path=chrome_driver_executable_path,
                chrome_options=options,
                desired_capabilities=capa)
            wait = WebDriverWait(driver, 40)
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(80)

            # driver.get('http://google.com/search?q=' + urllib.parse.urlencode(keyword)) # does not work
            driver.get('http://google.com/')
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#lst-ib')))
            driver.execute_script("window.stop();")
            driver.execute_script("window.stop();")

            attempt += 1
            elm = driver.find_element_by_css_selector('#lst-ib')
            elm.send_keys(keyword)
            elm.send_keys(Keys.RETURN)
            sleep(3)
            recaptcha = None
            try:
                recaptcha = driver.find_elements_by_css_selector('#recaptcha')
            except:
                pass
            if not recaptcha:
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#res a')))
                # driver.execute_script("window.stop();")
                site_links = driver.find_elements_by_css_selector('#res a')
                site_links_filtered = filter(lambda x: site_url in x.get_attribute('href'), site_links)
                site_link = next(site_links_filtered)
                site_link.click()
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'head')))
                sleep(5)
                successful_attempt += 1
                final_sleep = 5
            else:
                driver.execute_script("window.stop();")
                recaptcha_ex += 1
                final_sleep = 0

        except TimeoutException as ex:
            final_sleep = 0
            timeout_ex += 1
        except Exception as ex:
            final_sleep = 0
            other_ex += 1
        else:
            info_message = '{}\t|\tprocess pid: {: <6}\t|\t{: >5} attempt\t|\t{: >5} successful click\t|\t{: >5} timeout\t|\t {: >5} recaptcha \t|\t{: >5} error'.format(
                datetime.now().strftime('%Y/%m/%d %H:%M:%S'), os.getpid(), attempt,
                successful_attempt,
                timeout_ex,
                recaptcha_ex,
                other_ex
            )
            print(info_message)
            f = open('log.txt', 'a')
            f.write(info_message + '\n')
            f.close()
        finally:
            sleep(final_sleep)
            if driver:
                driver.close()
            del driver

    print()
    print('process pid: {} | finished {} successful clicks! \nprocess stopped...'.format(os.getpid(),
                                                                                         max_successful_clicks))
    f = open('log.txt', 'a')
    f.write('process pid: {} | finished {} successful clicks! \nprocess stopped...'.format(os.getpid(),
                                                                                           max_successful_clicks) + '\n')
    f.close()
    print()


class WorkerThread(Thread):
    def __init__(self, q, keyword, site_url, max_successful_clicks, browser_visibility_flag):
        super().__init__()
        self.setDaemon(True)
        self.q = q
        self.keyword = keyword
        self.site_url = site_url
        self.max_successful_clicks = max_successful_clicks
        self.browser_visibility_flag = browser_visibility_flag

    def run(self):
        while True:
            print()
            print('automated searching started...')
            print()
            main_script(self.keyword, self.site_url, self.max_successful_clicks, self.browser_visibility_flag)
            self.q.task_done()


parser = argparse.ArgumentParser(prog='python automate_search_google.py',
                                 description='A script to automatically search keywords on google and click on your desired website link as much as you want.')

parser.add_argument('k', help='list of keywords to search in format of "[\'keyword 1\',\'keyword 2\']"')
parser.add_argument('u', help='Url of your desired website to be clicked without http and www. eg: example.com')
parser.add_argument('m', type=int, help='maximum successful click count you want. eg: 500')
parser.add_argument('-v', '--visible', action='store_true',
                    help='browser visibility flag. if present the browser become visible')

args = parser.parse_args()

keywords = eval(args.k)

message = '  please start tor browser first  '.upper()
print()
message_str = '#' * 10 + message + '#' * 10
print('#' * len(message_str))
print('#' * len(message_str))
print('#' * 10 + ' ' * len(message) + '#' * 10)
print(message_str)
print('#' * 10 + ' ' * len(message) + '#' * 10)
print('#' * len(message_str))
print('#' * len(message_str))
print()

my_queue = Queue()

for key in keywords:
    worker = WorkerThread(my_queue, key, args.u, args.m, args.visible)
    worker.start()

for i in keywords:
    my_queue.put(i)
    sleep(1)

my_queue.join()

c = input('Press Enter to exit program... ')
exit(0)
