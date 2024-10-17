from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import logging
from decouple import config
from data_dto import DataDto

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("selenium").setLevel(logging.WARNING)

class TwitterService:
    def __init__(self):
        self.driver = self._create_driver()

    def _create_driver(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/google-chrome"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def parse_video_id(self, video_url):
        return video_url.split('/')[-1]

    def download_video(self, video):
        try:
            logging.debug(f"Starting download for video: {video['videoUrl']}")
            video_id = self.parse_video_id(video['videoUrl'])
            download_page_url = f"{config('URL')}{video_id}"
            
            self.driver.get(download_page_url)
            
            sources = self.driver.find_elements(By.TAG_NAME, "source")
            video_name_element = self.driver.find_element(By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-h6.MuiTypography-gutterBottom")
            channel_name_elements = self.driver.find_element(By.CSS_SELECTOR, "h6[class='MuiTypography-root MuiTypography-h6']")
            
            if video_name_element:
                video_name = video_name_element.text
            else:
                video_name = "Unknown"

            channel_name = channel_name_elements.text
            
            if not sources:
                video_element = self.driver.find_element(By.TAG_NAME, "video")
                video_url = video_element.get_attribute('src') 
            else:
                video_url = sources[1].get_attribute('src')
        
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
        
        except Exception as e:
            logging.error(f"Erro ao buscar a tag <source>: {e}")
            return None
        finally:
            self.driver.quit()
            logging.debug("Driver quit successfully")