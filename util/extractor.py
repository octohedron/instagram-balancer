"""Methods to extract the data for the given usernames profile"""
from time import sleep
from re import findall
import random
import math
from pprint import pprint
import decimal
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# Sleep values for 1 to 8 seconds
SHORTSLEEP_UPPER = 800
SHORTSLEEP_LOWER = 1
# Sleep values for 300 to 480 seconds
SLEEP_UPPER = 48000
SLEEP_LOWER = 30000


def get_user_info(browser):
    """Get the basic user info from the profile screen"""

    container = browser.find_element_by_class_name('_mesn5')
    infos = container.find_elements_by_class_name('_t98z6')
    followers = infos[1].text.split(' ')[0].replace(',', '').replace('.', '')
    followers_amount = int(followers.replace('k', '00').replace('m', '00000'))
    following = infos[2].text.split(' ')[0].replace(',', '').replace('.', '')
    following_amount = int(following.replace('k', '00'))

    return followers_amount, following_amount


# Extracts your followers
def extract_followers_list(browser, username):
    browser.get('https://www.instagram.com/' + username)
    followers_amount, following_amount = get_user_info(browser)
    body_elem = browser.find_element_by_tag_name('body')
    followers_button = body_elem.find_element_by_xpath(
        '//a[contains(@class, "_t98z6")]')
    followers_button.click()
    do_sleep(SHORTSLEEP_LOWER, SHORTSLEEP_UPPER)
    usernames = []
    # This should keep going until there's no more to scroll
    while (len(browser.find_elements_by_class_name("_6e4x5")) <
            followers_amount):
        scroll_for_loading_list(browser)

    link_elems = browser.find_elements_by_class_name('_o5iw8')
    for link in link_elems:
        usernames.append(link.get_attribute("href").split("/")[-2])
    return usernames, following_amount


# Goes through the list of people you follow and unfollows them if they
# are not following you
def unfollow_non_followers(browser, username, following_list, following_amount):
    browser.get('https://www.instagram.com/' + username)
    body_elem = browser.find_element_by_tag_name('body')
    following_button = body_elem.find_elements_by_class_name(
        '_t98z6')[2]
    following_button.click()
    do_sleep(SHORTSLEEP_LOWER, SHORTSLEEP_UPPER)
    # This should keep going until there's no more to scroll
    while (len(browser.find_elements_by_class_name("_6e4x5")) <
            following_amount):
        scroll_for_loading_list(browser)
    do_sleep(SHORTSLEEP_LOWER, SHORTSLEEP_UPPER)
    # Complete list of following elements
    following = browser.find_elements_by_class_name("_6e4x5")
    # Scroll to the top of the list
    browser.execute_script(
        "arguments[0].scrollIntoView(true)",
        browser.find_elements_by_class_name("_6e4x5")[0])
    # Scroll by 10
    scrolls = math.floor(following_amount / 10) + 1
    # Go by 10
    for x in range(0, scrolls):
        pprint("Starting with scroll " + str(x))
        # For index starting at current scroll position
        # ending at the bottom of the list of the current scroll
        ending = x * 10 + 10
        # if we are at the last scroll
        if x == scrolls:
            ending = following_amount - 1
        pprint("Scroll ends at " + str(ending))
        for y in range(x * 10, ending):  # i.e. 60 to 70 or 0 to 10
            # Inspect, each item on the list
            # if the account if being followed but not in the followers list
            # press the unfollow button
            # then sleep
            try:
                account_link = following[y].find_element_by_xpath(
                    './/a[contains(@class, "_2g7d5")]')
                account_name = account_link.get_attribute(
                    "href").split("/")[-2]
                pprint("Checking " + account_name)
                if account_name not in following_list:
                    pprint(account_name + " not in following_list, unfollowing")
                    unfollow_button = following[y].find_element_by_xpath(
                        './/button[contains(@class, "_qv64e _t78yp _4tgw8 _njrw0")]')
                    unfollow_button.click()
                    do_sleep(SLEEP_LOWER, SLEEP_UPPER)
            except IndexError:
                return
            do_sleep(SHORTSLEEP_LOWER, SHORTSLEEP_UPPER)
        # Do a scroll
        try:
            pprint("Try to scroll to " + str(x * 10 + 10) + " item")
            browser.execute_script(
                "arguments[0].scrollIntoView(true)",
                browser.find_elements_by_class_name("_6e4x5")[x * 10 + 10])
        except IndexError:
            index = following_amount - 1
            pprint("Index error, trying to scroll, scrolling to " + str(index))
            browser.execute_script(
                "arguments[0].scrollIntoView(true)",
                browser.find_elements_by_class_name("_6e4x5")[index])


def scroll_for_loading_list(browser):
    # scroll to the bottom to trigger loading
    try:
        browser.execute_script(
            "arguments[0].scrollIntoView(true)",
            browser.find_elements_by_class_name("_6e4x5")[-1])
        # sleep between 0 and 2 seconds
        do_sleep(SHORTSLEEP_LOWER, SHORTSLEEP_UPPER)
        # Will throw index out of range if you have less than 5 followers
        browser.execute_script(
            "arguments[0].scrollIntoView(true)",
            browser.find_elements_by_class_name("_6e4x5")[-5])
        do_sleep(SHORTSLEEP_LOWER, SHORTSLEEP_UPPER)
        browser.execute_script(
            "arguments[0].scrollIntoView(true)",
            browser.find_elements_by_class_name("_6e4x5")[-1])
    except Exception as e:
        do_sleep(SHORTSLEEP_LOWER, SHORTSLEEP_UPPER)
        print(e)


def do_sleep(start, end):
    sleep(float(decimal.Decimal(random.randrange(start, end)) / 100))
