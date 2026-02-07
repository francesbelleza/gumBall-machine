"""Unit tests for GumballMachine."""

import unittest
from gumball_machine import GumballMachine


class Test01InsertCoin(unittest.TestCase):
    def setUp(self):
        self.machine = GumballMachine()

    def test_insert_nickel(self):
        """Test that inserting a nickel increases balance by 5."""
        result = self.machine.insert_coin("nickel")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["value"], 5)
        self.assertEqual(result["balance"], 5)

    def test_insert_dime(self):
        """Test that inserting a dime increases balance by 10."""
        result = self.machine.insert_coin("dime")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["value"], 10)
        self.assertEqual(result["balance"], 10)

    def test_insert_quarter(self):
        """Test that inserting a quarter increases balance by 25."""
        result = self.machine.insert_coin("quarter")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["value"], 25)
        self.assertEqual(result["balance"], 25)

    def test_insert_invalid_coin_penny(self):
        """Test that inserting a penny, balance will not increase and coin rejected."""
        result = self.machine.insert_coin("penny")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["balance"], 0)

    def test_insert_invalid_coin_dollar(self):
        """Test that inserting a dollar, balance will not increase and coin rejected."""
        result = self.machine.insert_coin("dollar")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["balance"], 0)

    def test_insert_invalid_coin_random_string(self):
        """Test that inserting invalid coin, balance will not increase and coin rejected."""
        result = self.machine.insert_coin("banana")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["balance"], 0)

    def test_insert_multiple_coins(self):
        """Test that inserting multiple coins: 1 nickel + 1 dime + 1 quarter = 40 cents"""
        self.machine.insert_coin("nickel")
        self.machine.insert_coin("dime")
        result = self.machine.insert_coin("quarter")
        self.assertEqual(result["balance"], 40)

    def test_insert_coin_case_insensitive(self):
        """Test that coin is case insensitive"""
        result = self.machine.insert_coin("NICKEL")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["balance"], 5)

    def test_insert_coin_with_whitespace(self):
        """Test whitespace handling"""
        result = self.machine.insert_coin("  dime  ")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["balance"], 10)
    
    def test_insert_coin_with_mix_case(self):
        """Test mix case handling"""
        result = self.machine.insert_coin("NiCKeL")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["balance"], 5)

class Test02Dispense(unittest.TestCase):
    def setUp(self):
        self.machine = GumballMachine()

    def test_dispense_red_with_exact_change(self):
        """Test dispense red with exact change"""
        self.machine.insert_coin("nickel")
        result = self.machine.dispense("red")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["color"], "red")
        self.assertEqual(result["price"], 5)
        self.assertEqual(result["balance"], 0)

    def test_dispense_yellow_with_exact_change(self):
        """Test dispense yellow with exact change"""
        self.machine.insert_coin("dime")
        result = self.machine.dispense("yellow")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["color"], "yellow")
        self.assertEqual(result["price"], 10)
        self.assertEqual(result["balance"], 0)

    def test_dispense_red_insufficient_balance(self):
        """Test dispense red with insufficient balance"""
        result = self.machine.dispense("red")
        self.assertFalse(result["dispensed"])
        self.assertIn("Insufficient", result["reason"])
        self.assertEqual(result["balance"], 0)

    def test_dispense_yellow_insufficient_balance(self):
        """Test dispense yellow with insufficient balance"""
        self.machine.insert_coin("nickel")
        result = self.machine.dispense("yellow")
        self.assertFalse(result["dispensed"])
        self.assertIn("Insufficient", result["reason"])
        self.assertEqual(result["balance"], 5)

    def test_dispense_unknown_type(self):
        """Test dispense unknown type of gumball"""
        self.machine.insert_coin("quarter")
        result = self.machine.dispense("blue")
        self.assertFalse(result["dispensed"])
        self.assertIn("Unknown", result["reason"])
        self.assertEqual(result["balance"], 25)

    def test_dispense_red_with_overpay(self):
        """Test dispense ted with overpay"""
        self.machine.insert_coin("quarter")
        result = self.machine.dispense("red")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["balance"], 20)

    def test_dispense_yellow_with_overpay(self):
        """Test dispense yellow with overpay"""
        self.machine.insert_coin("quarter")
        result = self.machine.dispense("yellow")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["balance"], 15)

    # def test_dispense_case_insensitive(self):
    #     self.machine.insert_coin("nickel")
    #     result = self.machine.dispense("RED")
    #     self.assertTrue(result["dispensed"])

    # def test_dispense_multiple_reds_from_quarter(self):
    #     """Quarter (25¢) → two reds (5¢ each) → 15¢ remaining."""
    #     self.machine.insert_coin("quarter")
    #     r1 = self.machine.dispense("red")
    #     self.assertTrue(r1["dispensed"])
    #     self.assertEqual(r1["balance"], 20)
    #     r2 = self.machine.dispense("red")
    #     self.assertTrue(r2["dispensed"])
    #     self.assertEqual(r2["balance"], 15)

    # def test_dispense_multiple_yellows_from_quarter(self):
    #     """Quarter (25¢) → two yellows (10¢ each) → 5¢ remaining."""
    #     self.machine.insert_coin("quarter")
    #     r1 = self.machine.dispense("yellow")
    #     self.assertTrue(r1["dispensed"])
    #     self.assertEqual(r1["balance"], 15)
    #     r2 = self.machine.dispense("yellow")
    #     self.assertTrue(r2["dispensed"])
    #     self.assertEqual(r2["balance"], 5)

    # def test_dispense_mix_red_and_yellow(self):
    #     """Quarter (25¢) → 1 yellow (10¢) + 1 red (5¢) → 10¢ remaining."""
    #     self.machine.insert_coin("quarter")
    #     self.machine.dispense("yellow")
    #     result = self.machine.dispense("red")
    #     self.assertTrue(result["dispensed"])
    #     self.assertEqual(result["balance"], 10)

    # def test_dispense_until_insufficient(self):
    #     """Insert dime, dispense yellow, then fail on second yellow."""
    #     self.machine.insert_coin("dime")
    #     r1 = self.machine.dispense("yellow")
    #     self.assertTrue(r1["dispensed"])
    #     r2 = self.machine.dispense("yellow")
    #     self.assertFalse(r2["dispensed"])
    #     self.assertEqual(r2["balance"], 0)


class Test03ReturnChange(unittest.TestCase):
    def setUp(self):
        self.machine = GumballMachine()

    def test_return_change_no_balance(self):
        """Test return change with no balance"""
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 0)
        self.assertEqual(result["balance"], 0)

    def test_return_change_nickel(self):
        """Test return nickel"""
        self.machine.insert_coin("nickel")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 5)
        self.assertEqual(result["breakdown"]["nickels"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_dime(self):
        """Test return dime"""
        self.machine.insert_coin("dime")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 10)
        self.assertEqual(result["breakdown"]["dimes"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_quarter(self):
        """Test return quarter"""
        self.machine.insert_coin("quarter")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 25)
        self.assertEqual(result["breakdown"]["quarters"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_after_partial_spend(self):
        """Test return change after partial spend Quarter → 2 reds → return 15¢ (1 dime + 1 nickel)."""
        self.machine.insert_coin("quarter")
        self.machine.dispense("red")
        self.machine.dispense("red")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 15)
        self.assertEqual(result["breakdown"]["dimes"], 1)
        self.assertEqual(result["breakdown"]["nickels"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_large_amount(self):
        """Test return change in large amount (75 cents) → return 75¢ (3 quarters)"""
        self.machine.insert_coin("quarter")
        self.machine.insert_coin("quarter")
        self.machine.insert_coin("quarter")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 75)
        self.assertEqual(result["breakdown"]["quarters"], 3)
        self.assertEqual(result["balance"], 0)

    def test_return_change_resets_balance(self):
        """Test return change reset the balance"""
        self.machine.insert_coin("quarter")
        self.machine.return_change()
        self.assertEqual(self.machine.balance, 0)
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 0)

    def test_return_change_breakdown_40_cents(self):
        """Test return change breakdown 40 cents: 40¢ = 1 quarter + 1 dime + 1 nickel."""
        self.machine.insert_coin("quarter")
        self.machine.insert_coin("dime")
        self.machine.insert_coin("nickel")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 40)
        self.assertEqual(result["breakdown"]["quarters"], 1)
        self.assertEqual(result["breakdown"]["dimes"], 1)
        self.assertEqual(result["breakdown"]["nickels"], 1)


# class TestFullScenarios(unittest.TestCase):
#     """End-to-end workflow tests."""

#     def setUp(self):
#         self.machine = GumballMachine()

#     def test_scenario_quarter_two_reds_return_change(self):
#         """The exact scenario from the spec:
#         Insert quarter → dispense 2 reds → return 15¢."""
#         self.machine.insert_coin("quarter")
#         self.machine.dispense("red")
#         self.machine.dispense("red")
#         result = self.machine.return_change()
#         self.assertEqual(result["returned"], 15)

#     def test_scenario_insert_coins_then_invalid_dispense(self):
#         """Insert coins, try invalid lever, balance unchanged."""
#         self.machine.insert_coin("dime")
#         result = self.machine.dispense("green")
#         self.assertFalse(result["dispensed"])
#         self.assertEqual(result["balance"], 10)

#     def test_scenario_no_coins_dispense_fails(self):
#         r = self.machine.dispense("red")
#         self.assertFalse(r["dispensed"])
#         r = self.machine.dispense("yellow")
#         self.assertFalse(r["dispensed"])

#     def test_scenario_invalid_coin_then_valid_dispense(self):
#         """Invalid coin rejected, then valid coin inserted and dispensed."""
#         self.machine.insert_coin("peso")
#         self.assertEqual(self.machine.balance, 0)
#         self.machine.insert_coin("nickel")
#         result = self.machine.dispense("red")
#         self.assertTrue(result["dispensed"])
#         self.assertEqual(result["balance"], 0)

#     def test_scenario_multiple_transactions(self):
#         """Simulate multiple insert-dispense-return cycles."""
#         # Transaction 1
#         self.machine.insert_coin("quarter")
#         self.machine.dispense("yellow")
#         self.machine.return_change()
#         self.assertEqual(self.machine.balance, 0)

#         # Transaction 2
#         self.machine.insert_coin("dime")
#         self.machine.insert_coin("nickel")
#         self.machine.dispense("red")
#         self.machine.dispense("yellow")
#         self.assertEqual(self.machine.balance, 0)

#     def test_scenario_exact_change_no_remainder(self):
#         """Insert exact amount for yellow, nothing left."""
#         self.machine.insert_coin("nickel")
#         self.machine.insert_coin("nickel")
#         result = self.machine.dispense("yellow")
#         self.assertTrue(result["dispensed"])
#         self.assertEqual(result["balance"], 0)
#         change = self.machine.return_change()
#         self.assertEqual(change["returned"], 0)

class NumberedTextTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_count = 0

    def getDescription(self, test):
        """Overrides the default name and returns ONLY the docstring."""
        doc = test.shortDescription()
        # If a docstring exists, return it; otherwise, fall back to the function name
        return doc if doc else str(test)

    def startTest(self, test):
        self.test_count += 1
        # Prints the number before the description
        self.stream.write(f"{self.test_count}. ")
        self.stream.flush()
        super().startTest(test)
class NumberedTestRunner(unittest.TextTestRunner):
    resultclass = NumberedTextTestResult

def suite():
    suite = unittest.TestSuite()
    
    # 1. Insert Tests - Manually ordered
    suite.addTest(Test01InsertCoin('test_insert_nickel'))
    suite.addTest(Test01InsertCoin('test_insert_dime'))
    suite.addTest(Test01InsertCoin('test_insert_quarter'))
    suite.addTest(Test01InsertCoin('test_insert_invalid_coin_penny'))
    suite.addTest(Test01InsertCoin('test_insert_invalid_coin_dollar'))
    suite.addTest(Test01InsertCoin('test_insert_invalid_coin_random_string'))
    suite.addTest(Test01InsertCoin('test_insert_multiple_coins'))
    suite.addTest(Test01InsertCoin('test_insert_coin_case_insensitive'))
    suite.addTest(Test01InsertCoin('test_insert_coin_with_whitespace'))
    suite.addTest(Test01InsertCoin('test_insert_coin_with_mix_case'))

    # 2. Dispense Tests
    suite.addTest(Test02Dispense('test_dispense_red_with_exact_change'))
    suite.addTest(Test02Dispense('test_dispense_yellow_with_exact_change'))
    suite.addTest(Test02Dispense('test_dispense_red_insufficient_balance'))
    suite.addTest(Test02Dispense('test_dispense_yellow_insufficient_balance'))
    suite.addTest(Test02Dispense('test_dispense_unknown_type'))
    suite.addTest(Test02Dispense('test_dispense_red_with_overpay'))
    suite.addTest(Test02Dispense('test_dispense_yellow_with_overpay'))

    # 3. Return Change Tests
    suite.addTest(Test03ReturnChange('test_return_change_no_balance'))
    suite.addTest(Test03ReturnChange('test_return_change_nickel'))
    suite.addTest(Test03ReturnChange('test_return_change_dime'))
    suite.addTest(Test03ReturnChange('test_return_change_quarter'))
    suite.addTest(Test03ReturnChange('test_return_change_after_partial_spend'))
    suite.addTest(Test03ReturnChange('test_return_change_large_amount'))
    suite.addTest(Test03ReturnChange('test_return_change_resets_balance'))
    suite.addTest(Test03ReturnChange('test_return_change_breakdown_40_cents'))

    return suite

if __name__ == "__main__":
    runner = NumberedTestRunner(verbosity=2)
    runner.run(suite())