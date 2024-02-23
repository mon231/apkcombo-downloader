import requests
from typing import List
import undetected_chromedriver as webdriver
from tcp_tuple import TcpTuple


class ProxyManager:
    def __init__(self):
        self.__proxies_list = ProxyManager.__fetch_proxies()
        self.__next_proxy_index = 0

    def get_proxied_undetected_browser(self) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        proxy = self.__get_next_proxy()
        chrome_options.add_argument(f'--proxy-server={proxy}')

        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        browser = webdriver.Chrome(options=chrome_options)
        browser.start_session()

        return browser

    def __get_next_proxy(self) -> TcpTuple:
        if self.__next_proxy_index >= len(self.__proxies_list):
            raise RuntimeError('No more proxies to use')

        current_proxy_index = self.__next_proxy_index
        self.__next_proxy_index += 1

        return self.__proxies_list[current_proxy_index]

    @staticmethod
    def __fetch_proxies() -> List[TcpTuple]:
        PROXIES_COLLECTION_WEBSITE = 'https://www.sslproxies.org'

        proxies_website_reponse = requests.get(PROXIES_COLLECTION_WEBSITE)
        proxies_list = proxies_website_reponse.text.split('</textarea>')[0].split('UTC.\n\n')[1].splitlines()

        return [TcpTuple(tcp_pair.split(':')[0], int(tcp_pair.split(':')[1])) for tcp_pair in proxies_list]
