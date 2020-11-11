from flask import Flask, render_template, request, redirect, url_for
from forms import StartUpForm, UpdateWallet, UpdateItems, BuyForm
import os

# M1 is the vending machine
import machine as m1

# directory selector
import tkinter
from tkinter import *
from tkinter import filedialog as fd
app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = '9q83h4q43q48hqh34829h4928'

# Helper var to indicate progress
progress = 20

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
    return render_template('startup.html', form=form,  wallet=m1.wallet, items=m1.items)


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
    return render_template('updateWallet.html', form_wallet=form_wallet, wallet=m1.wallet, items=m1.items)


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
    return render_template('updateItems.html', form=form, wallet=m1.wallet, items=m1.items)


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
        paymentOut = m1.makePayment(
            user_cash, item, denom_1, denom_2, denom_3, denom_4)
    return render_template('buy.html', form=form, items=m1.items, paymentOut=paymentOut, wallet=m1.wallet)


"""
-   Uses Tkinter to get the directory of a file
-   Not used because of later web complications
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


if __name__ == '__main__':
    app.run()
