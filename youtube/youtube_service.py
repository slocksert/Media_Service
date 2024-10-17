import logging
from pytubefix import YouTube
from data_dto import DataDto

logging.basicConfig(level=logging.DEBUG)

class YoutubeService:

    def download_video(self, video):
        try:
            logging.debug(f"Starting download for video: {video['videoUrl']}")
            yt_video = YouTube(video['videoUrl'])
            logging.debug("YouTube video object created")

            stream = yt_video.streams.filter(file_extension='mp4', only_video=True).first()
            logging.debug(f"Stream found: {stream}")

            if stream is not None:
                video_name = stream.title
                video_url = stream.url
                channel_name = yt_video.author

                data = DataDto(
                    id=video['id'],
                    videoName=video_name,
                    videoUrl=video_url,
                    channelName=channel_name,
                    cookies=''
                )
                logging.debug("DataDto object created")
                logging.debug(f"Data: {data.to_dict()}")
                return data
            else:
                logging.debug("No compatible video found.")
                return None
        except Exception as e:
            logging.error(f"An error occurred during download: {str(e)}")
            return None