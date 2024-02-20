from . import mpLogging

import os
import pickle
import yaml
import configparser
import re

VALUES_SECTION = "Values"


class ConfigLoader:
    def __init__(self, settingsFile=None):
        # can look up full key value or just further in
        # Only using section name if it exists, otherwise not including
        # MainSettingsKey.SectionName.Key = Value
        # MainSettingsKey.Key = Value
        # SetcionName.Key = Value
        # Key = Value
        self.valueDict = {}
        if settingsFile:
            self.loadValues(settingsFile)

    def loadValues(self, settingsFile):
        parser = configparser.ConfigParser()
        parser.read(settingsFile)
        if VALUES_SECTION in parser.sections():
            valuesTupleList = parser.items(VALUES_SECTION)
            for settingsKey, settingsValue in valuesTupleList:
                settingsKey = settingsKey.lower()
                if os.path.exists(settingsValue):
                    parser = configparser.ConfigParser()
                    with open(settingsValue) as stream:
                        # appending a section just in case a section was never passed in
                        parser.read_string("[top]\n" + stream.read())
                    for section in parser.sections():
                        for fileKey, fileValue in parser.items(section):
                            self.valueDict[str(settingsKey) + "." + str(fileKey)] = (
                                fileValue
                            )
                            if section != "top":
                                self.valueDict[
                                    str(settingsKey)
                                    + "."
                                    + str(section)
                                    + "."
                                    + str(fileKey)
                                ] = fileValue
                                self.valueDict[str(section) + "." + str(fileKey)] = (
                                    fileValue
                                )
                            self.valueDict[str(fileKey)] = fileValue
                else:
                    mpLogging.warning(
                        "Path provided but not found",
                        description=f"Key: {settingsKey} Value/Path: {settingsValue}",
                    )
        else:
            print("No default values provided")

    def matchReplace(self, reMatch):
        string = reMatch.group(0)
        if len(string) > 3:
            string = string[2 : len(string) - 1]
            # need to use lower() becuase configParser converst keys to lower
            if string.lower() in self.valueDict:
                return self.valueDict[string.lower()]
        return string

    def loadAndReplaceYamlFile(self, path):
        contents = {}
        try:
            with open(path) as file:
                contents = yaml.safe_load(self.replaceStrings(file.read()))
        except OSError:
            mpLogging.error("Exception loading file", description=f"File: {path}")
        return contents

    def replaceStrings(self, file_stirng):
        if len(file_stirng) > 0:
            return re.sub(r"\$\[[^]]*\]", self.matchReplace, file_stirng)


def saveObj(obj, name):
    with open("../obj/" + name + ".pkl", "wb+") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def pickleConfigFile(path):
    with open(path) as file:
        saveObj(
            yaml.safe_load(file),
            os.path.splitext(os.path.split(path)[1])[0],
        )


def getKeyValueIni(iniFile):
    valueDict = {}
    parser = configparser.ConfigParser()
    with open(iniFile) as stream:
        # appending a section just in case a section was never passed in
        parser.read_string("[top]\n" + stream.read())
    for section in parser.sections():
        for fileKey, fileValue in parser.items(section):
            valueDict[str(fileKey)] = fileValue
    return valueDict


def dfsConfigDict(config, match, do):
    def dfs(c):
        if isinstance(c, str):
            return
        try:
            c.items()
        except AttributeError as _:
            try:
                for v in c:
                    pass
            except TypeError as _:
                pass
            else:
                for v in c:
                    dfs(v)
        else:
            for k, v in c.items():
                if match(c, k, v):
                    do(c, k, v)
                else:
                    dfs(v)

    dfs(config)
