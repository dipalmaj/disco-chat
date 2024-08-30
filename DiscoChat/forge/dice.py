# Let's enhance the `Dice` class to include a constructor that can create an instance from a string representation.
# We'll also update the `__repr__` method to provide a string representation that includes advanced cases like "keep highest".
# Finally, we'll add a function that returns all known advanced cases and their corresponding short string keys.

import re
from typing import Optional


class Dice:
    def __init__(self, num: int, die: int, modifier: int = 0, keep: Optional[str] = None, advantage: Optional[bool] = None):
        """
        Initialize a Dice object.
        :param num: Number of dice to roll (e.g., 2 in 2d6).
        :param die: Type of die (e.g., 6 in 2d6).
        :param modifier: A modifier to add/subtract to the final roll.
        :param keep: String indicating to keep highest (kh) or lowest (kl).
        :param advantage: Boolean indicating if roll has advantage (True) or disadvantage (False).
        """
        self.num = num
        self.die = die
        self.modifier = modifier
        self.keep = keep
        self.advantage = advantage

    @classmethod
    def from_string(cls, dice_str: str):
        """
        Create a Dice object from a string representation.
        Examples:
        - '2d6+3'
        - '2d6kh' (keep highest)
        - '2d6kl' (keep lowest)
        - '2d6adv' (advantage)
        - '2d6dis' (disadvantage)
        """
        pattern = r"(\d+)d(\d+)([+-]\d+)?(kh|kl|adv|dis)?"
        match = re.match(pattern, dice_str)
        if not match:
            raise ValueError("Invalid dice string format.")

        num = int(match.group(1))
        die = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        keep_or_adv = match.group(4)

        keep = None
        advantage = None

        if keep_or_adv == "kh":
            keep = "kh"
        elif keep_or_adv == "kl":
            keep = "kl"
        elif keep_or_adv == "adv":
            advantage = True
        elif keep_or_adv == "dis":
            advantage = False

        return cls(num, die, modifier, keep, advantage)

    def roll(self) -> int:
        """
        Roll the dice and return the result.
        :return: The sum of the rolls plus the modifier.
        """
        total = sum(random.randint(1, self.die) for _ in range(self.num))
        return total + self.modifier

    def roll_with_advantage(self, advantage: bool = True) -> int:
        """
        Roll the dice with advantage (keep the highest) or disadvantage (keep the lowest).
        :param advantage: True for advantage (default), False for disadvantage.
        :return: The result of the roll with advantage/disadvantage applied.
        """
        rolls = [self.roll() - self.modifier for _ in range(2)]
        result = max(rolls) if advantage else min(rolls)
        return result + self.modifier

    def roll_keep_highest(self) -> int:
        """
        Roll the dice and keep the highest roll.
        :return: The sum of the highest rolls plus the modifier.
        """
        rolls = [random.randint(1, self.die) for _ in range(self.num)]
        return sum(sorted(rolls, reverse=True)[:1]) + self.modifier

    def roll_keep_lowest(self) -> int:
        """
        Roll the dice and keep the lowest roll.
        :return: The sum of the lowest rolls plus the modifier.
        """
        rolls = [random.randint(1, self.die) for _ in range(self.num)]
        return sum(sorted(rolls)[:1]) + self.modifier

    def average_roll(self) -> float:
        """
        Calculate the average result of the roll.
        :return: The average result as a float.
        """
        avg_roll = (self.num * (1 + self.die)) / 2
        return avg_roll + self.modifier

    def __repr__(self) -> str:
        """
        Provide a string representation of the Dice object, e.g., '2d6+3', '2d6kh' for keep highest, etc.
        :return: A string representing the dice.
        """
        base = f"{self.num}d{self.die}"
        if self.keep == "kh":
            base += "kh"
        if self.keep == "kl":
            base += "kl"
        if self.advantage is True:
            base += "adv"
        if self.advantage is False:
            base += "dis"
        
        return f"{base}{f'+{self.modifier}' if self.modifier != 0 else ''}"

    @staticmethod
    def get_known_advanced_cases() -> dict:
        """
        Return a dictionary of known advanced cases and their short string keys.
        :return: Dictionary with descriptions as keys and short string keys as values.
        """
        return {
            "keep highest": "kh",
            "keep lowest": "kl",
            "advantage": "adv",
            "disadvantage": "dis"
        }


# Example Usage:
dice_standard = Dice(2, 6, 3)
print(f"Standard roll: {dice_standard.roll()}")  # Standard roll

dice_adv = Dice.from_string("2d6adv")
print(f"Advantage roll {dice_adv}: {dice_adv.roll_with_advantage()}")

dice_kl = Dice.from_string("2d6kl")
print(f"Keep lowest roll {dice_kl}: {dice_kl.roll_keep_lowest()}")

known_cases = Dice.get_known_advanced_cases()
print(f"Known advanced cases: {known_cases}")