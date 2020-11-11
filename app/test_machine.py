import unittest
import machine

filename_machine1 = 'app/testing/test-items.csv'


class TestMachine(unittest.TestCase):

    """
    -   Test scenario where user has enough and not enough coins
    """
    def test_has_coins(self):
        machine.wallet = [5, 5, 3, 1]
        self.assertTrue(machine.has_coins(4, 4, 2, 1))
        self.assertFalse(machine.has_coins(4, 4, 2, 2))

    """
    -   Check if adding coins works
    """
    def test_add_coins(self):
        machine.wallet = [5, 5, 3, 1]
        machine.add_coins(1, 1, 1, 1)
        self.assertTrue(machine.wallet == [6, 6, 4, 2])

    """
    -   Check if removing coins work properly
    """
    def test_remove_coins(self):
        machine.wallet = [5, 5, 3, 1]
        machine.remove_coins(1, 1, 1, 1)
        self.assertTrue(machine.wallet == [4, 4, 2, 0])

    """
    -   Test to see if all the items loaded successfully from a csv file
    """
    def test_load_items(self):
        items_machine1 = {}
        i = 0
        items_machine1[i] = ['Simba', 7, 0]
        i = i + 1
        items_machine1[i] = ['Lays', 7, 6]
        i = i + 1
        items_machine1[i] = ['Coke', 12, 7]
        i = i + 1
        items_machine1[i] = ['Fanta', 12, 5]
        i = i + 1
        items_machine1[i] = ['Water', 8, 8]
        i = i + 1
        items_machine1[i] = ['Kit-cat', 10, 12]
        i = i + 1
        items_machine1[i] = ['PS', 10, 2]
        i = i + 1
        items_machine1[i] = ['Gelly-beans', 14, 4]
        i = i + 1
        items_machine1[i] = ['Nik-Naks', 3, 7]
        self.assertEqual(machine.load_items(filename_machine1), items_machine1)

    """
    -   Test to see if an item is within the given list of items
    """
    def test_has_item(self):
        machine.load_items(filename_machine1)
        found_item = machine.has_item('Coke')
        found_non_item = machine.has_item('Apple tiser')
        zero_item = machine.has_item('Simba')
        self.assertTrue(found_item)
        self.assertFalse(found_non_item)
        self.assertFalse(zero_item)

    """
    -   Test to see if the cost of an item is correct 
    """
    def test_get_item_cost(self):
        machine.load_items(filename_machine1)
        self.assertTrue(machine.get_item_cost('PS') == 10)

    """
    -   Test to see if the amount of money the user gave is enough
    """
    def test_is_enough_money(self):
        machine.load_items(filename_machine1)
        self.assertFalse(machine.is_enough_money(9, 'PS'))
        self.assertTrue(machine.is_enough_money(10, 'PS'))
        self.assertTrue(machine.is_enough_money(11, 'PS'))

    """
    -   Test the helper function to see the quantity of a specific item
    """
    def test_num_items(self):
        machine.load_items(filename_machine1)
        self.assertTrue(machine.num_items('Fanta'), 5)

    """
    -   Test to see if an item is successfully deducted from an item
    """
    def test_deduct_item(self):
        machine.load_items(filename_machine1)
        old_num_cokes = machine.num_items('Coke')
        machine.deduct_item('Coke')
        self.assertTrue(machine.num_items('Coke'), old_num_cokes - 1)

    """
    -   Test to see if the user change output is enough
    """
    def test_get_user_change(self):
        machine.load_items(filename_machine1)
        self.assertTrue(20 - machine.get_item_cost('Coke') ==
                        machine.get_user_change(20, machine.get_item_cost('Coke')))

    """
    -   Test to see if user gets the right amount of R10 notes (coins)
    """
    def test_get_num_denom_4_change(self):
        machine.load_items(filename_machine1)
        change = machine.denom_4 * 2
        num_denom_4 = machine.get_num_denom_4_change(change)
        self.assertTrue(num_denom_4 == 2)

    """
    -   Test to see if user gets the right amount of R5 coins
    """
    def test_get_num_denom_3_change(self):
        machine.load_items(filename_machine1)
        change = machine.denom_4 * 1 + machine.denom_3 * 1
        num_denom_3 = machine.get_num_denom_3_change(change)
        self.assertTrue(num_denom_3 == 1)

    """
    -   Test to see if user gets the right amount of R2 coins
    """
    def test_get_num_denom_2_change(self):
        machine.load_items(filename_machine1)
        change = machine.denom_3 * 1 + machine.denom_2 * 1
        num_denom_2 = machine.get_num_denom_2_change(change)
        self.assertTrue(num_denom_2 == 1)

    """
    -   Test to see if user gets the right amount of R1 coins 
    """
    def test_get_num_denom_1_change(self):
        machine.load_items(filename_machine1)
        change = machine.denom_2 * 1 + machine.denom_1 * 1
        num_denom_1 = machine.get_num_denom_1_change(change)
        self.assertTrue(num_denom_1 == 1)

    """
    -   Test helper function that returns the number lines in a file
    """
    def test_fiile_num_lines(self):
        file = open(filename_machine1, "r")
        num_lines = 10
        ans = machine.file_num_lines(file)
        file.close()
        self.assertTrue(num_lines == ans)

    """
    -   Test all possible scenarios of a payment that could be made
    """
    def test_makePayment(self):
        machine.load_items(filename_machine1)
        machine.wallet = [5, 5, 5, 5]
        print(machine.makePayment(18, 'Lays', 1, 1, 1, 1))
        self.assertTrue(machine.makePayment(1000, 'Simba', 10, 10,
                                            10, 10) == "Invalid coins specified, Complete refund")
        self.assertTrue(machine.makePayment(1000, 'Simba', 4, 4,
                                            4, 4) == "Item out of stock, Complete refund")
        self.assertTrue(machine.makePayment(1000, 'Not an item',
                                            4, 4, 4, 4) == "Invalid item selected, Complete refund")
        self.assertTrue(machine.makePayment(1, 'Lays', 1, 0, 0, 0)
                        == "Invalid cash amount, Complete refund")
        self.assertTrue(machine.makePayment(18, 'Lays', 1, 1, 1, 1) ==
                        "You have successfully purchased item = Lays Your change is = R11: 1 x R1, 0 x R2, 0 x R5, 1 x R10 ")

    """
    -   Test to see if the progress bar closes properly
    """
    def test_z_close_app(self):
        print("Closing machine progress bar")
        self.assertTrue(machine.close_app())


if __name__ == "__main__":
    unittest.main()
