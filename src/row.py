from chart import LiveStitch, StitchCoords

class Row:
    def set_rules(self):
        self.__rules = []
        if self.row_num == 0 or self.row_num % 2 == 1 or self.is_increase_row():
            self.__rules.append('NoIncreasesRowRule')
            self.__rules.append('NoDecreasesRowRule')
            self.__rules.append('NoCablesRowRule')
        if self.is_increase_row():
            self.__rules.append('DoubleStitchCountIncreaseRowRule')
    def __init__(self, row_num, stitch_count, chart):
        self.row_num = row_num
        self.stitch_count = stitch_count
        self._chart = chart
        self.__stitches = []
        self.set_rules()
    def __repr__(self):
        return f"Row(row_num={self.row_num},stitch_count={self.stitch_count})"
    def __str__(self):
        return f"Row(#{self.row_num}: {self.stitch_count}sts)"
    def __getitem__(self, stitch_index):
        if stitch_index < 0 or stitch_index >= self.stitch_count:
            raise IndexError(f"Invalid stitch: {stitch_index} (only {self.stitch_count} available)")
        coords = StitchCoords(self.row_num, stitch_index)
        for stitch in self.__stitches:
            if coords in stitch.coords:
                return stitch
    def __setitem__(self, stitch_index, stitch_enum):
        affected_coords = []
        initial_coords = StitchCoords(self.row_num, stitch_index)
        next_coords = initial_coords
        for i in range(stitch_enum.starting_size):
            affected_coords.append(next_coords)
            next_coords = self._chart.increment_coords(next_coords)
        affected_stitches = []
        affected_coords = set(affected_coords)
        for stitch in self.__stitches:
            if len(affected_coords.intersection(stitch.coords)) > 0:
                affected_stitches.append(stitch)
        for stitch in affected_stitches:
            self.__stitches.remove(stitch)
        self.__stitches.append(LiveStitch(stitch_enum, stitch_index, self))
        self.__stitches.sort()
        return self[stitch_index]
    def previous_row(self):
        return self._chart[self.row_num - 1]
    def next_row(self):
        return self._chart[self.row_num + 1]
    def is_increase_row(self):
        return self.row_num > 0 and self.stitch_count > self.previous_row().stitch_count
    def stitches_print_string(self):
        row_string = ""
        for stitch in self.__stitches:
            if row_string != "":
                row_string += " "
            row_string += str(stitch.stitch_enum)
        return row_string
    def print_stitches(self):
        row_string = self.stitches_print_string()
        print(row_string)
    def is_empty(self):
        return len(self.__stitches) == 0
