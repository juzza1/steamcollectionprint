from steamcollectionprint import common


def shell_print(collections, subscriptions, dependencies):

    print("Key:\nx - subscribed\nM - item also in other collections\nC - dependency in this collection\n")

    if not collections and not subscriptions:
        print("No subscriptions or collections found. Make sure you provided a valid Steam App ID and your cookie file is up-to-date.")
        return

    item_collections = {}
    for c in collections:
        for i in collections[c]['items']:
            if i in item_collections:
                item_collections[i].add(c)
            else:
                item_collections[i] = set()
    ind = 2
    for i, col_id in enumerate(sorted(collections, key=lambda id_: collections[id_]['title'])):
        deps = {}
        print(collections[col_id]['title'])
        for item_id in sorted(collections[col_id]['items'], key=lambda id_: collections[col_id]['items'][id_]):
            s = ' ' * ind
            # Check if subscribed
            if item_id in subscriptions:
                s += 'x '
            else:
                s += '  '
            # Check if item in other collections
            if len(item_collections[item_id]) > 1:
                s += 'M '
            else:
                s += '  '
            print(s, end='')
            print(collections[col_id]['items'][item_id])
            if item_id in dependencies:
                deps.update(dependencies[item_id])
        if deps:
            print('{}DEPS:'.format(' ' * ind))
            for d_id in sorted(deps, key=lambda id_: deps[id_]):
                s = ' ' * ind * 2
                # Check if subscribed
                if d_id in subscriptions:
                    s += 'x '
                else:
                    s += '  '
                # Check if dep in this collection
                if d_id in collections[col_id]['items']:
                    s += 'C '
                else:
                    s += '  '
                # Check if dep in other collections
                if d_id in item_collections and len(item_collections[d_id]) > 1:
                    s += 'M '
                else:
                    s += '  '
                print(s, end='')
                print('{} {}'.format(deps[d_id], common.item_url(d_id)))
        if i < len(collections)-1:
            print()

    outside = {item_id for item_id in subscriptions if item_id not in item_collections}
    if outside:
        print("\nSubscriptions outside collections:")
        for id_ in outside:
            print('{}{} {}'.format(' ' * ind, subscriptions[item_id],
                                   common.item_url(id_)))
    else:
        print("\nAll subscriptions in collections!")
