from .aggregate import aggregate

import fnmatch
import itertools


class aggregateData(aggregate):
    """
    Aggregate column expands based off of the input columns
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # use a set here for fast lookup later as it will mostly be lookup
        self.aggregateColumns: set = set()

    def getDataColumnsNotUsed(self) -> list[str]:
        """
        find if there are new columns that have not already been processed by an aggregate action
        """
        dataColumns = []
        # combine them both to be a tuple
        calcKeys = []
        # if this is a trigger aggregate we get the calc keys
        # otherwise get the newCalc keys
        if self.feed.newCalcData is None:
            if self.feed.calcData is not None:
                calcKeys = self.feed.calcData.keys()
        else:
            calcKeys = self.feed.newCalcData.keys()

        for seq in (self.feed.data.keys(), calcKeys):
            # then iterate over each key view
            for key in seq:
                # make sure we haven't already processed that column
                if key not in self.aggregateColumns:
                    dataColumns.append(key)

        return dataColumns

    def findWildCardMatchColumns(
        self, dataColumns: list[str], wildcardActionInputCols: list[str]
    ) -> list[list]:
        """
        Using an input list of columns and a list of wild card columns find a
        list of lists for all columns that go with each wildcard input col
        """
        wildcardMatchColumns: list[list] = []
        for columnPattern in wildcardActionInputCols:
            columnMatchList = []
            # iterating over a copy here as we're going to remove while iterating
            for dataColumn in list(dataColumns):
                if fnmatch.fnmatch(dataColumn, columnPattern):
                    columnMatchList.append(dataColumn)
                    dataColumns.remove(dataColumn)
            wildcardMatchColumns.append(columnMatchList)
        return wildcardMatchColumns

    def getColumnsBasedOnWildcard(self) -> dict[str, list[str]]:
        """
        Return dictionary of action key -> input column list
        This will group the wildcard matching based on a key
        they key is determined by what strings are in the wildcard section
        """
        dataColumns = self.getDataColumnsNotUsed()

        # The input columns to the aggregate action contain the wildcard columns
        # so now we comprise lists of all the columns that match those wildcards
        wildcardMatchColumns = self.findWildCardMatchColumns(dataColumns, self.input)

        actionInputCols: dict[str, list[str]] = {}

        # Once we've found all the columns that match the wildcard patterns let's pair them together
        # but we only need to do this if len(self.input) > 1
        firstColumnPatternSplit = self.input[0].split("*")
        firstColumnPatternSplit.remove("")
        for column in wildcardMatchColumns[0]:
            input = [column]
            # find the part of the column that are the wildcard parts
            columnKeys = []
            index = column.index(firstColumnPatternSplit[0])
            # have to get up to the first pattern as the wild card was at the start
            if index != 0:
                columnKeys.append(column[0:index])
            prevPattern = firstColumnPatternSplit[0]
            for patternSplitStr in firstColumnPatternSplit[1:]:
                nextIndex = column.index(patternSplitStr)
                columnKeys.append(patternSplitStr[index + len(prevPattern) : nextIndex])
                index = nextIndex
                prevPattern = patternSplitStr

            # check if there's more after the last pattern
            if index + len(prevPattern) != len(column):
                columnKeys.append(column[index + len(prevPattern) : len(column)])

            # now that we have all the parts of the column that were the wildcard, lets find the groupings
            for columnList in wildcardMatchColumns[1:]:
                for column in columnList:
                    if all(key in column for key in columnKeys):
                        input.append(column)
                        columnList.remove(column)
                        break

            # let's make sure at the end we have the expected amount of columns
            if len(input) == len(self.input):
                actionInputCols[columnKeys[0]] = input
                # these columns are now defenitely going to be used so barring a major problem add them here
                self.aggregateColumns.update(input)

        return actionInputCols

    def modifyCombinedActionAggregate(self):
        """
        For combined actions there is only child action, so we modify its input columns
        """
        actionInputCols = self.getCombinedColumnsColumnsBasedOnWildcard()
        self.childActions[0].input.extend(actionInputCols)

    def getCombinedColumnsColumnsBasedOnWildcard(self) -> list[str]:
        """
        For a combined aggregate get the columns that match the wildcard
        """
        dataColumns = self.getDataColumnsNotUsed()

        # The input columns to the aggregate action contain the wildcard columns
        # so now we comprise lists of all the columns that match those wildcards
        wildCardMatchColumns = self.findWildCardMatchColumns(dataColumns, self.input)
        # this gave us a list of list, but we want to flatten it
        actionInputCols = list(itertools.chain.from_iterable(wildCardMatchColumns))
        self.aggregateColumns.update(actionInputCols)
        return actionInputCols

    def addNewChildren(self) -> None:
        """
        aggregate update has been called so we must create the children actions of the aggregate
        in turn these children will be called update on for this time and future times
        """
        if self.combined:
            # if it's combined then we're only creating one action with all the wild card matching as input cols
            actionInputCols = self.getCombinedColumnsColumnsBasedOnWildcard()
            if len(actionInputCols) > 0:
                newAction = self.createChildAction()
                newAction.input = actionInputCols
                newAction.aggregate = False
                self.childActions.append(newAction)
        else:
            actionInputCols = self.getColumnsBasedOnWildcard()
            for key, columns in actionInputCols.items():
                newAction = self.createChildAction()
                newAction.input = columns
                newAction.name += "-" + key
                newAction.aggregate = False
                self.childActions.append(newAction)
