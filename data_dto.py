import json

class DataDto:
    def __init__(self, id, videoName, videoUrl, channelName, cookies):
        self.id = id
        self.videoName = videoName
        self.videoUrl = videoUrl
        self.channelName = channelName
        self.cookies = cookies

    def to_dict(self):
        return {
            'id': self.id,
            'videoName': self.videoName,
            'videoUrl': self.videoUrl,
            'channelName': self.channelName,
            'cookies': self.cookies
        }

    def to_json(self):
        return json.dumps(self.to_dict())