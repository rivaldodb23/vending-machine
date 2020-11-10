from flask import Flask, render_template, request, redirect, url_for
from forms import StartUpForm, UpdateWallet, UpdateItems, BuyForm

# M1 is the vending machine
import machine as m1

# directory selector
import tkinter
from tkinter import *
from tkinter import filedialog as fd
app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhhhh'

# The default route when app starts, redirects to startup
@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for('startup'))


"""
- Creates a form StartUpForm
- Forms gets wallet and items data
- These data gets stored into the machine m1's state
"""
@app.route("/startup", methods=['GET', 'POST'])
def startup():
    form = StartUpForm()
    if form.is_submitted():
        print("Form submitted")
        result = request.form
        path = result['items_filename']
        m1.load_items(path)
        print(result)
        wallet_data = [int(result['denom_1']), int(result['denom_2']), int(
            result['denom_3']), int(result['denom_4'])]
        m1.wallet = wallet_data
        return redirect(url_for('buy'))
    return render_template('startup.html', form=form)


"""
- Allows user to enter wallet data
- Saves the machine's wallet state of the user to the updated version
"""
@app.route("/update_wallet", methods=['GET', 'POST'])
def update_wallet():
    form_wallet = UpdateWallet()
    if form_wallet.is_submitted():
        form_wallet
        result = request.form
        print(result)
        wallet_data = [int(result['denom_1']), int(result['denom_2']), int(
            result['denom_3']), int(result['denom_4'])]
        m1.wallet = wallet_data
        print("New wallet ", m1.wallet)
        return redirect(url_for('buy'))
    return render_template('updateWallet.html', form_wallet=form_wallet)


"""
- When button is clicked, the user selects new set of data for items
"""
@app.route("/update_items", methods=['GET', 'POST'])
def update_items():
    form = UpdateItems()
    if form.is_submitted():
        result = request.form
        path = result['items_filename']
        m1.load_items(path)
        return redirect(url_for('buy'))
    return render_template('updatItems.html', form=form)


"""
- Main section
- User selects coins from their wallet and purchase a item
- makePayment function will returned detailed output of the success or failure
    of the payement
"""
@app.route("/buy", methods=['GET', 'POST'])
def buy():
    paymentOut = "Payment output"
    form = BuyForm()
    if form.is_submitted():
        result = request.form
        denom_1 = int(result['denom_1'])
        denom_2 = int(result['denom_2'])
        denom_3 = int(result['denom_3'])
        denom_4 = int(result['denom_4'])
        user_cash = denom_1*1 + denom_2*2 + denom_3*5 + denom_4*10
        item = result['item_name']
        print("user cash = \t", user_cash, "\titem = \t", item)
        paymentOut = makePayment(
            user_cash, item, denom_1, denom_2, denom_3, denom_4)
    return render_template('buy.html', form=form, items=m1.items, paymentOut=paymentOut, wallet=m1.wallet)


"""
-   Uses Tkinter to get the directory of a file
"""


def getPath():
    '''
        Choose a directory in which the generated files will be saved

        USE:
            path = getPath()
    '''
    root = Tk()
    root.filename = fd.askopenfilename()
    # temp code to remove the ugly tk popup - not working well currently with while loop
    #     Button(root, text="Quit", command=root.destroy).pack()
    #     root.mainloop()
    filename = root.filename
    root.quit
    return filename


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
    if (m1.has_coins(c1, c2, c3, c4) == False):
        return "Invalid coins specified, Complete refund"

    if (m1.has_item(item) == False):
        if (m1.num_items(item) == 0):
            return "Item out of stock, Complete refund"
        return "Invalid item selected, Complete refund"

    if (m1.is_enough_money(user_cash, item) == False):
        return "Invalid cash amount, Complete refund"
    m1.deduct_item(item)
    change = m1.get_user_change(user_cash, m1.get_item_cost(item))
    R1 = m1.get_num_denom_1_change(change)
    R2 = m1.get_num_denom_2_change(change)
    R5 = m1.get_num_denom_3_change(change)
    R10 = m1.get_num_denom_4_change(change)
    str_out = "You have successfully purchased item = " + item + " "
    str_out = str_out + "Your change is = " + str(change)
    str_out = str_out + " " + str(R1) + " x R1, " + str(R2) + \
        " x R2, " + str(R5) + " x R5, " + str(R10) + " x R10 "
    m1.remove_coins(c1, c2, c3, c4)
    m1.add_coins(R1, R2, R5, R10)
    return str_out


if __name__ == '__main__':
    app.run()
