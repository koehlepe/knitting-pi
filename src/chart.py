from stitch import StitchEnum, Direction
import random

class StitchCoords:
    def __init__(self, row_num, stitch_num):
        self.row_num = row_num
        self.stitch_num = stitch_num
    def __repr__(self):
        return f"StitchCoords(row={self.row_num}, stitch={self.stitch_num})"
    def __str__(self):
        return f"(row {self.row_num}, stitch {self.stitch_num})"
    def __hash__(self):
        return hash(self.row_num) ^ hash(self.stitch_num)
    def __eq__(self, other):
        if other is None:
            return False
        return self.row_num == other.row_num and self.stitch_num == other.stitch_num
    def __lt__(self, other):
        if self.row_num == other.row_num:
            return self.stitch_num < other.stitch_num
        return self.row_num < other.row_num
    def __le__(self, other):
        return self == other or self < other
    def __gt__(self, other):
        if self.row_num == other.row_num:
            return self.stitch_num > other.stitch_num
        return self.row_num > other.row_num
    def __ge__(self, other):
        return self == other or self > other
    def next_coords_from(self, chart):
        return chart.increment_coords(self)

class LiveStitch:
    def set_coords(self):
        self.coords = []
        coords = StitchCoords(self._row.row_num, self._start_index)
        for i in range(self.stitch_enum.ending_size):
            self.coords.append(coords)
            coords = self._chart().increment_coords(self.coords[-1])
    def __init__(self, stitch_enum, start_index, row):
        self.stitch_enum = stitch_enum
        self._start_index = start_index
        self._row = row
        self.set_coords()
    def __repr__(self):
        return f"LiveStitch(stitch={repr(self.stitch_enum)},start_index={self._start_index},row={self._row})"
    def __str__(self):
        return f"{self.stitch_enum} {self.start_coords()}"
    def __hash__(self):
        return hash(self.stitch_enum) ^ hash(self._start_index) ^ hash(self._row)
    def __eq__(self, other):
        if other is None:
            return False
        return self.stitch_enum == other.stitch_enum and self._start_index == other._start_index and self._row == other._row
    def __lt__(self, other):
        if self._row is None:
            return False
        if self.start_coords() == other.start_coords():
            return self.end_coords() < other.end_coords()
        return self.start_coords() < other.start_coords()
    def __le__(self, other):
        if self._row is None:
            return False
        return self.start_coords() <= other.start_coords()
    def __gt__(self, other):
        if self._row is None:
            return False
        if self.start_coords() == other.start_coords():
            return self.end_coords() > other.end_coords()
        return self.start_coords() > other.start_coords()
    def __ge__(self, other):
        if self._row is None:
            return False
        return self.start_coords() >= other.start_coords()
    def _chart(self):
        return self._row._chart
    def name(self):
        return self.stitch_enum.name()
    def start_coords(self):
        return self.coords[0]
    def all_coords(self):
        return self.coords
    def end_coords(self):
        return self.coords[-1]
