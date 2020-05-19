import csv
import json
import matplotlib.pyplot as plt
import re
import urllib.request

api_key = sys.argv[1]
channel_name = None
max_results = None

def get_uploads_playlist():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={channel_name}&key={api_key}"

    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    uploads = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&max_results={str(max_results)}&playlistId={uploads}&key={api_key}"

    return json.loads(urllib.request.urlopen(url).read())

def get_videos(data):
    video_id_list = []
    for video in data["items"]:
        video_id = video["snippet"]["resourceId"]["videoId"]
        url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,statistics&key={api_key}"
        data = json.loads(urllib.request.urlopen(url).read())
#        print(data["items"][0]["statistics"])
        video_id_list.append(data)
    return video_id_list
    
def get_data(video_id_list,type):
    data_list = []
    for video in video_id_list:
        views = int(video["items"][0]["statistics"][type])
        data_list.append(views)
    return data_list

def print_graph(data_list):
    x = 0
    xlist = []
    for video in range(len(data_list)):
        xlist.append(x)
        x += 1
    plt.plot(xlist,list(map(int,data_list)))
    plt.xlabel("video_id No.")
    plt.ylabel("View count")
    plt.title("YouTube Channel: " + channel_name)
    plt.show()
    
def main():
    global channel_name, max_results
    max_results = 50
    channel_name = "unboxtherapy"
#    channel_name=input()
    data = get_uploads_playlist()
    video_id_list=get_videos(data)
    view = get_data(video_id_list,"viewCount")
#    like = get_data(video_id_list,"likeCount")
#    dislike = get_data(video_id_list,"dislikeCount")
#    comment = get_data(video_id_list,"commentCount")
    print_graph(view)
    
if __name__ == "__main__":
    main()
