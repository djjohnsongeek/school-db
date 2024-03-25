from enum import IntEnum

class StaffRole(IntEnum):
    Teacher = 1
    Staff = 2

class PersonGender(IntEnum):
    Male = 1,
    Female = 2

class MessageCategory(IntEnum):
    Success = 1,
    Warn = 2,
    Error = 3