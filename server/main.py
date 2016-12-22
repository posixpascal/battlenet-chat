#!/usr/bin/env python3
import logging
import sys; sys.path.append("protos")
import battlenet
import queue
import threading

from flask import Flask
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route("/account.json")
def account():
    with open("data/account.json", "r") as f:
        src = f.read()
    return src

@app.route("/friends.json")
def friends():
    with open("data/friends.json", "r") as f:
        src = f.read()
    return src

@app.route("/messages.json")
def messages():
    with open("data/messages.json", "r") as f:
        src = f.read()
    return src

logging.basicConfig(level=logging.INFO, format="")
logger = logging.getLogger(__name__)


def challenge_handler(url):
    return bytes("YOUR-TOKEN-HERE", "ascii")
    # later configuration
    account_name = ""
    account_password = ""
    url = url.decode('utf-8')

    # use selenium to get token
    driver = webdriver.PhantomJS() # or add to your PATH
    driver.set_window_size(1024, 768) # optional
    driver.get(url)
    while (driver.current_url == url):
        sleep(0.5)
        print("waiting for redirect...")
    print(driver.current_url)


    driver.save_screenshot('screen.png') # save a screenshot to disk
    print("test2")
    elem = driver.find_element_by_name("accountName")
    elem.clear()
    elem.send_keys(account_name)
    print("test3")
    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(account_password)
    print("test4")
    driver.execute_script("")
    submit_btn = driver.find_element_by_id("submit")
    submit_btn.click()
    current_url = driver.current_url
    driver.save_screenshot("screen.png")
    while (driver.current_url == current_url):
        print(driver.current_url)
        driver.save_screenshot("screen.png")
        print(driver.get_log("browser"))
        submit_btn.click()
        sleep(5)
    
    print("url changed: ")
    print(driver.current_url)

    sys.exit(1)

    

bnet = battlenet.BattleNet(challenge_handler)

messages = []
friends = []
account = {}


class BattleNetThread(threading.Thread):
    def __init__(self, loop_time = 1.0/60):
        self.timeout = loop_time
        super(BattleNetThread, self).__init__()


    def run(self):
        bnet.notification_api.notification_listener_service.add_whisper_listener(self.on_whisper)
        bnet.friends_api.friends_service.add_subscribe_friends_listener(self.on_friend_subscribe)

        bnet.connect("us.actual.battle.net", 1119)
        while True:
            bnet.handle_packets()

    def on_friend_subscribe(self, data):
        with open("test.log", "w") as f:
            f.write(data)

    def on_whisper(self, sender_battle_tag, message, sender_id):  
        messages.append({"username": sender_battle_tag, "message": message, "id": sender_id})
        with open("data/messages.json", "w") as f:
            f.write(json.dumps(messages))
        bnet.notification_api.notification_service.send_notification(sender_id, message)


BattleNetThread().start()