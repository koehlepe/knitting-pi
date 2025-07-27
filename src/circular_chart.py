from row import Row
from chart import StitchCoords
from stitch import StitchEnum, Direction
import random

class CircularChart:
  stitches_that_may_not_appear_next_to_each_other = {StitchEnum.YO,
                                                     StitchEnum.M1R,
                                                     StitchEnum.M1L,
                                                     StitchEnum.RLI,
                                                     StitchEnum.LLI}

  def __init__(self, num_rows, starting_stitch_count):
    self.__chart_array = []
    # build the internal data for how many stitches each row needs
    stitch_counts_per_row = []
    current_stitch_count = starting_stitch_count
    num_rows_at_current_stitch_count = 2
    while len(stitch_counts_per_row) < num_rows:
      num_rows_to_append = min(num_rows-len(stitch_counts_per_row),num_rows_at_current_stitch_count)
      stitch_counts_per_row.extend([current_stitch_count] * num_rows_to_append)
      current_stitch_count = current_stitch_count * 2
      num_rows_at_current_stitch_count = num_rows_at_current_stitch_count * 2
    # print(stitch_counts_per_row)
    for i, stitch_count in enumerate(stitch_counts_per_row):
      self.__chart_array.append(Row(i,stitch_count,chart=self))
    # print(self.__chart_array)
    # print(self.is_empty())

  def print_chart(self):
    max_pad_size = len(str(len(self.__chart_array)+1))
    for ri in range(len(self.__chart_array)-1,-1,-1):
      row_string = "Row " + str(ri+1).zfill(max_pad_size)
      row_string = row_string + " (" + str(self.__chart_array[ri].stitch_count) + "sts): "
      row_string = row_string + str([s.name() for s in self.__chart_array[ri]])
      print(row_string)

  def print_chart_2(self):
    max_pad_size = len(str(len(self.__chart_array)+1))
    for row_num in range(len(self.__chart_array)-1,-1,-1):
      row_str = "Row " + str(row_num+1).zfill(max_pad_size)
      row_str = row_str + " (" + str(self.__chart_array[row_num].stitch_count) + "sts): "
      row_str = row_str + self[row_num].stitches_print_string()
      print(row_str)

  def is_empty(self):
    return all(row.is_empty() for row in self.__chart_array)

  def __getitem__(self, row_num):
    if row_num < len(self.__chart_array):
      return self.__chart_array[row_num]
    return None

  def increment_coords(self,coords):
    row = self[coords.row_num]
    assert coords.stitch_num < row.stitch_count, \
    f"invalid coords: {coords} for row: {row}"
    if coords.stitch_num + 1 < row.stitch_count:
      return StitchCoords(coords.row_num, coords.stitch_num + 1)
    elif self[coords.row_num + 1] != None:
      return StitchCoords(coords.row_num + 1, 0)
    else:
      return None

  def final_coords(self):
    return self[-1].end_coords()

  def final_coords_for_stitch_starting_at(self, new_stitch, start_coords):
    next_coords = start_coords
    for i in range(new_stitch.starting_size - 1):
      self.increment_coords(next_coords)

  def generate_random_chart(self):
    assert self.is_empty(), "cannot generate a random chart -- it is not empty"
    current = StitchCoords(0, 0)
    previous_stitch = None
    while current != None:
      print("generating at " + str(current))
      current_row = self[current.row_num]

      is_increase_row = current.row_num != 0 and \
      current_row.stitch_count > current_row.previous_row().stitch_count
      print(is_increase_row)

      # what stitches are allowed on this row?
      if current_row.row_num == 0:
        allowed_stitches = [st for st in list(StitchEnum) if
                            st.starting_size == 1 and st.ending_size == 1]
      elif is_increase_row:
        allowed_stitches = [st for st in list(StitchEnum) if
                            st.starting_size < 2]
      else:
        allowed_stitches = list(StitchEnum)

      # increase limitations
      if previous_stitch in CircularChart.stitches_that_may_not_appear_next_to_each_other:
        allowed_stitches = [st for st in allowed_stitches if st not in \
                            CircularChart.stitches_that_may_not_appear_next_to_each_other]
        allowed_stitches = [st for st in allowed_stitches if st.direction !=
                            Direction.LEFT and st not in
                            {StitchEnum.CDD, StitchEnum.S2KP}]

      # eliminate all directional 3->1 decreases, it's too hard to fill the \
      # remaining 2 slots at random; also eliminate increases of +2 or more
      allowed_stitches = [st for st in allowed_stitches if st.starting_size
                          != 3 or st in {StitchEnum.CDD, StitchEnum.S2KP}]
      allowed_stitches = [st for st in allowed_stitches if st.increased_stitch_count() < 2]
      print("allowed stitches: " + str(allowed_stitches))

      # generate a stitch
      new_stitch = random.choice(allowed_stitches)
      print("generated " + str(new_stitch))

      if current_row == self[-1]:
        total_retries = 0
        stitch_requires_more_stitches_below_than_may_exist = \
         (current.stitch_num + new_stitch.starting_size) > \
         current_row.stitch_count
        stitch_will_extend_the_number_of_stitches_on_the_final_row = \
         (current.stitch_num + new_stitch.ending_size) > \
         current_row.stitch_count
        stitch_is_m1_increase_on_final_row = (current.stitch_num + 1) == \
        current_row.stitch_count and new_stitch.starting_size == 0
        while (total_retries < 10 and (stitch_requires_more_stitches_below_than_may_exist or
               stitch_will_extend_the_number_of_stitches_on_the_final_row or
               stitch_is_m1_increase_on_final_row)):
          total_retries += 1
          new_stitch = random.choice(allowed_stitches)
          print("generated " + str(new_stitch))
          stitch_requires_more_stitches_below_than_may_exist = \
           (current.stitch_num + new_stitch.starting_size) > \
           current_row.stitch_count
          stitch_will_extend_the_number_of_stitches_on_the_final_row = \
           (current.stitch_num + new_stitch.ending_size) > \
           current_row.stitch_count
          stitch_is_m1_increase_on_final_row = (current.stitch_num + 1) == \
           current_row.stitch_count and new_stitch.starting_size == 0
        assert total_retries < 10, "whoops infinite recursion"


      # increase row? if 0->1 increase, add 1->1 stitch first. kfb/pfb are fine.
      if is_increase_row:
        print("increase row!")
        assert new_stitch.starting_size == 0 or new_stitch.is_increase() or \
         (new_stitch.starting_size == 1 and new_stitch.ending_size == 1), \
         f"messed up the allowed stitches for increase rows somehow (trying to \
         add {new_stitch})"
        if new_stitch.starting_size == 0:
          initial_stitch = random.choice([st for st in list(StitchEnum) if \
                                          st.starting_size == 1 and \
                                          st.ending_size == 1])
          self[current.row_num][current.stitch_num] = initial_stitch
          for i in range(initial_stitch.ending_size):
            current = self.increment_coords(current)
          self[current.row_num][current.stitch_num] = new_stitch
          previous_stitch = new_stitch
        elif new_stitch.is_increase():
          # by definition 1->2 -- insert as-is
          self[current.row_num][current.stitch_num] = new_stitch
          previous_stitch = new_stitch
        else:
          # by definition 1->1 -- need to add a 0->1 increase
          next_stitch = random.choice([st for st in list(StitchEnum) if \
                                       st.starting_size == 0])
          self[current.row_num][current.stitch_num] = new_stitch
          for i in range(new_stitch.ending_size):
            current = self.increment_coords(current)
          self[current.row_num][current.stitch_num] = next_stitch
          previous_stitch = next_stitch
      elif new_stitch.is_increase():
        # increase on non-increase row. need correspodning decrease
        print("increase on non-increase row")
        if new_stitch.direction == Direction.STRAIGHT:
          # pick a decrease at random and follow the directionality rules
          other_stitch = random.choice([st for st in list(StitchEnum) if \
                                        st.starting_size == 2 and \
                                        st.is_decrease()])
          if other_stitch.direction == Direction.LEFT:
            self[current.row_num][current.stitch_num] = new_stitch
            for i in range(new_stitch.ending_size):
              current = self.increment_coords(current)
            self[current.row_num][current.stitch_num] = other_stitch
            previous_stitch = other_stitch
          else:
            self[current.row_num][current.stitch_num] = other_stitch
            for i in range(other_stitch.ending_size):
              current = self.increment_coords(current)
            self[current.row_num][current.stitch_num] = new_stitch
            previous_stitch = new_stitch
        elif new_stitch.direction == Direction.LEFT:
          initial_stitch = random.choice([st for st in list(StitchEnum) if \
                                          st.starting_size == 2 and \
                                          st.is_decrease() and \
                                          st.direction == Direction.RIGHT])
          self[current.row_num][current.stitch_num] = initial_stitch
          for i in range(initial_stitch.ending_size):
            current = self.increment_coords(current)
          self[current.row_num][current.stitch_num] = new_stitch
          previous_stitch = new_stitch
        else:
          # must be RIGHT
          final_stitch = random.choice([st for st in list(StitchEnum) if \
                                        st.starting_size == 2 and \
                                        st.is_decrease() and \
                                        st.direction == Direction.LEFT])
          self[current.row_num][current.stitch_num] = new_stitch
          for i in range(new_stitch.ending_size):
            current = self.increment_coords(current)
          self[current.row_num][current.stitch_num] = final_stitch
          previous_stitch = final_stitch
      elif new_stitch.is_decrease():
        if new_stitch.starting_size == 3:
          print("CDD!")
          # must be CDD. need increase before AND after
          assert previous_stitch not in CircularChart.stitches_that_may_not_appear_next_to_each_other, \
          f"whoops somehow we still got {previous_stitch} before CDD"
          initial_stitch = random.choice([st for st in list(StitchEnum) if \
                                          st.starting_size == 0 and \
                                          st.direction != Direction.LEFT])
          final_stitch = random.choice([st for st in list(StitchEnum) if \
                                        st.starting_size == 0 and st.direction \
                                        != Direction.RIGHT])
          self[current.row_num][current.stitch_num] = initial_stitch
          for i in range(initial_stitch.ending_size):
            current = self.increment_coords(current)
          self[current.row_num][current.stitch_num] = new_stitch
          for i in range(new_stitch.ending_size):
            current = self.increment_coords(current)
          self[current.row_num][current.stitch_num] = final_stitch
          previous_stitch = final_stitch
        else:
          # must be 2->1; find appropriate before/after increase
          print("2->1!")
          if new_stitch.direction == Direction.LEFT:
            initial_stitch = random.choice([st for st in list(StitchEnum) if \
                                            st.starting_size == 0 and \
                                            st.direction != Direction.LEFT])
            self[current.row_num][current.stitch_num] = initial_stitch
            for i in range(initial_stitch.ending_size):
              current = self.increment_coords(current)
            self[current.row_num][current.stitch_num] = new_stitch
            previous_stitch = new_stitch
          else:
            # must lean right
            final_stitch = random.choice([st for st in list(StitchEnum) if \
                                          st.starting_size == 0 and \
                                          st.direction != Direction.RIGHT])
            self[current.row_num][current.stitch_num] = new_stitch
            for i in range(new_stitch.ending_size):
              current = self.increment_coords(current)
            self[current.row_num][current.stitch_num] = final_stitch
            previous_stitch = final_stitch
      else:
        # new stitch is neither on an increase row nor a decrease -- just
        # insert it as is.
        self[current.row_num][current.stitch_num] = new_stitch
        previous_stitch = new_stitch
      print(previous_stitch)
      print("generated through " + str(current))
      current_row.print_stitches()
      if self[current.row_num] != current_row:
        self[current.row_num].print_stitches()
      for i in range(previous_stitch.ending_size):
        current = self.increment_coords(current)
      print("new coords " + str(current))
      print("")
