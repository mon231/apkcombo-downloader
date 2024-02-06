import time
import requests
from time import sleep
from pathlib import Path
from argparse import ArgumentParser
from selenium.webdriver.common.by import By
import undetected_chromedriver as webdriver

def parse_args():
    arguments_parser = ArgumentParser('apk files downloader, using apkcombo website')

    arguments_parser.add_argument('--path', type=Path, required=True, help='target apk path')
    arguments_parser.add_argument('--package', type=str, required=True, help='name of package to download')
    arguments_parser.add_argument('--language', type=str, required=False, default='en', help='target app language (e.g. en for english, es para espanol, ...)')
    arguments_parser.add_argument('--device', type=str, required=False, choices=['phone', 'tablet', 'tv', 'default'], default='default', help='name of package to download')
    arguments_parser.add_argument('--architecture', type=str, required=False, choices=['arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64', 'default'], default='default', help='architecture of package to download')
    arguments_parser.add_argument('--dpi', type=int, required=False, choices=[120, 160, 240, 320, 480, 640, 213], default=480, help='dpi of package to download')
    arguments_parser.add_argument('--sdk', type=str, required=False, choices=['default'] + [str(sdk_version) for sdk_version in range(21, 33)], default='default', help='android-sdk of package to download')

    return arguments_parser.parse_args()


def download_file(url: str, output_path: Path):
    with requests.get(url, stream=True) as request_stream:
        request_stream.raise_for_status()

        with open(output_path, 'wb') as output_file:
            DEFAULT_CHUNK_SIZE = 8192

            for chunk in request_stream.iter_content(chunk_size=DEFAULT_CHUNK_SIZE):
                output_file.write(chunk)


def get_headless_chrome_options() -> webdriver.ChromeOptions:
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    return chrome_options


def main():
    arguments = parse_args()

    website_url = f'https://apkcombo.com/downloader/#package={arguments.package}&device={arguments.device}&sdk={arguments.sdk}&arches={arguments.architecture}&dpi={arguments.dpi}&lang={arguments.language}'
    print(f'About to download from web page {website_url}')

    browser = webdriver.Chrome(options=get_headless_chrome_options())
    browser.start_session()
    
    browser.get(website_url)
    page_loaded_timepoint = time.time()
    
    while not browser.find_elements(By.CLASS_NAME, 'file-list'):
        DOWNLOAD_URL_LOAD_TIMEOUT_SEC = 10
        if time.time() - page_loaded_timepoint > DOWNLOAD_URL_LOAD_TIMEOUT_SEC:
            raise RuntimeError('download-url load time reached timeout')

        DOWNLOAD_URL_EXISTENCE_CHECK_DELAY_SEC = 0.5
        sleep(DOWNLOAD_URL_EXISTENCE_CHECK_DELAY_SEC)
        
    files_list = browser.find_element(By.CLASS_NAME, 'file-list')
    download_url = files_list.find_element(By.TAG_NAME, 'a').get_attribute('href')

    print(f'About to download {download_url} into {arguments.path}')
    download_file(download_url, arguments.path)

    print(f'Successfully downloaded {arguments.package} package, at {arguments.path}')
    browser.quit()


if __name__ == '__main__':
    main()
