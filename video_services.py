from abc import ABC, abstractmethod
from tiktok.tiktok_service import SeleniumService as Tiktok
from youtube.youtube_service import YoutubeService as Youtube
from twitter.twitter_service import TwitterService as Twitter

class VideoService(ABC):
    @abstractmethod
    def download_video(self, video):
        ...

class TikTokService(VideoService):
    def download_video(self, video):
        tiktok_service_instance = Tiktok()
        return tiktok_service_instance.download_video(video)

class TwitterService(VideoService):
    def download_video(self, video):
        twitter_service_instance = Twitter()
        return twitter_service_instance.download_video(video)

class YoutubeService(VideoService):
    def download_video(self, video):
        youtube_service_instance = Youtube()
        return youtube_service_instance.download_video(video)