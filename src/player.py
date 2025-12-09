from enum import Enum

class Job(Enum):
    PLD = ("pld", "Paladin", "Tank")
    WAR = ("war", "Warrior", "Tank")
    DRK = ("drk", "Dark Knight", "Tank")
    GNB = ("gnb", "Gunbreaker", "Tank")

    WHM = ("whm", "White Mage", "Healer")
    SCH = ("sch", "Scholar", "Healer")
    AST = ("ast", "Astrologian", "Healer")
    SGE = ("sge", "Sage", "Healer")

    MNK = ("mnk", "Monk", "Melee DPS")
    DRG = ("drg", "Dragoon", "Melee DPS")
    NIN = ("nin", "Ninja", "Melee DPS")
    SAM = ("sam", "Samurai", "Melee DPS")
    RPR = ("rpr", "Reaper", "Melee DPS")
    VPR = ("vpr", "Viper", "Melee DPS")

    BRD = ("brd", "Bard", "Physical Ranged DPS")
    MCH = ("mch", "Machinist", "Physical Ranged DPS")
    DNC = ("dnc", "Dancer", "Physical Ranged DPS")

    BLM = ("blm", "Black Mage", "Magical Ranged DPS")
    SMN = ("smn", "Summoner", "Magical Ranged DPS")
    RDM = ("rdm", "Red Mage", "Magical Ranged DPS")
    PCT = ("pct", "Pictomancer", "Magical Ranged DPS")

    def __init__(self, short, full, role):
        self.short = short
        self.full = full
        self.role = role

    @classmethod
    def from_string(cls, value):
        """Coerce a string into a Job enum, matching short code or full name."""
        if isinstance(value, Job):
            return value  # already the correct type

        value = value.strip().lower()

        for job in cls:
            if value == job.short.lower() or value == job.full.lower():
                return job

        raise ValueError(f"Unknown job value: {value!r}")
    
class Player:
    def __init__(self, name, job, is_main_spec, bosses_without_loot, items_needed, slot_types_needed):
        self.name = name
        self.job = Job.from_string(job) # Can take either an enum or a string and sets it to the correct enum
        self.is_main_spec = is_main_spec
        self.bosses_without_loot = bosses_without_loot
        self.items_needed = items_needed  # total number of pieces needed
        self.slot_types_needed = slot_types_needed  # e.g. {"weapon", "ring", "head"}