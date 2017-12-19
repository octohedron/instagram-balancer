#!/usr/bin/env python3.5

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from util.extractor import extract_followers_list, unfollow_non_followers
from util.login_util import login_user
from os import environ

chrome_options = Options()
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--lang=en-US')
chrome_prefs = {
    'intl.accept_languages': 'en-US'
}
chrome_options.add_experimental_option('prefs', chrome_prefs)

browser = webdriver.Chrome('./assets/chromedriver',
                           chrome_options=chrome_options)

# makes sure slower connections work as well
browser.implicitly_wait(25)

try:
    INSTA_USER = environ.get('INSTA_USER')
    INSTA_PW = environ.get('INSTA_PW')

    if not login_user(browser,
                      INSTA_USER,
                      INSTA_PW,
                      True):
        print('Wrong login data!')
    else:
        print('Extracting followers from ' + INSTA_USER)
        print('Logged in successfully!')
        following_list, following_amount = extract_followers_list(
            browser, INSTA_USER)
        # pprint("following_list")
        # pprint(following_list)
        unfollow_non_followers(browser, INSTA_USER,
                               following_list, following_amount)

except KeyboardInterrupt:
    print('Aborted...')

finally:
    browser.delete_all_cookies()
    browser.close()
