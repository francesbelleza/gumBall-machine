# Gumball Machine - Test Cases

## Coin Insertion Tests

| # | Test Case | Input | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Insert nickel | `insert_coin("nickel")` | Accepted, balance = 5¢ |
| 2 | Insert dime | `insert_coin("dime")` | Accepted, balance = 10¢ |
| 3 | Insert quarter | `insert_coin("quarter")` | Accepted, balance = 25¢ |
| 4 | Insert invalid coin (penny) | `insert_coin("penny")` | Rejected, balance = 0¢ |
| 5 | Insert invalid coin (dollar) | `insert_coin("dollar")` | Rejected, balance = 0¢ |
| 6 | Insert invalid coin (random string) | `insert_coin("banana")` | Rejected, balance = 0¢ |
| 7 | Insert multiple valid coins | nickel + dime + quarter | Balance = 40¢ |
| 8 | Case insensitivity | `insert_coin("NICKEL")` | Accepted, balance = 5¢ |
| 9 | Whitespace handling | `insert_coin("  dime  ")` | Accepted, balance = 10¢ |

## Dispensing Tests

| # | Test Case | Setup | Action | Expected Result |
|---|-----------|-------|--------|-----------------|
| 10 | Dispense red with exact change | Insert nickel (5¢) | `dispense("red")` | Dispensed, balance = 0¢ |
| 11 | Dispense yellow with exact change | Insert dime (10¢) | `dispense("yellow")` | Dispensed, balance = 0¢ |
| 12 | Dispense red with no balance | None | `dispense("red")` | Rejected — insufficient balance |
| 13 | Dispense yellow with insufficient balance | Insert nickel (5¢) | `dispense("yellow")` | Rejected — need 10¢, have 5¢ |
| 14 | Dispense unknown type | Insert quarter (25¢) | `dispense("blue")` | Rejected — unknown type, balance unchanged |
| 15 | Dispense red with overpay | Insert quarter (25¢) | `dispense("red")` | Dispensed, balance = 20¢ |
| 16 | Dispense yellow with overpay | Insert quarter (25¢) | `dispense("yellow")` | Dispensed, balance = 15¢ |
| 17 | Case insensitivity on lever | Insert nickel (5¢) | `dispense("RED")` | Dispensed |
| 18 | Multiple reds from quarter | Insert quarter (25¢) | `dispense("red")` x2 | Both dispensed, balance = 15¢ |
| 19 | Multiple yellows from quarter | Insert quarter (25¢) | `dispense("yellow")` x2 | Both dispensed, balance = 5¢ |
| 20 | Mix red and yellow | Insert quarter (25¢) | yellow + red | Both dispensed, balance = 10¢ |
| 21 | Dispense until insufficient | Insert dime (10¢) | `dispense("yellow")` x2 | First succeeds, second rejected |

## Return Change Tests

| # | Test Case | Setup | Expected Result |
|---|-----------|-------|-----------------|
| 22 | Return change with no balance | None | Returned 0¢ |
| 23 | Return nickel | Insert nickel | Returned 5¢ (1 nickel) |
| 24 | Return dime | Insert dime | Returned 10¢ (1 dime) |
| 25 | Return quarter | Insert quarter | Returned 25¢ (1 quarter) |
| 26 | Return after partial spend (spec scenario) | Quarter → 2 reds | Returned 15¢ (1 dime + 1 nickel) |
| 27 | Return large amount | 3 quarters | Returned 75¢ (3 quarters) |
| 28 | Return resets balance to zero | Insert quarter → return | Balance = 0¢; second return = 0¢ |
| 29 | Breakdown for 40¢ | quarter + dime + nickel | 1 quarter + 1 dime + 1 nickel |

## End-to-End Scenario Tests

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 30 | Spec scenario: quarter → 2 reds → change | Insert quarter, pull red lever twice, return change | 2 reds dispensed, 15¢ returned |
| 31 | Invalid lever then valid action | Insert dime, dispense "green" | Rejected, balance still 10¢ |
| 32 | No coins → dispense fails | Pull red and yellow levers | Both rejected |
| 33 | Invalid coin then valid dispense | Insert "peso" (rejected), insert nickel, dispense red | Red dispensed, balance = 0¢ |
| 34 | Multiple transactions in sequence | Txn1: quarter → yellow → return; Txn2: dime + nickel → red + yellow | Both transactions succeed, balance ends at 0¢ |
| 35 | Exact change leaves nothing | 2 nickels → dispense yellow | Dispensed, balance = 0¢, return change = 0¢ |
