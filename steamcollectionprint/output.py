from steamcollectionprint import common


def shell_print(collections, subscriptions, dependencies):

    print("Key:\nx - subscribed\nE - item also in other collections\nC - dependency in this collection\nM - dependency in this and other collections")

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
        print(collections[col_id]['title'])
        deps = {}
        for item_id in sorted(collections[col_id]['items'], key=lambda id_: collections[col_id]['items'][id_]):
            if item_id in dependencies:
                deps.update(dependencies[item_id])
        dep_enum = {dep_id: i+1 for i, dep_id in enumerate(sorted(deps, key=lambda i: deps[i]))}
        itemlines = []
        for item_id in sorted(collections[col_id]['items'], key=lambda id_: collections[col_id]['items'][id_]):
            # Check if subscribed
            insub = False
            s = []
            if item_id in subscriptions:
                s += 'x'
            else:
                s += ' '
            # Check if item in other collections
            if len(item_collections[item_id]) > 1:
                s += 'E'
            else:
                s += ' '
            dep_str = ''
            for d_id in sorted(dep_enum, key=lambda i: dep_enum[i]):
                if d_id in dependencies[item_id]:
                    dep_str += str(dep_enum[d_id])
                else:
                    dep_str += ' ' * len(str(dep_enum[d_id]))
            s.append(dep_str)
            print(' ' * ind, end='')
            print(' '.join(s), collections[col_id]['items'][item_id])
        if deps:
            print(' ' * ind, end='')
            print('DEPS:')
            for d_id in sorted(deps, key=lambda id_: deps[id_]):
                s = [str(dep_enum[d_id])]
                # Check if subscribed
                if d_id in subscriptions:
                    s += 'x'
                else:
                    s += ' '
                # Check if dep in this collection
                incol = False
                if d_id in collections[col_id]['items']:
                    incol = True
                # Check if dep in other collections
                ocol = False
                if d_id in item_collections and len(item_collections[d_id]) > 1:
                    ocol = True
                if incol and ocol:
                    s += 'M'
                elif incol and not ocol:
                    s += 'C'
                elif ocol:
                    s += 'E'
                else:
                    s += ' '
                print(' ' * ind * 2, end='')
                print(' '.join(s), deps[d_id], common.item_url(d_id))
        if i < len(collections)-1:
            print()

    nocol = {item_id for item_id in subscriptions if item_id not in item_collections}
    if nocol:
        print("\nSubscriptions outside collections:")
        for id_ in nocol:
            print('{}{} {}'.format(' ' * ind, subscriptions[item_id],
                                   common.item_url(id_)))
    else:
        print("\nAll subscriptions in collections!")
"""
    nosub = {item_id for item_id in item_collections if item_id not in subscriptions}
    if nosub:
        print("\nUnsubscribed items in collections:")
        for id_ in nosub:
            title = 
            print('{}{} {}'.format(' ' * ind, collections[item_collections[item_id]]['items'][id_], common.item_url(id_)))
    else:
        print("\nAll collections fully subscribed!")
"""
