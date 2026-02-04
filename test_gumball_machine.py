"""Unit tests for GumballMachine."""

import unittest
from gumball_machine import GumballMachine


class TestInsertCoin(unittest.TestCase):
    def setUp(self):
        self.machine = GumballMachine()

    def test_insert_nickel(self):
        result = self.machine.insert_coin("nickel")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["value"], 5)
        self.assertEqual(result["balance"], 5)

    def test_insert_dime(self):
        result = self.machine.insert_coin("dime")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["value"], 10)
        self.assertEqual(result["balance"], 10)

    def test_insert_quarter(self):
        result = self.machine.insert_coin("quarter")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["value"], 25)
        self.assertEqual(result["balance"], 25)

    def test_insert_invalid_coin_penny(self):
        result = self.machine.insert_coin("penny")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["balance"], 0)

    def test_insert_invalid_coin_dollar(self):
        result = self.machine.insert_coin("dollar")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["balance"], 0)

    def test_insert_invalid_coin_random_string(self):
        result = self.machine.insert_coin("banana")
        self.assertFalse(result["accepted"])
        self.assertEqual(result["balance"], 0)

    def test_insert_multiple_coins(self):
        self.machine.insert_coin("nickel")
        self.machine.insert_coin("dime")
        result = self.machine.insert_coin("quarter")
        self.assertEqual(result["balance"], 40)

    def test_insert_coin_case_insensitive(self):
        result = self.machine.insert_coin("NICKEL")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["balance"], 5)

    def test_insert_coin_with_whitespace(self):
        result = self.machine.insert_coin("  dime  ")
        self.assertTrue(result["accepted"])
        self.assertEqual(result["balance"], 10)


class TestDispense(unittest.TestCase):
    def setUp(self):
        self.machine = GumballMachine()

    def test_dispense_red_with_exact_change(self):
        self.machine.insert_coin("nickel")
        result = self.machine.dispense("red")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["color"], "red")
        self.assertEqual(result["price"], 5)
        self.assertEqual(result["balance"], 0)

    def test_dispense_yellow_with_exact_change(self):
        self.machine.insert_coin("dime")
        result = self.machine.dispense("yellow")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["color"], "yellow")
        self.assertEqual(result["price"], 10)
        self.assertEqual(result["balance"], 0)

    def test_dispense_red_insufficient_balance(self):
        result = self.machine.dispense("red")
        self.assertFalse(result["dispensed"])
        self.assertIn("Insufficient", result["reason"])
        self.assertEqual(result["balance"], 0)

    def test_dispense_yellow_insufficient_balance(self):
        self.machine.insert_coin("nickel")
        result = self.machine.dispense("yellow")
        self.assertFalse(result["dispensed"])
        self.assertIn("Insufficient", result["reason"])
        self.assertEqual(result["balance"], 5)

    def test_dispense_unknown_type(self):
        self.machine.insert_coin("quarter")
        result = self.machine.dispense("blue")
        self.assertFalse(result["dispensed"])
        self.assertIn("Unknown", result["reason"])
        self.assertEqual(result["balance"], 25)

    def test_dispense_red_with_overpay(self):
        self.machine.insert_coin("quarter")
        result = self.machine.dispense("red")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["balance"], 20)

    def test_dispense_yellow_with_overpay(self):
        self.machine.insert_coin("quarter")
        result = self.machine.dispense("yellow")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["balance"], 15)

    def test_dispense_case_insensitive(self):
        self.machine.insert_coin("nickel")
        result = self.machine.dispense("RED")
        self.assertTrue(result["dispensed"])

    def test_dispense_multiple_reds_from_quarter(self):
        """Quarter (25¢) → two reds (5¢ each) → 15¢ remaining."""
        self.machine.insert_coin("quarter")
        r1 = self.machine.dispense("red")
        self.assertTrue(r1["dispensed"])
        self.assertEqual(r1["balance"], 20)
        r2 = self.machine.dispense("red")
        self.assertTrue(r2["dispensed"])
        self.assertEqual(r2["balance"], 15)

    def test_dispense_multiple_yellows_from_quarter(self):
        """Quarter (25¢) → two yellows (10¢ each) → 5¢ remaining."""
        self.machine.insert_coin("quarter")
        r1 = self.machine.dispense("yellow")
        self.assertTrue(r1["dispensed"])
        self.assertEqual(r1["balance"], 15)
        r2 = self.machine.dispense("yellow")
        self.assertTrue(r2["dispensed"])
        self.assertEqual(r2["balance"], 5)

    def test_dispense_mix_red_and_yellow(self):
        """Quarter (25¢) → 1 yellow (10¢) + 1 red (5¢) → 10¢ remaining."""
        self.machine.insert_coin("quarter")
        self.machine.dispense("yellow")
        result = self.machine.dispense("red")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["balance"], 10)

    def test_dispense_until_insufficient(self):
        """Insert dime, dispense yellow, then fail on second yellow."""
        self.machine.insert_coin("dime")
        r1 = self.machine.dispense("yellow")
        self.assertTrue(r1["dispensed"])
        r2 = self.machine.dispense("yellow")
        self.assertFalse(r2["dispensed"])
        self.assertEqual(r2["balance"], 0)


class TestReturnChange(unittest.TestCase):
    def setUp(self):
        self.machine = GumballMachine()

    def test_return_change_no_balance(self):
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 0)
        self.assertEqual(result["balance"], 0)

    def test_return_change_nickel(self):
        self.machine.insert_coin("nickel")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 5)
        self.assertEqual(result["breakdown"]["nickels"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_dime(self):
        self.machine.insert_coin("dime")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 10)
        self.assertEqual(result["breakdown"]["dimes"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_quarter(self):
        self.machine.insert_coin("quarter")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 25)
        self.assertEqual(result["breakdown"]["quarters"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_after_partial_spend(self):
        """Quarter → 2 reds → return 15¢ (1 dime + 1 nickel)."""
        self.machine.insert_coin("quarter")
        self.machine.dispense("red")
        self.machine.dispense("red")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 15)
        self.assertEqual(result["breakdown"]["dimes"], 1)
        self.assertEqual(result["breakdown"]["nickels"], 1)
        self.assertEqual(result["balance"], 0)

    def test_return_change_large_amount(self):
        """3 quarters = 75¢ → return 75¢ (3 quarters)."""
        self.machine.insert_coin("quarter")
        self.machine.insert_coin("quarter")
        self.machine.insert_coin("quarter")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 75)
        self.assertEqual(result["breakdown"]["quarters"], 3)
        self.assertEqual(result["balance"], 0)

    def test_return_change_resets_balance(self):
        self.machine.insert_coin("quarter")
        self.machine.return_change()
        self.assertEqual(self.machine.balance, 0)
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 0)

    def test_return_change_breakdown_40_cents(self):
        """40¢ = 1 quarter + 1 dime + 1 nickel."""
        self.machine.insert_coin("quarter")
        self.machine.insert_coin("dime")
        self.machine.insert_coin("nickel")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 40)
        self.assertEqual(result["breakdown"]["quarters"], 1)
        self.assertEqual(result["breakdown"]["dimes"], 1)
        self.assertEqual(result["breakdown"]["nickels"], 1)


class TestFullScenarios(unittest.TestCase):
    """End-to-end workflow tests."""

    def setUp(self):
        self.machine = GumballMachine()

    def test_scenario_quarter_two_reds_return_change(self):
        """The exact scenario from the spec:
        Insert quarter → dispense 2 reds → return 15¢."""
        self.machine.insert_coin("quarter")
        self.machine.dispense("red")
        self.machine.dispense("red")
        result = self.machine.return_change()
        self.assertEqual(result["returned"], 15)

    def test_scenario_insert_coins_then_invalid_dispense(self):
        """Insert coins, try invalid lever, balance unchanged."""
        self.machine.insert_coin("dime")
        result = self.machine.dispense("green")
        self.assertFalse(result["dispensed"])
        self.assertEqual(result["balance"], 10)

    def test_scenario_no_coins_dispense_fails(self):
        r = self.machine.dispense("red")
        self.assertFalse(r["dispensed"])
        r = self.machine.dispense("yellow")
        self.assertFalse(r["dispensed"])

    def test_scenario_invalid_coin_then_valid_dispense(self):
        """Invalid coin rejected, then valid coin inserted and dispensed."""
        self.machine.insert_coin("peso")
        self.assertEqual(self.machine.balance, 0)
        self.machine.insert_coin("nickel")
        result = self.machine.dispense("red")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["balance"], 0)

    def test_scenario_multiple_transactions(self):
        """Simulate multiple insert-dispense-return cycles."""
        # Transaction 1
        self.machine.insert_coin("quarter")
        self.machine.dispense("yellow")
        self.machine.return_change()
        self.assertEqual(self.machine.balance, 0)

        # Transaction 2
        self.machine.insert_coin("dime")
        self.machine.insert_coin("nickel")
        self.machine.dispense("red")
        self.machine.dispense("yellow")
        self.assertEqual(self.machine.balance, 0)

    def test_scenario_exact_change_no_remainder(self):
        """Insert exact amount for yellow, nothing left."""
        self.machine.insert_coin("nickel")
        self.machine.insert_coin("nickel")
        result = self.machine.dispense("yellow")
        self.assertTrue(result["dispensed"])
        self.assertEqual(result["balance"], 0)
        change = self.machine.return_change()
        self.assertEqual(change["returned"], 0)


if __name__ == "__main__":
    unittest.main()
