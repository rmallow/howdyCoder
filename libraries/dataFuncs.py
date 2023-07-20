import praw
from praw.models import MoreComments
from datetime import datetime

import pandas
from urllib.request import urlopen
import json
import random


def irregular(chance=5, passback_dict={}):
    if random.randint(1, chance) == 1:
        passback_dict["num"] = passback_dict.get("num", 0) + 1
        return passback_dict["num"]
    else:
        return None


def getJsonDataStr(url):
    response = urlopen(url)
    return response.read().decode("utf-8")


def getPandasFromUrl(url):
    jsonStr = getJsonDataStr(url)
    return pandas.read_json(path_or_buf=jsonStr)


def setupReddit(clientId=None, clientSecret=None, userAgent=None, **kwargs):
    """algoBuilder"""
    if clientId is not None and clientSecret is not None and userAgent is not None:
        return praw.Reddit(
            client_id=clientId, client_secret=clientSecret, user_agent=userAgent
        )
    else:
        return None


def setupRedditAuth(
    clientId=None, clientSecret=None, userAgent=None, username=None, password=None
):
    if (
        clientId is not None
        and clientSecret is not None
        and userAgent is not None
        and username is not None
        and password is not None
    ):
        return praw.Reddit(
            client_id=clientId,
            client_secret=clientSecret,
            user_agent=userAgent,
            username=username,
            password=password,
        )
    else:
        return None


WORDS = "randomassortmentofwordsin astring that will be spliced later wow look at me go what could this be who knows"


def randomWord(**kwargs):
    """algoBuilder"""
    start = random.randint(0, len(WORDS) - 10)
    end = random.randint(start + 1, len(WORDS))
    return {"word": WORDS[start:end]}


def randomNumber(cap=2, **kwargs):
    return random.randint(0, cap)


def redditTest(reddit=None, subreddit="learnpython", **kwargs):
    data = None
    if reddit is not None:
        data = {"title": [], "time": [], "uid": [], "comment": []}
        redditVals = None
        redditVals = reddit.subreddit(subreddit).new(limit=10)
        if redditVals:
            for submission in redditVals:
                data["title"].append(submission.title)
                commentString = ""
                first = True
                for comment in submission.comments:
                    if isinstance(comment, MoreComments):
                        continue
                    if not first:
                        commentString += "\n"
                    commentString += comment.body

                data["comment"].append(commentString)
                data["time"].append(datetime.utcfromtimestamp(submission.created_utc))
                data["uid"].append(submission.id)
    return data


def redditThreaded(outputQueue, reddit=None, subreddit="learnpython", **kwargs):
    """algoBuilder"""
    for comment in reddit.subreddit(subreddit).stream.comments(
        pause_after=None, skip_existing=True
    ):
        data = {"time": [], "body": [], "uid": []}
        data["time"].append(datetime.utcfromtimestamp(comment.created_utc))
        data["body"].append(comment.body)
        data["uid"].append(comment.id)
        outputQueue.put(data)


def cryptoIndex(fmpURL=None, **kwargs):
    if fmpURL is not None:
        jsonStr = getJsonDataStr(fmpURL)
        jList = json.loads(jsonStr)
        returnDict = {}
        indexValue = 0
        for item in jList:
            if (
                "price" in item
                and item["price"] is not None
                and "sharesOutstanding" in item
                and item["sharesOutstanding"] is not None
                and "symbol" in item
            ):
                returnDict["price-" + item["symbol"]] = item["price"]
                returnDict["sharesOutstanding-" + item["symbol"]] = item[
                    "sharesOutstanding"
                ]
                indexValue += item["price"] * item["sharesOutstanding"]
        returnDict["indexValue"] = indexValue
        return returnDict


def setupCryptoList(url=None, **kwargs):
    cryptoSet = set()
    jList = json.loads(getJsonDataStr(url))
    for item in jList:
        if "symbol" in item:
            # strip off USD, last three characters
            cryptoSet.add(item["symbol"][:-3])
    return {"cryptoList": list(cryptoSet)}


def getWeatherAlerts(url=None, passback_dict={}, **kwargs):
    id = passback_dict.get("weather_id", None)
    if url is not None:
        jsonDict = json.loads(getJsonDataStr(url))
        if "features" in jsonDict:
            feature = jsonDict["features"][0]
            if (
                "id" in feature
                and feature["id"] is not None
                and feature["id"] != id
                and "properties" in feature
            ):
                properties = feature["properties"]
                if "headline" in properties and properties["headline"] is not None:
                    data = {
                        "id": feature["id"],
                        "headline": properties["headline"],
                    }
                    passback_dict["weather_id"] = feature["id"]
                    return data
