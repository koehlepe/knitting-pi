from stitch import StitchEnum, Direction
from abc import abstractmethod

class RowRule:
  combos = None
  @classmethod
  @abstractmethod
  def allowed_stitches(cls):
    pass
  @classmethod
  @abstractmethod
  def build_valid_stitch_combinations(cls):
    cls.combos = []
    for stitch in cls.allowed_stitches():
      cls.combos.append([stitch])
  def valid_stitch_combinations(cls):
    if cls.combos == None:
      cls.build_valid_stitch_combinations()
    return cls.combos
  @abstractmethod
  def validate(self, new_stitches, partial_row):
    return all(new_stitch in self.allowed_stitches()
    for new_stitch in new_stitches) \
    and (partial_row.current_size() + len(new_stitches)
    <= partial_row.stitch_count)

class MaintainStitchCountRowRule(RowRule):
  @classmethod
  def build_valid_stitch_combinations(cls):
    cls.combos = [[st] for st in list(StitchEnum) if st.is_static_stitch_count()]
    for decrease in [st for st in list(StitchEnum) if st.is_decrease()]:
      for increase in [st for st in list(StitchEnum) if st.is_increase()]:
        match (decrease.direction, increase.direction):
          case (Direction.RIGHT, Direction.STRAIGHT):
            cls.combos.append([decrease, increase])
          case (Direction.RIGHT, Direction.LEFT):
            cls.combos.append([decrease, increase])
          case (Direction.STRAIGHT, Direction.RIGHT):
            cls.combos.append([increase, decrease])
          case (Direction.STRAIGHT, Direction.LEFT):
            cls.combos.append([decrease, increase])
          case (Direction.LEFT, Direction.RIGHT):
            cls.combos.append([increase, decrease])
          case (Direction.LEFT, Direction.STRAIGHT):
            cls.combos.append([increase, decrease])
  @classmethod
  def allowed_stitches(self):
    return list(StitchEnum)
  def validate(self, new_stitches, partial_row):
    return super().validate(new_stitches, partial_row)

class NoDoubleIncreasesFromThinAirRowRule(RowRule):
  @classmethod
  def allowed_stitches(self):
    return list(StitchEnum)
  def is_non_duplicatable_increase(self,stitch):
    return stitch.starting_size == 0 or stitch in [StitchEnum.RLI, StitchEnum.LLI]
  def validate(self, new_stitches, partial_row):
    if not super().validate(new_stitches, partial_row):
      return False
    all_stitches = []
    if len(partial_row) > 0:
      all_stitches.append(partial_row[-1])
    all_stitches.extend(new_stitches)
    for i in range(1,len(all_stitches)):
      first_stitch = all_stitches[i-1]
      second_stitch = all_stitches[i]
      print("comparing " + str(first_stitch) + " and " + str(second_stitch) + " for double increases")
      if self.is_non_duplicatable_increase(all_stitches[i-1]) and self.is_non_duplicatable_increase(all_stitches[i]):
        return False
    print("done comparing for double increases")
    return True

class DoubleStitchCountIncreaseRowRule(RowRule):
  @classmethod
  def build_valid_stitch_combinations(cls):
    cls.combos = []
    for stitch in cls.allowed_stitches():
      if stitch.is_increase() and stitch.starting_size == 1:
        cls.combos.append([stitch])
    for stitch_static in [st for st in cls.allowed_stitches() if st.is_static_stitch_count()]:
      for stitch_increase in [st for st in cls.allowed_stitches() if st.starting_size == 0]:
        cls.combos.extend([[stitch_static,stitch_increase],[stitch_increase,stitch_static]])
  @classmethod
  def allowed_stitches(cls):
    return [stitch_enum for stitch_enum in list(StitchEnum) if stitch_enum.starting_size < 2]
  def validate(self, new_stitches, partial_row):
    return super().validate(self, new_stitches, partial_row) and new_stitches in self.valid_stitch_combinations()

class NoIncreasesRowRule(RowRule):
  @classmethod
  def allowed_stitches(self):
    return [stitch_enum for stitch_enum in list(StitchEnum) if not stitch_enum.is_increase()]
  def validate(self, new_stitches, partial_row):
    return super.validate(self, new_stitches, partial_row) and new_stitches in self.valid_stitch_combinations()

class NoDecreasesRowRule(RowRule):
  @classmethod
  def allowed_stitches(cls):
    return [stitch_enum for stitch_enum in list(StitchEnum) if not stitch_enum.is_decrease()]
  def validate(self, new_stitches, partial_row):
    return super.validate(self, new_stitches, partial_row) and new_stitches in self.valid_stitch_combinations()

class NoCablesRowRule(RowRule):
  @classmethod
  def allowed_stitches(self):
    return [stitch_enum for stitch_enum in list(StitchEnum) if not stitch_enum.is_cable()]
  def validate(self, new_stitches, partial_row):
    return super().validate(new_stitches, partial_row) and new_stitches in self.valid_stitch_combinations()

for cls in [MaintainStitchCountRowRule, NoDoubleIncreasesFromThinAirRowRule, DoubleStitchCountIncreaseRowRule, NoIncreasesRowRule, NoDecreasesRowRule, NoCablesRowRule]:
  rule = cls()
  print(rule.valid_stitch_combinations())
for cls in [MaintainStitchCountRowRule, NoDoubleIncreasesFromThinAirRowRule, DoubleStitchCountIncreaseRowRule, NoIncreasesRowRule, NoDecreasesRowRule, NoCablesRowRule]:
  rule = cls()
  print(rule.valid_stitch_combinations()) #ensure everything stayed the same...
