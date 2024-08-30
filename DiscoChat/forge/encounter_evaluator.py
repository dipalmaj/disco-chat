class EncounterEvaluator:
    def __init__(self, party_dpr: List[DPRCalculator], enemy_hp: List[int]):
        """
        Initialize the Encounter Evaluator.
        :param party_dpr: A list of DPRCalculator instances for each party member.
        :param enemy_hp: A list of hit points for each enemy.
        """
        self.party_dpr = party_dpr
        self.enemy_hp = enemy_hp

    def calculate_party_dpr(self) -> float:
        """
        Calculate the total DPR for the party.
        :return: The total party DPR as a float.
        """
        total_dpr = sum(dpr.expected_dpr() for dpr in self.party_dpr)
        return total_dpr

    def evaluate_encounter(self) -> float:
        """
        Evaluate the encounter by calculating the time it would take for the party to defeat the enemies.
        :return: The number of rounds required to defeat all enemies.
        """
        total_enemy_hp = sum(self.enemy_hp)
        party_dpr = self.calculate_party_dpr()

        if party_dpr == 0:
            return float('inf')  # If the party cannot deal damage, the encounter is impossible

        rounds_to_defeat = total_enemy_hp / party_dpr
        return rounds_to_defeat


# Example usage of Encounter Evaluator:
party_dpr_calculators = [
    DPRCalculator(attack_bonus=7, target_ac=15, damage_dice=Dice.from_string('1d8+3'), num_attacks=2),
    DPRCalculator(attack_bonus=5, target_ac=15, damage_dice=Dice.from_string('1d6+2'), num_attacks=1),
]

enemy_hp = [30, 45, 50]  # Example enemy hit points

encounter_evaluator = EncounterEvaluator(party_dpr=party_dpr_calculators, enemy_hp=enemy_hp)
rounds_needed = encounter_evaluator.evaluate_encounter()

print(f"Rounds needed to defeat all enemies: {rounds_needed:.2f}")