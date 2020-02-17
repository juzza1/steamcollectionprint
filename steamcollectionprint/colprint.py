#!/usr/bin/env python3

import argparse
from datetime import datetime
from http.cookiejar import MozillaCookieJar
import re
import sys

from bs4 import BeautifulSoup
import requests

from steamcollectionprint import common, output


def default_soup_maker(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def import_cookies(cookie_file):
    cookies = MozillaCookieJar(cookie_file)
    cookies.load()
    return cookies


def _workshop_page_soups(url, soup_maker=default_soup_maker):
    # Get first page first, find how many pages more there are
    soup = soup_maker(url.format(1))
    soups = [soup]
    last_page = max((int(pl.text.strip()) for pl in soup.find_all(class_='pagelink')), default=1)
    for pnum in range(2, last_page + 1):
        soups.append(soup_maker(url.format(pnum)))
    return soups


def collection_items(collection_id, soup_maker=default_soup_maker):
    soup = soup_maker(common.collection_url(collection_id))
    items = {}
    for div in soup.find_all(class_='collectionItemDetails'):
        id_ = div.find('a')['href'].split('=')[-1]
        title = div.find(class_='workshopItemTitle').text.strip()
        #author_name = div.find(class_='workshopItemAuthorName').a.text.strip()
        #author_url = div.find(class_='workshopItemAuthorName').a['href']
        items[id_] = title
    return items


def collections(app_id, user_id, soup_maker=default_soup_maker):
    collections_url = 'https://steamcommunity.com/profiles/{}/myworkshopfiles/?section=collections&appid={}&p={{}}&numberpage=30'.format(user_id, app_id)
    collections = {}
    for col_page_soup in _workshop_page_soups(collections_url, soup_maker):
        for a in col_page_soup.find_all(class_='workshopItemCollection'):
            col_id = a['href'].split('=')[-1]
            title = a.find(class_='workshopItemTitle').text.strip()
            items = collection_items(col_id, soup_maker)
            collections[col_id] = {'title': title, 'items': items}
    return collections


def subscriptions(app_id, user_id, soup_maker=default_soup_maker):
    subscriptions_url = 'https://steamcommunity.com/profiles/{}/myworkshopfiles/?appid={}&browsefilter=mysubscriptions&p={{}}&numperpage=30'.format(user_id, app_id)
    items = {}
    for sub_page_soup in _workshop_page_soups(subscriptions_url, soup_maker):
        for div in sub_page_soup.find_all(class_='workshopItemSubscriptionDetails'):
            id_ = div.a['href'].split('=')[-1]
            title = div.find(class_='workshopItemTitle').text.strip()
            #upd_str = div.find(string=re.compile(r'Last Updated'))
            #m = re.search(r'Last Updated (.*)', upd_str)
            #updated = parse_steam_date(m.group(1))
            items[id_] = title
    return items


def dependencies(item_id, soup_maker=default_soup_maker):
    # TODO: save downloaded item pages somewhere for faster access
    soup = soup_maker(common.item_url(item_id))
    #title = soup.find(class_='workshopItemTitle'.text.strip())
    #author_block = soup.find(class_='creatorsBlock')
    #author_url = author_block.a['href']
    #author_name = author_block.find(class_='friendBlockContent').text.strip()
    a = soup.find(class_='detailsStatsContainerRight')
    #updated = parse_steam_date(list(a.stripped_strings)[-1])
    items = {}
    req = soup.find(class_='requiredItemsContainer')
    if req:
        for a in req.find_all('a'):
            dep_id = a['href'].split('=')[-1]
            # Recurse for dependencies of dependencies
            items.update(dependencies(dep_id, soup_maker))
            title = a.find(class_='requiredItem').text.strip()
            items[dep_id] = title
    return items


def main(app_id, cookie_file):
    cookies = import_cookies(cookie_file)
    user_id = requests.utils.dict_from_cookiejar(cookies)['steamRememberLogin'].split('%')[0]
    s = requests.Session()
    s.cookies = cookies
    soup_maker = lambda url: BeautifulSoup(s.get(url).text, 'html.parser')
    colls = collections(app_id, user_id, soup_maker)
    subs = subscriptions(app_id, user_id, soup_maker)
    items_in_collections = {itm for col_id in colls for itm in colls[col_id]['items']}
    deps = {item_id: dependencies(item_id, soup_maker) for item_id in items_in_collections}

    output.shell_print(colls, subs, deps)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Outputs information about your Steam workshop collections and subscriptions.')
    parser.add_argument('appid', help='Steam App ID')
    parser.add_argument(
        'cookie_file', metavar='cookie-file',
        help='Netscape-format cookie file containing cookies for steamcommunity.com.')
    #parser.add_argument('-f', '--force-update', action='store_true')
    #parser.add_argument('-o', '--output')
    args = parser.parse_args()
    main(args.appid, args.cookie_file)


if __name__ == '__main__':
    parse_args()
