"""
This machine represents a vending machine. The 4 denominations is automatically set, but
can be changed. Let base_denom = 1 money value unit be the smallest coin value. This system requires that every
other coint perfectly divides by the base_denom coin. For example, if R1 is the base_denom coin, and
R2, R5, R10 (for the purpos of this example) the other coin then the equation

R2 mod R1 == R5 mod R1 == R10 mod R1 == 0

Also note that every item_cost mod base_denom == 0 should be true. This implies that there
will always be chamge

Currently the assumption is made that there are an inexhaustable amount of each denom coin 
"""

import csv

base_denom = 1
denom_1 = base_denom
denom_2 = 2
denom_3 = 5
denom_4 = 10

items = {};
wallet = [5,5,3,3];

"""
- Checks to see if the user has the right amount of coins in their wallet
- Coins in wallet must be >= coins specified
"""

def has_coins(c1, c2, c3, c4):
    return (wallet[0] - c1 >= 0) and (wallet[1] - c2 >= 0) and (wallet[2] - c3 >= 0) and (wallet[3] - c4 >= 0)

"""
- Adds coins to wallet
"""

def add_coins(c1, c2, c3, c4):
    coin_set = [c1,c2,c3,c4]
    for i in range(0,4):
        wallet[i] = wallet[i] + coin_set[i]
"""
- Removes coins from wallet
"""

def remove_coins(c1, c2, c3, c4):
    coin_set = [c1,c2,c3,c4]
    for i in range(0,4):
        wallet[i] = wallet[i] - coin_set[i]


"""
- Loads the item data and store it in global variable items
- Saves Name of item, what the item costs, number of that items
"""
def load_items(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        i = -1;
        for row in reader:
            if (i != -1):
                cost = round(int(row[1]))
                num_items = int(row[2])
                row[1] = cost
                row[2] = num_items
                items[i] = row
            i = i + 1
    return items


"""
- Checks to see if an item exists in the current machine
- Items of the machine are stored in global variable 'items'
"""
def has_item(item):
    for row in items:
            if item in items[row]:
                return (items[row][2] > 0)
    return False

"""
- Finds the item in the machine
- Returns the cost of the item chosen
"""
def get_item_cost(item):
    for row in items:
            if item in items[row]:
                return items[row][1]
    return False

"""
- Checks to see if the user has enough money to purchase the item
- Returns True if the user has enough money to purchase the item
- Returns False otherwise
"""
def is_enough_money(money, item):
    if (get_item_cost(item) > money):
        return False
    return True

"""
- Helper function
- Returns the current number of a specific item
"""
def num_items(item):
    for row in items:
            if item in items[row]:
                return items[row][2]
    return -1

"""
- Decrements the number of a specific item by 1
"""
def deduct_item(item):
    for row in items:
            if item in items[row]:
                new_num_items = num_items(item) - 1
                items[row][2] = new_num_items

"""
- Returns the change a user needs to receive
"""
def get_user_change(user_money, item_cost):
    return user_money - item_cost

"""
- Returns the amount of coins change by the highest denom, denom 4
"""
def get_num_denom_4_change(change):
    return change // denom_4
"""
- Returns the amount of coins change by denom 3
"""
def get_num_denom_3_change(change):
    return (change % denom_4) // denom_3

"""
- Returns the amount of coins change by denom 2
"""
def get_num_denom_2_change(change):
    return ((change % denom_4) % denom_3) // denom_2
"""
- Returns the amount of coins change by the base denom, denom 1
"""
def get_num_denom_1_change(change):
    return (((change % denom_4) % denom_3) % denom_2) // denom_1