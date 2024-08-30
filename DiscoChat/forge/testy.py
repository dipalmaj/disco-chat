import unittest

class TestDiceAndDPR(unittest.TestCase):

    def test_dice_roll(self):
        dice = Dice(1, 6)
        result = dice.roll()
        self.assertTrue(1 <= result <= 6)

    def test_dice_average_roll(self):
        dice = Dice(2, 6)
        expected_avg = 7.0  # Average of 2d6 is (1+6)/2 * 2
        self.assertAlmostEqual(dice.average_roll(), expected_avg)

    def test_dice_from_string(self):
        dice = Dice.from_string('2d8+3')
        self.assertEqual(dice.num, 2)
        self.assertEqual(dice.die, 8)
        self.assertEqual(dice.modifier, 3)
        self.assertIsNone(dice.keep)
        self.assertIsNone(dice.advantage)

        dice_adv = Dice.from_string('2d8adv')
        self.assertEqual(dice_adv.advantage, True)

        dice_kl = Dice.from_string('2d8kl')
        self.assertEqual(dice_kl.keep, 'kl')

    def test_dpr_calculator(self):
        damage_dice = Dice(1, 8, 3)
        crit_bonus_dice = Dice(1, 8)
        dpr_calculator = DPRCalculator(attack_bonus=5, target_ac=15, damage_dice=damage_dice, num_attacks=2, crit_range=20, crit_bonus=crit_bonus_dice)
        expected_dpr = dpr_calculator.expected_dpr()
        self.assertTrue(expected_dpr > 0)

    def test_encounter_evaluator(self):
        party_dpr_calculators = [
            DPRCalculator(attack_bonus=7, target_ac=15, damage_dice=Dice.from_string('1d8+3'), num_attacks=2),
            DPRCalculator(attack_bonus=5, target_ac=15, damage_dice=Dice.from_string('1d6+2'), num_attacks=1),
        ]
        enemy_hp = [30, 45, 50]

        encounter_evaluator = EncounterEvaluator(party_dpr=party_dpr_calculators, enemy_hp=enemy_hp)
        rounds_needed = encounter_evaluator.evaluate_encounter()

        self.assertTrue(rounds_needed > 0)

    def test_encounter_generator(self):
        """
        This test checks the output of the DPR and Encounter Evaluation
        over multiple generated encounter scenarios.
        """
        def encounter_generator(num_tests):
            for _ in range(num_tests):
                # Randomized encounter scenario
                party_dpr_calculators = [
                    DPRCalculator(attack_bonus=random.randint(5, 10),
                                  target_ac=random.randint(10, 20),
                                  damage_dice=Dice.from_string(f"{random.randint(1, 2)}d{random.randint(4, 12)}+{random.randint(1, 5)}"),
                                  num_attacks=random.randint(1, 3))
                    for _ in range(random.randint(1, 4))
                ]
                enemy_hp = [random.randint(20, 50) for _ in range(random.randint(1, 3))]

                yield party_dpr_calculators, enemy_hp

        for party_dpr_calculators, enemy_hp in encounter_generator(5):
            encounter_evaluator = EncounterEvaluator(party_dpr=party_dpr_calculators, enemy_hp=enemy_hp)
            rounds_needed = encounter_evaluator.evaluate_encounter()

            # Make sure that the rounds needed to defeat the enemies is a positive value
            self.assertTrue(rounds_needed > 0)


# Run the tests
unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestDiceAndDPR))