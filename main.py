import os
import traceback
import wget
import time
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

import requests
import os

proxy_user = "celengspeed"
proxy_pass = "celengspeed"
proxy_host = "103.197.190.122"
proxy_port = "1080"

socks_proxy = f"socks5h://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

# --- Requests ---
proxies = {
    "http": socks_proxy,
    "https": socks_proxy,
}



def download_video(url: str, save_path: str = "video.mp4"):
    try:
        # request dengan stream=True biar tidak boros RAM
        with requests.get(url, stream=True, timeout=20, proxies=proxies) as r:
            print("status", r)
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            
            # bikin folder kalau belum ada
            os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
            
            with open(save_path, "wb") as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        done = int(50 * downloaded / total_size) if total_size else 0
                        print(f"\r[{'█' * done}{'.' * (50-done)}] {downloaded}/{total_size} bytes", end="")
        
        print(f"\n✅ Download selesai: {save_path}")
        return save_path
    except Exception as e:
        print(f"❌ Gagal download: {e}")
        return None


def KillPid():
    try:
        # Kill Chrome dan Chromedriver di Windows
        os.system("taskkill /F /IM chrome.exe /T")
        os.system("taskkill /F /IM chromedriver.exe /T")
    except:
        pass

class VHtearDriver:
    def __init__(self):
        self.options = Options()
        # Lokasi default Chrome di Windows
        self.options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(self.options.binary_location):
            self.options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        

        #self.options.add_argument('--headless=new')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-logging')
        self.options.add_argument('--log-level=3')
        self.options.add_argument('--silent')

        self.service = Service(ChromeDriverManager().install())

    def youtubeDownload(self, youtube_url):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        dataNE = {}
        try:
            self.driver.get("https://yt-mp4.org/")
            input_form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'input[placeholder="Enter YouTube URL here..."]')
                )
            )
            input_form.clear()
            input_form.send_keys(youtube_url)
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(text(), "Fetch Video")]')
                )
            )
            button.click()

            for i in range(30): 
                try:
                    download_section = self.driver.find_element(By.ID, "downloadSection")
                    print("✅ Download section muncul!")
                    break
                except NoSuchElementException:
                    print(f"⏳ Belum muncul... ({i+1})")
                    time.sleep(0.5)
            else:
                raise Exception("❌ Download section tidak muncul dalam 30 detik")

            for i in range(30):
                try:
                    get_link_button = self.driver.find_element(By.CSS_SELECTOR, "button.bg-green-600")
                    get_link_button.click()
                    print("🔗 Tombol Get Link diklik")
                    break
                except NoSuchElementException:
                    print(f"⏳ Tombol Get Link belum ada... ({i+1})")
                    time.sleep(1)
            else:
                raise Exception("❌ Tombol Get Link tidak ditemukan dalam 30 detik")

            for i in range(30):
                try:
                    download_button = self.driver.find_element(
                          By.CSS_SELECTOR,
                          "a.text-white.rounded-lg.p-2.text-center"
                      )
                    download_link = download_button.get_attribute("href")
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")

                    img = soup.find("img")
                    original_url = ""
                    if img:
                        src = img["src"]
                        if "url=" in src:
                            original_url = unquote(src.split("url=")[1].split("&")[0])
                            print("URL Asli:", original_url)
                        else:
                            print("SRC:", src)
                    print("✅ Link download:", download_link)
                    ce = "jancok"
                    dataNE = {
                            'status': 200,
                            'img': original_url,
                            'url_ori': download_link,
                            'url': "https://crot.sosmedboost.com/media/local_storage_v2/mp4/"+ce+".mp4",
                          }
                    self.driver = webdriver.Chrome(service=self.service, options=self.options)
                    download_video(download_link)
                    return dataNE
                except NoSuchElementException:
                    print(f"⏳ Link download belum siap... ({i+1})")
                    time.sleep(1)
            else:
                raise Exception("❌ Link download tidak tersedia dalam 30 detik")
        except:
          print(traceback.format_exc())
          KillPid()
        finally:
          KillPid()

VHdriver = VHtearDriver()
sw = VHdriver.youtubeDownload("https://youtu.be/rdD-dKr-L-I?si=PT-oBsfEWa5ecZvv")
print(sw)
