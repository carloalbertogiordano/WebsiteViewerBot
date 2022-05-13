from re import T
from turtle import done
from types import NoneType
import requests
from random import choice
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import sys
from multiprocessing import Process
import os
import signal

import time

def proxy_generator():
    #Site with proxy list
    response = requests.get("https://sslproxies.org/")
    #Used to extract list of proxies
    soup = BeautifulSoup(response.content, 'html5lib')
    #list containing ips
    x1 = soup.findAll('td')[::8]
    #list containing ports
    x2 = soup.findAll('td')[1::8]
    result = []
    #This for makes the result look like ip:port instread of <br>ip</br>:<br>port</br>
    for i in range(len(x1)):
        ip = str(x1[i])
        port = str(x2[i])
        ip_port = (  ip[4:-5] + ":" + port[4:-5] )
        result.append(ip_port)
    return result

def closeDialog ():
    while True:
        ch = input('Do you want to quit the program y/n?')
        if ch == 'y':
            os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)
            exit()

def openBrowserWithProxy(url, proxy):
    # instantiate a chrome options object so you can set the size and headless preference
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=920x80")
    #use proxy
    chrome_options.add_argument( '--proxy-server='+proxy )
    #avoid dialogs
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    # go to the url
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    while True:
        time.sleep(1)

def openBrowsers(url):
    #Generate proxy list
    proxies = proxy_generator()
    #Number of browsers to open
    MaxInstances = int(sys.argv[2])

    for proxy in proxies:
        if MaxInstances > 0:
            print("CurrentProxy " + proxy)
            try:
                MaxInstances = MaxInstances - 1
                print("Remaining instances "+str(MaxInstances))
                #Create browser process
                p = Process(target=openBrowserWithProxy, args=(url, proxy))
                
                if p.pid is NoneType:
                    print("Could not create process")
                    exit()
                #Make it daemon so that father tries to terminate them before exiting
                p.daemon=True
                p.start()
                print("Started: "+str(p.pid))
                print(" ")
                
            except OSError as e:
                # Proxy returns Connection error
                print(e)
    #Closing dialog y/n
    closeDialog()


if __name__ == '__main__':
    #check_Proxy()
    openBrowsers(sys.argv[1])
    print('The program is terminated')
