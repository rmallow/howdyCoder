class messageKey:
    def __init__(self, sourceCode, time):
        self.sourceCode = sourceCode
        self.time = time

    def __eq__(self, other):
        return self.sourceCode == other.sourceCode and self.time == other.time

    def __hash__(self):
        return hash((self.sourceCode, self.time))

    def compareTime(self, other):
        retVal = None
        if self.sourceCode == other.sourceCode:
            if self.time < other.time:
                retVal = -1
            elif self.time > other.time:
                retVal = 1
            else:
                retVal = 0
        return retVal
