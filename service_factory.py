from video_services import TikTokService, YoutubeService, TwitterService


class ServiceFactory:
    @staticmethod
    def get_service(platform):
        services = {
        'youtube': YoutubeService(),
        'tiktok': TikTokService(),
        'twitter': TwitterService()
        }
        return services.get(platform)