from enum import Enum, auto

class Direction(Enum):
    LEFT = auto()
    STRAIGHT = auto()
    RIGHT = auto()

class StitchDefinition:
    abbreviation: str
    description: str
    starting_size: int
    ending_size: int
    direction: Direction

    def __init__(self, abbreviation, description, starting_size, ending_size, direction):
        self.abbreviation = abbreviation
        self.description = description
        self.starting_size = starting_size
        self.ending_size = ending_size
        self.direction = direction

    def __repr__(self):
        return f"StitchDefinition({self.abbreviation.upper()})"

    def __str__(self):
        return self.abbreviation.upper()

    def is_increase(self):
        return self.starting_size < self.ending_size

    def is_decrease(self):
        return self.ending_size < self.starting_size

    def is_static_stitch_count(self):
        return self.starting_size == self.ending_size

    def is_allowed_on_initial_row(self):
        return self.starting_size == 1 and self.is_static_stitch_count()

class StitchEnum(StitchDefinition, Enum):
    # 0 -> 1
    YO = ('yo', 'yarn over', 0, 1, Direction.STRAIGHT)
    M1L = ('m1l', 'make 1 left', 0, 1, Direction.LEFT)
    M1R = ('m1r', 'make 1 right', 0, 1, Direction.RIGHT)
    # 1 -> 1
    KNIT = ('knit', 'knit', 1, 1, Direction.STRAIGHT)
    PURL = ('purl', 'purl', 1, 1, Direction.STRAIGHT)
    KTBL = ('ktbl', 'knit 1 through the back loop', 1, 1, Direction.STRAIGHT)
    PTBL = ('ptbl', 'purl 1 through the back loop', 1, 1, Direction.STRAIGHT)
    BOBBLE = ('bobble', 'make a bobble', 1, 1, Direction.STRAIGHT)
    # 1 -> 2
    KFB = ('kfb', 'knit front & back', 1, 2, Direction.STRAIGHT)
    PFB = ('pfb', 'purl front & back', 1, 2, Direction.STRAIGHT)
    RLI = ('rli', 'right lifted increase from right leg of stitch below', 1, 2, Direction.RIGHT)
    LLI = ('lli', 'left lifted increase from left leg of stitch below', 1, 2, Direction.LEFT)
    # 1 -> 3
    KYOK = ('kyok', 'knit-yo-knit into same stitch', 1, 3, Direction.STRAIGHT)
    # 1 -> 5
    KYOKYOK = ('kyokyok', 'k-yo-k-yo-k into same stitch', 1, 5, Direction.STRAIGHT)
    # 2 -> 1
    K2TOG = ('k2tog', 'knit 2 together', 2, 1, Direction.RIGHT)
    SSK = ('ssk', 'slip slip knit 2 together', 2, 1, Direction.LEFT)
    P2TOG = ('p2tog', 'purl 2 together', 2, 1, Direction.RIGHT)
    SSP = ('ssp', 'slip slip purl 2 together through the back loop', 2, 1, Direction.LEFT)
    # 2 -> 2
    RCKK = ('rckk', 'right cross 1/1 knit', 2, 2, Direction.STRAIGHT)
    LCKK = ('lckk', 'left cross 1/1 knit', 2, 2, Direction.STRAIGHT)
    RCKP = ('rckp', 'right cross k1/p1', 2, 2, Direction.STRAIGHT)
    LCPK = ('lcpk', 'left cross p1/k1', 2, 2, Direction.STRAIGHT)
    # 3 -> 1
    K3TOG = ('k3tog', 'knit 3 together', 3, 1, Direction.RIGHT)
    SSSK = ('sssk', 'slip slip slip knit 3 together', 3, 1, Direction.LEFT)
    P3TOG = ('p3tog', 'purl 3 together', 3, 1, Direction.RIGHT)
    SSSP = ('sssp', 'slip slip slip purl 3 together through the back loop', 3, 1, Direction.LEFT)
    CDD = ('cdd', 'centered double decrease (s2kp)', 3, 1, Direction.STRAIGHT)
    S2KP = ('s2kp', 'slip 2 together knitwise, knit 1, pass slipped stitches over (cdd)', 3, 1, Direction.STRAIGHT)

    def name(self):
        return self.abbreviation.upper()

    def is_increase(self):
        return self.starting_size < self.ending_size

    def is_decrease(self):
        return self.ending_size < self.starting_size

    def is_static_stitch_count(self):
        return self.starting_size == self.ending_size

    def is_cable(self):
        return self.starting_size > 1 and self.is_static_stitch_count()

    def increased_stitch_count(self):
        if self.is_increase():
            return self.ending_size - self.starting_size
        return 0

    def decreased_stitch_count(self):
        if self.is_decrease():
            return self.ending_size - self.starting_size
        return 0

    def is_allowed_on_initial_row(self):
        return self.starting_size == 1 and self.is_static_stitch_count()

    def is_allowed_on_random_generation(self):
        return (self.starting_size < 3 and self.ending_size < 3) or self in {StitchEnum.CDD, StitchEnum.S2KP}
