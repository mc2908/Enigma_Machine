from Rotor import *
class Rotorscase:

    def __init__(self):
        self.nRotations = 0
        self.rotors = []
        self.num_rotors = 0
        self.max_rotors = 4
        self.min_rotors = 3
        self.debug_mode = False

    def add(self, rotor):
        if self.num_rotors > self.max_rotors:
            return
        self.rotors.append(rotor)
        rotor.location = self.num_rotors
        if self.num_rotors >= 1:
            self.rotors[self.num_rotors-1].left_rotor = rotor
            rotor.right_rotor = self.rotors[self.num_rotors-1]
        self.num_rotors += 1

    def rotate(self):
        self.nRotations += 1
        self.__reset_rotor()
        if self.debug_mode:
            print(f"\n")
            print(f"rotation number {self.nRotations}")
        can_rotate = True
        for idx, rotor in enumerate(self.rotors):
            if rotor.is_rightmost_rotor() or rotor.is_at_notch() and not rotor.is_leftmost_rotor() and not rotor.has_rotated and can_rotate:
                can_rotate = rotor.rotate()
            else:
                can_rotate = False
            if self.debug_mode:
                print(f"rotor {rotor.eType} is now on position {Rotor.num2Char(rotor.pos)}")


    def __reset_rotor(self):
        for  rotor in self.rotors:
            rotor.has_rotated = False

    def reset_to_default_position(self):
        for rotor in self.rotors:
            rotor.reset_to_default()

    def encode_right_to_left(self, in_char):
        out_char = in_char
        for rotor in self.rotors:
            out_char = rotor.encode_right_to_left(out_char)
        self.rotors.reverse()
        return out_char

    def encode_left_to_right(self, in_char):
        out_char = in_char
        for rotor in self.rotors:
            out_char = rotor.encode_left_to_right(out_char)
        self.rotors.reverse()
        return out_char

    def get_rotor_by_location(self, idx):
        return self.rotors[idx-1]

    def get_rotor_by_name(self):
        pass

    def remove_rotor_by_name(self):
        pass

    def remove_all_rotors(self):
        self.nRotations = 0
        self.rotors = []
        self.num_rotors = 0


    def set_rotor_initial_positions(self,positions):
        positions.reverse()
        for idx, pos in enumerate(positions):
            rotor = self.rotors[idx]
            rotor.set_intial_position(pos)


    def set_rotor_initial_ring_setting(self,ring_set):
        ring_set.reverse()
        for idx, ring in enumerate(ring_set):
            rotor = self.rotors[idx]
            rotor.set_ring_setting(ring)









