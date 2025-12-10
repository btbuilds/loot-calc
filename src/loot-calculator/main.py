from scipy.optimize import linear_sum_assignment
from player import Player, Job
from item import Item
from constants import *

def calculate_weight(player: Player, item: Item, num_contenders: int):
    """
    Calculate the priority weight for assigning a specific item to a player.

    Lower weights are better. The value represents how desirable it is
    (from the raid's perspective) to give *this item* to *this player*.

    Factors included:
    - Off-spec penalty: Heavily punishes giving an item to someone who isn't main spec.
    - Job priority: Gives specific jobs higher priority.
    - Recent loot: Players who haven't gotten loot recently get higher priority.
    - Slot priority: Some slots (weapon, body, legs) provide more value.
    - Items needed: Players missing more pieces get slightly boosted.
    - Final item bonus: If this item would complete the player's BiS set for that slot type.
    - Contest penalty: More contenders = slightly higher cost to assign this item.

    Args:
        player (Player): The player being evaluated.
        item (Item): The item under consideration.
        num_contenders (int): Total number of players who need this item slot.

    Returns:
        int: The computed weight for this player/item pair.
    """
    weight = 0

    # Spec priority
    if not player.is_main_spec:
        weight += OFF_SPEC_PENALTY

    # Job priority
    weight += JOB_PRIORITY.get(player.job, 0)

    # Recent loot
    weight += player.bosses_without_loot * RECENT_LOOT_PENALTY_MULT

    # Slot priority
    weight += SLOT_WEIGHTS.get(item.slot_type, 0)

    # Need intensity
    weight += player.items_needed * ITEMS_NEEDED_MULT

    # If this is the final needed item in a slot-type
    if item.slot_type in player.slot_types_needed and len(player.slot_types_needed) == 1:
        weight += FINAL_ITEM

    # Contest penalty
    # (num_contenders includes them)
    if num_contenders > 1:
        weight += (num_contenders - 1) * 25

    return weight

def build_weight_matrix(players, items):
    """
    Construct the player -> item weight matrix used by the assignment algorithm.

    Each row represents a player.
    Each column represents an item.
    Each cell is the weight for giving that item to that player.

    If a player does NOT need a given item slot, the weight is set to a very
    large number to effectively mark it as "unassignable."

    Args:
        players (list[Player]): All players eligible for loot this week.
        items (list[Item]): The loot drops available this week.

    Returns:
        list[list[int]]: 2D matrix of assignment weights.
    """
    matrix = []
    
    for player in players:
        row = []
        for item in items:
            # Determine how many people want this item
            contenders = sum(1 for p in players if item.slot_type in p.slot_types_needed)

            # If player doesn't need it at all, penalize hard
            if item.slot_type not in player.slot_types_needed:
                row.append(999999)  # Basically "don't pick me"
            else:
                row.append(calculate_weight(player, item, contenders))
        
        matrix.append(row)
    
    return matrix

def assign_loot(players, items):
    """
    Assign each item to the most optimal player using the Hungarian algorithm.

    This solves the global assignment problem:
    It finds the combination of assignments that results in the lowest total weight,
    meaning the most fair/optimal loot distribution for the raid.

    Args:
        players (list[Player]): Players being considered for loot.
        items (list[Item]): Items being distributed.

    Returns:
        list[tuple[str, str]]: (player_name, item_name) assignment pairs.
    """
    matrix = build_weight_matrix(players, items)
    row_ind, col_ind = linear_sum_assignment(matrix)

    results = []
    for r, c in zip(row_ind, col_ind):
        results.append((players[r].name, items[c].name))
    return results


# Test Data
# Test Set 1: Small group with simple needs
test_set_1 = {
    "players": [
        Player("Alice", Job.WHM, True, 2, 3, {"weapon", "head"}),
        Player("Bob", Job.DRG, True, 1, 2, {"weapon"}),
        Player("Charlie", Job.BRD, False, 3, 4, {"head", "body"}),
    ],
    "items": [
        Item("Weapon Coffer", "weapon"),
        Item("Head Coffer", "head"),
    ]
}

# Test Set 2: Medium group with competing needs
test_set_2 = {
    "players": [
        Player("Diana", Job.SGE, True, 5, 6, {"accessory", "legs", "feet"}),
        Player("Eve", Job.RDM, True, 0, 1, {"accessory"}),
        Player("Frank", Job.SAM, True, 4, 5, {"legs", "hands"}),
        Player("Grace", Job.DNC, False, 2, 3, {"accessory", "feet"}),
        Player("Henry", Job.PLD, True, 3, 4, {"legs"}),
    ],
    "items": [
        Item("Accessory Coffer", "accessory"),
        Item("Legs Coffer", "legs"),
        Item("Feet Coffer", "feet"),
    ]
}

# Test Set 3: Large group with diverse needs
test_set_3 = {
    "players": [
        Player("Ivan", "warrior", True, 7, 8, {"weapon", "body", "head"}),
        Player("Jane", "summoner", True, 1, 2, {"weapon"}),
        Player("Kyle", Job.MNK, False, 6, 7, {"body", "hands", "feet"}),
        Player("Laura", Job.AST, True, 2, 3, {"head", "accessory"}),
        Player("Mike", Job.GNB, True, 4, 5, {"weapon", "body"}),
        Player("Nina", Job.MCH, False, 5, 6, {"hands", "feet"}),
        Player("Oscar", Job.NIN, True, 3, 4, {"head"}),
        Player("Paula", Job.PCT, True, 0, 1, {"accessory"}),
    ],
    "items": [
        Item("Weapon Coffer", "weapon"),
        Item("Body Coffer", "body"),
        Item("Head Coffer", "head"),
        Item("Accessory Coffer", "accessory"),
    ]
}

# Test Set 4: Edge case - everyone needs the same item
test_set_4 = {
    "players": [
        Player("Quinn", Job.DRK, True, 8, 7, {"weapon", "legs"}),
        Player("Rachel", Job.SAM, True, 6, 5, {"weapon", "body"}),
        Player("Steve", Job.BLM, False, 4, 6, {"weapon", "hands"}),
        Player("Tina", Job.RPR, True, 2, 3, {"weapon"}),
    ],
    "items": [
        Item("Weapon Coffer", "weapon"),
        Item("Legs Coffer", "legs"),
    ]
}

# Test Set 5: Mixed priorities with multiple items
test_set_5 = {
    "players": [
        Player("Uma", Job.WHM, True, 10, 8, {"hands", "feet", "legs", "body"}),
        Player("Victor", Job.MCH, False, 1, 2, {"hands"}),
        Player("Wendy", Job.VPR, True, 5, 6, {"feet", "legs"}),
        Player("Xavier", Job.GNB, True, 0, 1, {"body"}),
        Player("Yara", Job.RDM, True, 3, 4, {"hands", "feet"}),
        Player("Zack", Job.DRG, False, 7, 8, {"legs", "body"}),
    ],
    "items": [
        Item("Hands Coffer", "hands"),
        Item("Feet Coffer", "feet"),
        Item("Legs Coffer", "legs"),
        Item("Body Coffer", "body"),
    ]
}

# Test Set 6: No overlapping needs
test_set_6 = {
    "players": [
        Player("Aaron", Job.SAM, True, 4, 5, {"weapon"}),
        Player("Beth", Job.SCH, True, 3, 4, {"head"}),
        Player("Carl", Job.BRD, True, 2, 3, {"accessory"}),
    ],
    "items": [
        Item("Weapon Coffer", "weapon"),
        Item("Head Coffer", "head"),
        Item("Accessory Coffer", "accessory"),
    ]
}

# Test Set 7: All off-spec players
test_set_7 = {
    "players": [
        Player("Derek", Job.DRK, False, 5, 6, {"body", "legs"}),
        Player("Emma", Job.PCT, False, 4, 5, {"body", "hands"}),
        Player("Felix", Job.NIN, False, 6, 7, {"legs", "feet"}),
        Player("Gina", Job.AST, False, 3, 4, {"hands"}),
    ],
    "items": [
        Item("Body Coffer", "body"),
        Item("Legs Coffer", "legs"),
        Item("Hands Coffer", "hands"),
    ]
}

# Test Set 8: Varied item needs with multiple slot types per player
test_set_8 = {
    "players": [
        Player("Hugo", Job.RPR, True, 9, 8, {"weapon", "head", "body", "accessory"}),
        Player("Iris", Job.DNC, True, 2, 3, {"head", "feet"}),
        Player("Jack", Job.PLD, False, 5, 6, {"body", "hands", "legs"}),
        Player("Kelly", Job.SMN, True, 1, 2, {"accessory"}),
        Player("Liam", Job.DRG, True, 7, 7, {"weapon", "legs"}),
        Player("Mona", Job.WHM, False, 4, 5, {"hands", "feet"}),
    ],
    "items": [
        Item("Weapon Coffer", "weapon"),
        Item("Head Coffer", "head"),
        Item("Hands Coffer", "hands"),
        Item("Accessory Coffer", "accessory"),
    ]
}

# Function calls for each test set
print("Test Set 1:")
print(assign_loot(test_set_1["players"], test_set_1["items"]))
print()

print("Test Set 2:")
print(assign_loot(test_set_2["players"], test_set_2["items"]))
print()

print("Test Set 3:")
print(assign_loot(test_set_3["players"], test_set_3["items"]))
print()

print("Test Set 4:")
print(assign_loot(test_set_4["players"], test_set_4["items"]))
print()

print("Test Set 5:")
print(assign_loot(test_set_5["players"], test_set_5["items"]))
print()

print("Test Set 6:")
print(assign_loot(test_set_6["players"], test_set_6["items"]))
print()

print("Test Set 7:")
print(assign_loot(test_set_7["players"], test_set_7["items"]))
print()

print("Test Set 8:")
print(assign_loot(test_set_8["players"], test_set_8["items"]))
print()