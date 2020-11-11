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
import time
import progress

#   Variable to help track progress
complete = 0
progress_bar = progress.App()
progress_bar.hide()

base_denom = 1
denom_1 = base_denom
denom_2 = 2
denom_3 = 5
denom_4 = 10

items = {};
wallet = [0,0,0,0];

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
- Returns the number of lines in a file
- Function obtained from kite.com
"""
def file_num_lines(file):
    line_count = 0
    for line in file:
        if line != '\n':
            line_count += 1
    return line_count

"""
- Loads the item data and store it in global variable items
- Saves Name of item, what the item costs, number of that items
"""
def load_items(filename):
    progress_bar.update_bar(0)
    progress_bar.show()
    file = open(filename, "r")
    lines = file_num_lines(file)
    file.close()
    with open(filename) as file:
        lines = 10
        
        print("num lines = ", str(lines))
        reader = csv.reader(file)
        print("File read successfully")
        i = -1;
        for row in reader:
            complete = ((i+2)*100)/lines
            print("progress = ", str(complete))
            progress_bar.update_bar(complete)
            if (i != -1):
                cost = round(int(row[1]))
                num_items = int(row[2])
                row[1] = cost
                row[2] = num_items
                items[i] = row
            time.sleep(0.1)
            i = i + 1
    complete = 0
    print('progress = ', str(complete))
    progress_bar.hide()
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
"""
- Closes app thread
"""
def close_app():
    return progress_bar.stop()

"""
-   Gets the total cash and coins the user wants to buy with as input
-   If user does not have the coins the user specified to buy with, the user is notified
-   If item user specified does not exist, user is notified
-   If item user selected is out of stock, user is notified
-   If the amount of cash user specfied is too little, user is notified
-   For all the above the user gets a complete refund

-   If the payment is successful, user gets a detailed output of
    the transaction and change
"""
def makePayment(user_cash, item, c1, c2, c3, c4):
    progress_bar.show()
    progress_bar.update_bar(0)
    if (has_coins(c1, c2, c3, c4) == False):
        progress_bar.update_bar(100)
        progress_bar.hide()
        return "Invalid coins specified, Complete refund"

    if (has_item(item) == False):
        if (num_items(item) == 0):
            progress_bar.update_bar(100)
            progress_bar.hide()
            return "Item out of stock, Complete refund"
            progress_bar.update_bar(100)
            progress_bar.hide()
        return "Invalid item selected, Complete refund"

    if (is_enough_money(user_cash, item) == False):
        progress_bar.update_bar(100)
        progress_bar.hide()
        return "Invalid cash amount, Complete refund"
    deduct_item(item)
    progress_bar.update_bar(10)
    change = get_user_change(user_cash, get_item_cost(item))
    progress_bar.update_bar(20)
    R1 = get_num_denom_1_change(change)
    progress_bar.update_bar(30)
    R2 = get_num_denom_2_change(change)
    progress_bar.update_bar(40)
    R5 = get_num_denom_3_change(change)
    progress_bar.update_bar(50)
    R10 = get_num_denom_4_change(change)
    progress_bar.update_bar(60)
    str_out = "You have successfully purchased item = " + item + " "
    progress_bar.update_bar(70)
    str_out = str_out + "Your change is = R" + str(change) + ": "
    progress_bar.update_bar(80)
    str_out = str_out + str(R1) + " x R1, " + str(R2) + \
        " x R2, " + str(R5) + " x R5, " + str(R10) + " x R10 "
    remove_coins(c1, c2, c3, c4)
    progress_bar.update_bar(90)
    add_coins(R1, R2, R5, R10)
    progress_bar.update_bar(100)
    progress_bar.hide()
    return str_out