from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import logging
from data_dto import DataDto

logging.basicConfig(level = logging.DEBUG)
logging.getLogger("selenium").setLevel(logging.WARNING)

class SeleniumService:
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

    def download_video(self, video):
        try:
            self.driver.get(video['videoUrl'])
            
            video_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'video'))
            )

            source_elements = video_element.find_elements(By.CSS_SELECTOR, 'source')

            if not source_elements:
                videoUrl = video_element.get_attribute("src")
            else:
                videoUrl = source_elements[0].get_attribute("src")

            videoName_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1fbzdvh-H1Container.ejg0rhn1'))
            )
            channelName_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1c7urt-SpanUniqueId.evv7pft1'))
            )

            videoName = videoName_element.text
            channelName = channelName_element.text

            cookies = self.driver.get_cookies()
            cookies = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

            data_dto = DataDto(
                id=video['id'],
                videoName=videoName,
                videoUrl=videoUrl,
                channelName=channelName,
                cookies=cookies,
            )

            logging.debug(f"Video saved successfully from {channelName}")

            return data_dto

        except Exception as e:
            logging.error(f"Error downloading video: {e}")
            return None

        finally:
            self.driver.quit()