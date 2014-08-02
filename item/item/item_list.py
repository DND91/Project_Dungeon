#!/usr/bin/python
import functools

items = []
#IMPORT ITEMS
import item.item.item_amulet
import item.item.item_blade
import item.item.item_cape

#INIT ITEMS
amulet = item.item.item_amulet.ItemAmulet()
blade = item.item.item_blade.ItemBlade()
cape = item.item.item_cape.ItemCape()

#APPEND ITEMS
items.append(amulet)
items.append(blade)
items.append(cape)

#SORT LIST
def compare(a, b):
    return a.getCost() - b.getCost()
items = sorted(items, key=functools.cmp_to_key(compare))



