"""
Gumball Vending Machine Simulator

- Two gumball types: Red (5¢) and Yellow (10¢)
- Accepts nickels (5¢), dimes (10¢), and quarters (25¢)
- Invalid coins are rejected immediately
- Two dispensing levers (Red / Yellow)
- One gumball dispensed per lever pull
- "Return My Change" lever returns remaining balance
- Unlimited gumballs and change assumed
"""

VALID_COINS = {
    "nickel": 5,
    "dime": 10,
    "quarter": 25,
}

GUMBALL_PRICES = {
    "red": 5,
    "yellow": 10,
}


class GumballMachine:
    def __init__(self):
        self.balance = 0  # cents

    def insert_coin(self, coin: str) -> dict:
        """Insert a coin. Returns result with accepted/rejected status."""
        coin = coin.strip().lower()
        if coin in VALID_COINS:
            self.balance += VALID_COINS[coin]
            return {
                "accepted": True,
                "coin": coin,
                "value": VALID_COINS[coin],
                "balance": self.balance,
            }
        return {
            "accepted": False,
            "coin": coin,
            "balance": self.balance,
        }

    def dispense(self, color: str) -> dict:
        """Pull a dispenser lever. Returns result with success/failure."""
        color = color.strip().lower()
        if color not in GUMBALL_PRICES:
            return {
                "dispensed": False,
                "reason": f"Unknown gumball type: {color}",
                "balance": self.balance,
            }
        price = GUMBALL_PRICES[color]
        if self.balance < price:
            return {
                "dispensed": False,
                "reason": f"Insufficient balance. Need {price}¢, have {self.balance}¢.",
                "balance": self.balance,
            }
        self.balance -= price
        return {
            "dispensed": True,
            "color": color,
            "price": price,
            "balance": self.balance,
        }

    def return_change(self) -> dict:
        """Pull the 'Return My Change' lever."""
        change = self.balance
        self.balance = 0
        quarters, remainder = divmod(change, 25)
        dimes, remainder = divmod(remainder, 10)
        nickels = remainder // 5
        return {
            "returned": change,
            "breakdown": {
                "quarters": quarters,
                "dimes": dimes,
                "nickels": nickels,
            },
            "balance": self.balance,
        }


# ── Terminal simulation ──────────────────────────────────────────────

def _format_cents(cents: int) -> str:
    """Format cents as a dollar string."""
    return f"${cents / 100:.2f}"


def _print_banner():
    print("=" * 50)
    print("       GUMBALL VENDING MACHINE")
    print("=" * 50)
    print("  Gumballs:  RED = 5¢  |  YELLOW = 10¢")
    print("  Coins:     nickel (5¢)  dime (10¢)  quarter (25¢)")
    print("=" * 50)


def _print_menu(balance: int):
    print()
    print(f"  Balance: {_format_cents(balance)}")
    print("  ─────────────────────────────────")
    print("  [1] Insert nickel")
    print("  [2] Insert dime")
    print("  [3] Insert quarter")
    print("  [4] Dispense RED gumball   (5¢)")
    print("  [5] Dispense YELLOW gumball (10¢)")
    print("  [6] Return my change")
    print("  [7] Quit")
    print()


def main():
    machine = GumballMachine()
    _print_banner()

    while True:
        _print_menu(machine.balance)
        choice = input("  Choose [1-7]: ").strip()

        if choice == "1":
            result = machine.insert_coin("nickel")
            print(f"  >> Inserted nickel. Balance: {_format_cents(result['balance'])}")

        elif choice == "2":
            result = machine.insert_coin("dime")
            print(f"  >> Inserted dime. Balance: {_format_cents(result['balance'])}")

        elif choice == "3":
            result = machine.insert_coin("quarter")
            print(f"  >> Inserted quarter. Balance: {_format_cents(result['balance'])}")

        elif choice == "4":
            result = machine.dispense("red")
            if result["dispensed"]:
                print(f"  >> *clunk* A RED gumball rolls out! Balance: {_format_cents(result['balance'])}")
            else:
                print(f"  >> {result['reason']}")

        elif choice == "5":
            result = machine.dispense("yellow")
            if result["dispensed"]:
                print(f"  >> *clunk* A YELLOW gumball rolls out! Balance: {_format_cents(result['balance'])}")
            else:
                print(f"  >> {result['reason']}")

        elif choice == "6":
            result = machine.return_change()
            if result["returned"] == 0:
                print("  >> No change to return.")
            else:
                b = result["breakdown"]
                parts = []
                if b["quarters"]:
                    parts.append(f"{b['quarters']} quarter(s)")
                if b["dimes"]:
                    parts.append(f"{b['dimes']} dime(s)")
                if b["nickels"]:
                    parts.append(f"{b['nickels']} nickel(s)")
                print(f"  >> Returned {_format_cents(result['returned'])}: {', '.join(parts)}")

        elif choice == "7":
            if machine.balance > 0:
                result = machine.return_change()
                b = result["breakdown"]
                parts = []
                if b["quarters"]:
                    parts.append(f"{b['quarters']} quarter(s)")
                if b["dimes"]:
                    parts.append(f"{b['dimes']} dime(s)")
                if b["nickels"]:
                    parts.append(f"{b['nickels']} nickel(s)")
                print(f"  >> Returning your change: {_format_cents(result['returned'])} ({', '.join(parts)})")
            print("  >> Goodbye!")
            break

        else:
            print("  >> Invalid choice. Please pick 1-7.")


if __name__ == "__main__":
    main()
