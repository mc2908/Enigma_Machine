class FrozenClass(object):
    __isfrozen = False
    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError(f"{key} is not an attribute of class {type(self)}")
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True