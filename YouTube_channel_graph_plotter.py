import csv
import json
import matplotlib.pyplot as plt
import re
import urllib.request


class Channel:

    def __init__(self, username):
        self.api_key = "AIzaSyCFz_mD6HVPoaICeveS-SrIxrBqJ98kslo"
        self.max_result=25

        if self.api_key == "":
            print("please type your Youtube_API_Key: ")
            self.api_key = input()
        self.username=username
        uploads_playlist = self.get_uploads_playlist()

        self.video_id_list = []
        self.get_videos()

    def get_uploads_playlist(self):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={self.username}&key={self.api_key}"

        json_url = urllib.request.urlopen(url)
        self.channel_raw_data = json.loads(json_url.read())
        self.channel_name = self.channel_raw_data["items"][0]["snippet"]["title"]
        uploads = self.channel_raw_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&max_results={str(self.max_result)}&playlistId={uploads}&key={self.api_key}"

        self.uploads_playlist = json.loads(urllib.request.urlopen(url).read())

    def get_videos(self):
        for video in self.uploads_playlist["items"]:
            video_id = video["snippet"]["resourceId"]["videoId"]
            url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,statistics&key={self.api_key}"
            channel_raw_data = json.loads(urllib.request.urlopen(url).read())
            self.video_id_list.append(channel_raw_data)
        
    def print_graph(self, *argv):
        x = 0
        xlist = []
        for video in range(self.max_result):
            xlist.append(x)
            x += 1
            
        plt.subplot(211)
        for args in argv:
            plt.plot(xlist,list(map(int,args.data_list)),label=args.type)
        plt.xlabel("video_id No.")
        plt.ylabel("View count")
        plt.title("YouTube Channel: " + self.channel_name)
        plt.legend()
        
        plt.subplot(212)
        viewCount = int(self.channel_raw_data["items"][0]["statistics"]["viewCount"])
        subscriberCount = int(self.channel_raw_data["items"][0]["statistics"]["subscriberCount"])
        slices=[viewCount,subscriberCount]
        label=["viewCount","subscriberCount"]
        plt.pie(slices, labels=label)
        plt.legend()
        
        plt.subplots_adjust(left=0.08, bottom=0.00, right=0.93, top=0.90,wspace=0.20,hspace=0.25)
        plt.savefig(f"{self.username}.png")
        plt.close()
        
        
class video_data:
    def __init__(self, video_id_list, type):
        self.type=type
        self.data_list = []
        for video in video_id_list:
            views = int(video["items"][0]["statistics"][type])
            self.data_list.append(views)


def main():
    print("please type the YouTube channel ID that you want to view: ")
    username = input()
    input_channel = Channel(username)
    video_list = input_channel.video_id_list
    view = video_data(video_list,"viewCount")
    like = video_data(video_list,"likeCount")
    dislike = video_data(video_list,"dislikeCount")
    comment = video_data(video_list,"commentCount")
    input_channel.print_graph(view, like, dislike, comment)

    
if __name__ == "__main__":
    main()
