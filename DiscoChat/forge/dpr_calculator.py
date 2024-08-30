class DPRCalculator:
    def __init__(self, attack_bonus: int, target_ac: int, damage_dice: Dice, num_attacks: int = 1, crit_range: int = 20, crit_bonus: Optional[Dice] = None):
        """
        Initialize the DPR Calculator.
        :param attack_bonus: The attack bonus (e.g., +7)
        :param target_ac: The target's Armor Class (AC)
        :param damage_dice: The Dice object representing damage dice.
        :param num_attacks: Number of attacks per round.
        :param crit_range: The range for a critical hit (default is 20).
        :param crit_bonus: A Dice object for extra damage dice on a critical hit (optional).
        """
        self.attack_bonus = attack_bonus
        self.target_ac = target_ac
        self.damage_dice = damage_dice
        self.num_attacks = num_attacks
        self.crit_range = crit_range
        self.crit_bonus = crit_bonus if crit_bonus else Dice(damage_dice.num, damage_dice.die, damage_dice.modifier)

    def hit_chance(self) -> float:
        """
        Calculate the probability of hitting a target with a given AC.
        :return: Probability of hitting as a float between 0.05 and 0.95.
        """
        hit_probability = (21 - self.target_ac + self.attack_bonus) / 20
        return max(min(hit_probability, 0.95), 0.05)  # hit chance between 5% and 95%

    def expected_dpr(self) -> float:
        """
        Calculate the expected Damage Per Round (DPR).
        :return: The expected DPR as a float.
        """
        # Average damage per hit
        avg_damage = self.damage_dice.average_roll()

        # Critical hit probability
        crit_chance = (21 - self.crit_range) / 20
        crit_damage = self.crit_bonus.average_roll()

        # Expected damage per attack considering crits
        expected_damage = (1 - crit_chance) * avg_damage + crit_chance * (avg_damage + crit_damage)

        # Hit chance
        hit_probability = self.hit_chance()

        # Total DPR considering number of attacks
        dpr = expected_damage * hit_probability * self.num_attacks
        return dpr


# Example usage of DPR Calculator:
damage_dice = Dice.from_string('1d8+3')
crit_bonus_dice = Dice.from_string('1d8')

dpr_calculator = DPRCalculator(
    attack_bonus=7,
    target_ac=15,
    damage_dice=damage_dice,
    num_attacks=2,
    crit_range=20,
    crit_bonus=crit_bonus_dice
)

print(f"Expected DPR: {dpr_calculator.expected_dpr():.2f}")