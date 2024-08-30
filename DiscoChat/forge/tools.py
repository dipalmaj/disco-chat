import random

def average_damage(dice: str) -> float:
    """
    Calculate the average damage for a given dice roll expression.
    Example dice strings: '1d8', '2d6+3'
    """
    parts = dice.split('+')
    dice_part = parts[0].strip()
    modifier = int(parts[1].strip()) if len(parts) > 1 else 0

    num, die = map(int, dice_part.split('d'))
    avg_roll = (num * (1 + die)) / 2

    return avg_roll + modifier


def hit_chance(attack_bonus: int, target_ac: int) -> float:
    """
    Calculate the probability of hitting a target with a given AC.
    """
    hit_probability = (21 - target_ac + attack_bonus) / 20
    return max(min(hit_probability, 0.95), 0.05)  # hit chance between 5% and 95%


def expected_dpr(attack_bonus: int, target_ac: int, dice: str, num_attacks: int = 1, crit_range: int = 20, crit_bonus: str = None) -> float:
    """
    Calculate the expected Damage Per Round (DPR) for a character.
    Parameters:
    - attack_bonus: The attack bonus (e.g., +7)
    - target_ac: The target's Armor Class (AC)
    - dice: The damage dice (e.g., '1d8+3')
    - num_attacks: Number of attacks per round
    - crit_range: The range for a critical hit (default is 20)
    - crit_bonus: Extra damage dice on crit (e.g., '1d8')
    """
    # Average damage per hit
    avg_damage = average_damage(dice)

    # Critical hit probability
    crit_chance = (21 - crit_range) / 20
    crit_damage = average_damage(crit_bonus) if crit_bonus else avg_damage

    # Expected damage per attack considering crits
    expected_damage = (1 - crit_chance) * avg_damage + crit_chance * (avg_damage + crit_damage)

    # Hit chance
    hit_probability = hit_chance(attack_bonus, target_ac)

    # Total DPR considering number of attacks
    dpr = expected_damage * hit_probability * num_attacks
    return dpr


# Example usage:
fighter_dpr = expected_dpr(
    attack_bonus=7,
    target_ac=15,
    dice='1d8+3',
    num_attacks=2,
    crit_range=20,
    crit_bonus='1d8'
)

print(f"Expected DPR: {fighter_dpr:.2f}")