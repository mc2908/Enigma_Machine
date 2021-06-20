from rotor import *


# This class represents a container (Manager) of rotors objects
class Rotorscase:

    def __init__(self):
        self.rotors = []            # List of rotor objects
        self.num_rotors = 0         # number of added rotors
        self.max_rotors = 4         # number of maximum rotors allowed
        self.min_rotors = 3         # number of minimum rotors allowed
        self.debug_mode = False

    # Add Rotor object. Rotors must be added in right to left order
    def add(self, this_rotor: Rotor):
        if self.num_rotors >= self.max_rotors:
            raise ValueError(f"Maximum number of rotors ({self.max_rotors}) has been exceeded.")
        if this_rotor in self.rotors:
            raise ValueError(f"Rotor ({this_rotor.eType}) already added")
        self.rotors.append(this_rotor)
        this_rotor.location = self.num_rotors
        if self.num_rotors >= 1:
            # add a pointer to this rotor in the previously added rotor
            self.rotors[self.num_rotors-1].left_rotor = this_rotor
            # add a pointer to the previously added rotor in this rotor
            this_rotor.right_rotor = self.rotors[self.num_rotors-1]
        self.num_rotors += 1

    def rotate(self):
        # Each new keyboard press, before making the rotors rotate, reset the has_rotated flag
        self.__reset_rotor()
        # Iterate over the rotors from right to left and rotate them if necessary.
        # This outer for loop takes care of the double stepping
        for idx, this_rotor in enumerate(self.rotors):
            # Check if this rotor can rotate depending on its location, position and whether or not it has already
            # rotated for this key stroke
            if this_rotor.is_rightmost_rotor() or this_rotor.is_at_notch() and not this_rotor.is_leftmost_rotor() and not this_rotor.has_rotated:
                this_rotor.rotate()
            else:
                # If this rotor could not rotate the remaining ones on the left cannot rotate for sure.
                return
            if self.debug_mode:
                print(f"rotor {this_rotor.eType} is now on position {this_rotor.num2char(this_rotor.pos)}")

    def __reset_rotor(self):
        for this_rotor in self.rotors:
            this_rotor.has_rotated = False

    def reset_to_default_position(self):
        for this_rotor in self.rotors:
            this_rotor.reset_to_default()

    # Pass the input character through all rotors mappings from right  to left
    def encode_right_to_left(self, in_char):
        out_char = in_char
        for this_rotor in self.rotors:
            out_char = this_rotor.encode_right_to_left(out_char)
        # reverse the list to get it ready for encode_left_to_right
        self.rotors.reverse()
        return out_char

    # Pass the input character through all rotors mappings from left to right
    def encode_left_to_right(self, in_char):
        out_char = in_char
        for this_rotor in self.rotors:
            out_char = this_rotor.encode_left_to_right(out_char)
        # reverse the list to get it ready for encode_right_to_left
        self.rotors.reverse()
        return out_char


    def remove_all_rotors(self):
        self.rotors = []
        self.num_rotors = 0

    # set the rotors default initial position
    def set_rotors_initial_positions(self, positions):
        if self.num_rotors == 0:
            raise ValueError("No rotors have been added yet. Insert rotors first")
        if len(positions) != self.num_rotors:
            raise ValueError("Number of specified rotors positions does not match the number of rotors")
        positions.reverse()
        for idx, pos in enumerate(positions):
            this_rotor = self.rotors[idx]
            this_rotor.set_initial_position(pos)

    # set the rotors default ring setting
    def set_rotor_initial_ring_setting(self, ring_set):
        if self.num_rotors == 0:
            raise ValueError("No rotors have been added yet. Insert rotors first")
        if len(ring_set) != self.num_rotors:
            raise ValueError("Number of specified ring settings does not match the number of rotors")
        ring_set.reverse()
        for idx, ring in enumerate(ring_set):
            this_rotor = self.rotors[idx]
            this_rotor.set_ring_setting(ring)


if __name__ == '__main__':

    RC = Rotorscase()
    rotor1 = rotor_from_name("I")
    rotor2 = rotor_from_name("II")
    rotor3 = rotor_from_name("III")
    RC.add(rotor1)
    RC.add(rotor2)
    RC.add(rotor3)

    try:
        RC.add(rotor3)
        print("Test failed")
    except ValueError:
        print("Test passed")

    try:
        rotor4 = rotor_from_name("IV")
        rotor5 = rotor_from_name("V")
        RC.add(rotor4)
        print("4 rotors are still ok")
        RC.add(rotor5)
        print("Test failed")
    except ValueError:
        print("Test passed")

