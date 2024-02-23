import time
import requests
from pathlib import Path
from argparse import ArgumentParser
from selenium.webdriver.common.by import By
from proxy_manager import ProxyManager


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
            DOWNLOAD_CHUNK_SIZE = 8192

            for chunk in request_stream.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                output_file.write(chunk)


def get_download_url(package: str, device: str, sdk: str, architecture: str, dpi: int, language: str):
    return f'https://apkcombo.com/downloader/#package={package}&device={device}&sdk={sdk}&arches={architecture}&dpi={dpi}&lang={language}'


def download_using_proxy(proxy_manager: ProxyManager, target_path: Path, package: str, device: str, sdk: str, architecture: str, dpi: int, language: str):
    browser = proxy_manager.get_proxied_undetected_browser()
    website_url = get_download_url(package, device, sdk, architecture, dpi, language)

    browser.get(website_url)
    page_loaded_timepoint = time.time()

    while not browser.find_elements(By.CLASS_NAME, 'file-list'):
        DOWNLOAD_URL_LOAD_TIMEOUT_SEC = 10

        if time.time() - page_loaded_timepoint > DOWNLOAD_URL_LOAD_TIMEOUT_SEC:
            raise RuntimeError('download-url load time reached timeout')

        DOWNLOAD_URL_EXISTENCE_CHECK_DELAY_SEC = 0.5
        time.sleep(DOWNLOAD_URL_EXISTENCE_CHECK_DELAY_SEC)

    files_list = browser.find_element(By.CLASS_NAME, 'file-list')
    download_url = files_list.find_element(By.TAG_NAME, 'a').get_attribute('href')

    print(f'About to download {download_url} into {target_path}')
    download_file(download_url, target_path)

    print(f'Successfully downloaded {package} package, at {target_path}')
    browser.quit()


def main():
    arguments = parse_args()
    proxy_manager = ProxyManager()

    DOWNLOAD_ATTEMPTS_COUNT = 5
    for _ in range(DOWNLOAD_ATTEMPTS_COUNT):
        try:
            download_using_proxy(
                proxy_manager,
                arguments.path,
                arguments.package,
                arguments.device,
                arguments.sdk,
                arguments.architecture,
                arguments.dpi,
                arguments.language
            )
        except RuntimeError as e:
            print('download error:', e)


if __name__ == '__main__':
    main()
