from enum import Enum


class Event(Enum):

    #key presses (0 - 99)
    VOLUME_UP = 0,
    VOLUME_DOWN = 1
    NAV_UP = 2
    NAV_DOWN = 3,

    #ws events (100+)
