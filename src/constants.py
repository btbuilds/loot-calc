from player import Job

# Weights for priority calculation
# All of these can be tweaked to adjust behavior.

# Penalty for off-spec items to ensure they only get the item if no one else needs it 
OFF_SPEC_PENALTY = 1000

# Slot Priority
ACCESSORY = -10
BODY = -30
FEET = -20
HANDS = -20
HEAD = -20
LEGS = -30
WEAPON = -40

SLOT_WEIGHTS = {
    "accessory": ACCESSORY,
    "body": BODY,
    "feet": FEET,
    "hands": HANDS,
    "head": HEAD,
    "legs": LEGS,
    "weapon": WEAPON,
}

# Prioritize someone finishing their gear set if they only have one piece left
FINAL_ITEM = -50

# Prioritize people who have less gear
ITEMS_NEEDED_MULT = -5

# Multiplier for how many bosses the player has gone without receiving loot
RECENT_LOOT_PENALTY_MULT = -15

# Job Weights - Melee and casters get highest priority, healers get lowest
JOB_PRIORITY = {
    Job.PLD: -20,
    Job.WAR: -20,
    Job.DRK: -20,
    Job.GNB: -20,
    Job.WHM: -10,
    Job.SCH: -10,
    Job.AST: -10,
    Job.SGE: -10,
    Job.MNK: -40,
    Job.DRG: -40,
    Job.NIN: -40,
    Job.SAM: -40,
    Job.RPR: -40,
    Job.VPR: -40,
    Job.BRD: -30,
    Job.MCH: -30,
    Job.DNC: -30,
    Job.BLM: -40,
    Job.SMN: -35,
    Job.RDM: -35,
    Job.PCT: -40 }