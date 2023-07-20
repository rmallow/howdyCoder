from aenum import Enum
import string


class nameMatchEnum(Enum):
    @classmethod
    def _missing_name_(cls, name):
        for member in cls:
            memberName = member.name.translate(
                str.maketrans("", "", string.punctuation)
            )
            compareName = name.translate(str.maketrans("", "", string.punctuation))
            if memberName.lower() == compareName.lower():
                return member
