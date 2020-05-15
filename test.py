import json
import re
import urllib.request
import matplotlib.pyplot as plt
import csv
import sys

# from pytube import YouTube

api_key = sys.argv[1]
channelname=None
maxResults=None
def getUploadsPlaylist():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={channelname}&key={api_key}"

    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    uploads=data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults={maxResults}&playlistId={uploads}&key={api_key}"

#    json_url = urllib.request.urlopen(url)
    return json.loads(urllib.request.urlopen(url).read())
    
def processData(data):
    dataList=[]
    for i in data["items"]:
        video=i["snippet"]["resourceId"]["videoId"]
        url =f"https://www.googleapis.com/youtube/v3/videos?id={video}&part=snippet,statistics&key={api_key}"
        data = json.loads(urllib.request.urlopen(url).read())
    #    print(data["items"][0]["statistics"])
        views = int(data["items"][0]["statistics"]["viewCount"])
        dataList.append(views)
    return dataList

def printGraph(dataList):
    x=0
    xlist=[]
    for i in range(len(dataList)):
        xlist.append(x)
        x+=1
    plt.plot(xlist,list(map(int,dataList)))
    plt.xlabel("Video No.")
    plt.ylabel("View count")
    plt.title("YouTube Channel: "+channelname)
    plt.show()
    
def main():
    global channelname, maxResults
    maxResults="50"
    channelname="unboxtherapy"
#    channelname=input()
    data=getUploadsPlaylist()
    dataList=processData(data)
    printGraph(dataList)
    
if __name__ == "__main__":
    main()
