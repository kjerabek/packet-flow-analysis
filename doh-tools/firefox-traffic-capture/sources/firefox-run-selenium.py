#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from browsermobproxy import Server
from xvfbwrapper import Xvfb
import sys, time, random, logging
from shutil import which

logger = logging.getLogger("firefox-traffic-capture")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def getFirefoxWebdriver(proxy=None):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.newtabpage.enabled", False)
    profile.set_preference("browser.newtabpage.enhanced", False)
    profile.set_preference("browser.newtabpage.introShown", False)
    profile.set_preference("browser.newtabpage.directory.ping", "")
    profile.set_preference("browser.newtabpage.directory.source", "data:application/json,{}")
    profile.set_preference("browser.newtab.preload", False)
    profile.set_preference("toolkit.telemetry.reportingpolicy.firstRun", False)
    profile.set_preference("http.response.timeout", 2)
    profile.set_preference("dom.max_script_run_time", 2)



    profile.set_preference("network.trr.mode", 2)
    profile.set_preference("network.trr.uri", "https://mozilla.cloudflare-dns.com/dns-query")
    #profile.set_preference("network.trr.bootstrapAddress", "8.8.8.8")

    if proxy:
        profile.set_proxy(proxy.selenium_proxy())

    options = Options()
    options.binary = which("firefox")
    #options.add_argument("-headless")

    return webdriver.Firefox(firefox_profile=profile,
                            firefox_options=options,
                            log_path="/tmp/gecko.log")

def runSingleRequest():
    logger.info("Running single request mode")
    display = Xvfb()
    display.start()

    driver = getFirefoxWebdriver()
    driver.set_page_load_timeout(5)

    try :
        logger.debug("Starting driver.get: " + sys.argv[1])
        driver.get('http://' + sys.argv[1])
        logger.debug("Successful get")

        driver.execute_script("window.stop();")
        driver.quit()
        display.stop()
    except TimeoutException as e:
        logger.debug(e)

        driver.execute_script("window.stop();")
        driver.quit()
        display.stop()

    logger.info("Finished single request mode")


def runProxyHarRequest():
    logger.info("Running proxy request mode")
    outfile = open(sys.argv[3], "w+")
    port = {'port': 50000 + random.randint(1,10000)}
    server = Server("/sources/browsermob-proxy-2.1.4/bin/browsermob-proxy", port)
    server.start()

    time.sleep(1)
    proxy = server.create_proxy()
    time.sleep(1)

    display = Xvfb()
    display.start()
    driver = getFirefoxWebdriver(proxy)
    driver.set_page_load_timeout(5)

    proxy.new_har(sys.argv[1], options={'captureHeaders': True})

    try :
        logger.debug("Starting driver.get: " + sys.argv[1])
        driver.get('http://' + sys.argv[1])
        logger.debug("Successful get")

        driver.execute_script("window.stop();")
        outfile.write(str(proxy.har))
        server.stop()
        driver.quit()
        display.stop()
    except TimeoutException as e:
        logger.debug(e)
        driver.execute_script("window.stop();")

        outfile.write(str(proxy.har))
        logger.debug("Network log written into file: " + sys.argv[3])
        server.stop()
        driver.quit()
        display.stop()

    logger.info("Finished proxy request mode")



if __name__ == "__main__":
    if sys.argv[2] != "proxy":
        runSingleRequest()
    else:
        runProxyHarRequest()
