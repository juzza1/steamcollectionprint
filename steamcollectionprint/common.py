def item_url(item_id):
    return 'https://steamcommunity.com/workshop/filedetails/?id={}'.format(item_id)


def collection_url(collection_id):
    return item_url(collection_id)


def parse_steam_date(date_str):
    m = re.search(r'(\d+) (\w+)(?:, (\d+))?', date_str)
    day = int(m.group(1))
    month = datetime.strptime(m.group(2), '%b').month
    if m.group(3):
        year = int(m.group(3))
    else:
        year = datetime.now().year
    return datetime(year, month, day)
