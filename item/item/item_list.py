#!/usr/bin/python
import functools
import item.item.item_library as lib

items = lib.ItemLibrary()

#IMPORT ITEMS
#import item.item.item_amulet
from item.item.item_2hccweapon import *
from item.item.item_1hccweapon import *
#import item.item.item_cape

#FILL LIBRARY
items.fill(Item2HCCWeapon(1),
           Item1HCCWeapon(2))



