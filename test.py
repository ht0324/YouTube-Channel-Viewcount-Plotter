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
        video_id_list.append(data)
    return video_id_list
    
def get_data(video_id_list,type):
    data_list = []
    for video in video_id_list:
        views = int(video["items"][0]["statistics"][type])
        data_list.append(views)
    return data_list

class video_data:
    def __init__(self, video_id_list, type):
        self.type=type
        self.video_id_list=video_id_list
        self.data_list = []
        for video in video_id_list:
            views = int(video["items"][0]["statistics"][type])
            self.data_list.append(views)
            
    def print_graph(self):
        x = 0
        xlist = []
        for video in range(len(self.data_list)):
            xlist.append(x)
            x += 1
        plt.plot(xlist,list(map(int,self.data_list)),label=self.type)
        plt.xlabel("video_id No.")
        plt.ylabel("View count")
        plt.title("YouTube Channel: " + channel_name)
        plt.show()

def print_graph(*argv):
    x = 0
    xlist = []
    for video in range(max_results):
        xlist.append(x)
        x += 1
    for args in argv:
        plt.plot(xlist,list(map(int,args.data_list)),label=args.type)
    plt.xlabel("video_id No.")
    plt.ylabel("View count")
    plt.title("YouTube Channel: " + channel_name)
    plt.show()

def main():
    global channel_name, max_results
    max_results = 25
    channel_name = "unboxtherapy"
    data = get_uploads_playlist()
    video_id_list=get_videos(data)
    view=video_data(video_id_list,"viewCount")
    like=video_data(video_id_list,"likeCount")
    dislike=video_data(video_id_list,"dislikeCount")
    comment=video_data(video_id_list,"commentCount")
    print_graph(view, like, dislike, comment)

    
if __name__ == "__main__":
    main()
