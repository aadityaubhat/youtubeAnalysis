__author__ = 'aaditya'

from credential import DEVELOPER_KEY
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
# https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_categoryList():
    """
    :return: A Dictionary of youtube categories with categoryID as key and categoryName as value.
    """
    categoryList = {}
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # Call the videoCategories.list method to all the categories.
    search_response = youtube.videoCategories().list(part="snippet", regionCode="us").execute()
    for list in search_response[u'items']:
        categoryList[list[u'id'].encode("utf-8")] = list[u'snippet'][u'title'].encode("utf-8")
    return categoryList

def youtube_popular30(categoryList):
    """
    :param categoryList: A dictionary of youtube video categories with categoryID as key and categoryName as value.
    :return: A dictionary with categoryName as key and a list of top 30 videos for the category as the value. Each video
    is represented by a dictionary having key value for title, viewCount, likeCount, dislikeCount, commentCount.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    result = {}
    for categoryID, categoryName in categoryList.items():
        result[categoryName] = []
        search_response = youtube.videos().list(part="snippet, statistics", chart = "mostPopular", maxResults = 30,regionCode = "us", videoCategoryId = categoryID ).execute()
        if len(search_response[u"items"]):
            for outputList in search_response[u"items"]:
                try:
                    result[categoryName].append({"title": outputList[u"snippet"][u"title"].encode("utf-8"),"viewCount":
                    outputList[u"statistics"][u"viewCount"].encode("utf-8"),
                    "likeCount": outputList[u"statistics"][u'likeCount'].encode("utf-8"),
                    "dislikeCount": outputList[u"statistics"][u"dislikeCount"].encode("utf-8"),
                    "commentCount": outputList[u"statistics"][u"commentCount"].encode("utf-8")})
                except:
                    result[categoryName].append({"title": outputList[u"snippet"][u"title"].encode("utf-8")})
    return result






if __name__ == "__main__":
    categoryList = None
    try:
        categoryList = youtube_categoryList()
        popular30List = youtube_popular30(categoryList)
        firstLine = True
        with open("iPythonNotebook\data.csv", "wb") as file:
            for categoryKey in popular30List:
                if len(popular30List[categoryKey]) >0:
                    for videoDict in popular30List[categoryKey]:
                        if firstLine:
                            file.write("category,title,viewCount,likeCount,dislikeCount,commentCount")
                            firstLine = False
                        if(len(videoDict) == 5):
                            file.write("\n"+categoryKey+","+videoDict['title'].replace(",", "-")+","+videoDict['viewCount']+","+videoDict['likeCount']+","+videoDict['dislikeCount']+","+videoDict['commentCount'])
        file.close()
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
