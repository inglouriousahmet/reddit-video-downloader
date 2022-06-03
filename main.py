import json
import urllib.request
import requests

class Downloader():
    def __init__(self):
        pass
        

    def get_json(self):

        submission_permalink = input("Video post link: ").split('?')
        submission_json_link = "%s.json"% submission_permalink[0][:-1]
        get_json_data_of_submission = requests.get(submission_json_link,headers={"user-agent":"Ubuntu; Linux:videodownloader:v1.0"})
        load_json_data_content = json.loads(get_json_data_of_submission.content.decode('utf-8'))
        json_data_of_submission = json.dumps(load_json_data_content,indent=4, sort_keys=True)
        
        self.submission_id = load_json_data_content[0]["data"]["children"][0]["data"]["id"]
        self.url = load_json_data_content[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"].split('?')
        self.video_url = self.url[0]
        self.is_gif = load_json_data_content[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["is_gif"]

        with open('json/%s.json'% self.submission_id,'w') as json_file:
            json_file.write(json_data_of_submission)

    def get_video(self):
        urllib.request.urlretrieve(self.video_url,filename="video/%s_video.mp4"% self.submission_id)
        if not self.is_gif:
            raw_video_url = self.video_url.split('_')
            raw_video_format = raw_video_url[1].split('.')
            audio_url = "%s_audio.%s"% (raw_video_url[0],raw_video_format[1])
            urllib.request.urlretrieve(audio_url,filename="audio/%s_audio.mp4"% self.submission_id)

    def main(self):
        self.get_json()
        self.get_video()

if __name__ == "__main__":
    downloader = Downloader()
    downloader.main()