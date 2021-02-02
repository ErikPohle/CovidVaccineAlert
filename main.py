import urllib
import urllib.request,urllib.parse,urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime, time
from playsound import playsound
import schedule
import time
import ssl
import threading

def timestamp():
    ct = datetime.datetime.now()
    return "[{}, {}]".format(ct, ct.timestamp())

def alert(url):
    print(timestamp() + "OPENING FOUND FOR " + url + "\n")
    f.write(timestamp() + "OPENING FOUND FOR " + url + "\n")
    playsound('./sound/alert.mp3')

def go(url):
    print(timestamp() + "Beginning web scraping...\n")
    f.write(timestamp() + "Beginning web scraping...\n")
    has_opening = False
    print(timestamp() + "Opening URL.\n")
    f.write(timestamp() + "Opening URL.\n")
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    print(timestamp() + "Searching for classes named SUGsignups.\n")
    f.write(timestamp() + "Searching for classes named SUGsignups.\n")
    info = soup.find_all(class_="SUGsignups")
    print(timestamp() + "Stripping and analyzing HTML.\n")
    f.write(timestamp() + "Stripping and analyzing HTML.\n")

    for i in range(0, len(info), 1):
        #f.write(timestamp() + info[i].text.strip() + "\n")
        #print(info[i].text.strip())
        if "Already filled" not in info[i].text:
            f.write(timestamp() + info[i].text.strip() + "\n")
            has_opening = True

    if has_opening:
        print(timestamp() + "Opening found!\n")
        f.write(timestamp() + "Opening found!\n")
        alert(url)
    else:
        print(timestamp() + "No openings found... retrying soon.\n")
        f.write(timestamp() + "No openings found!\n")

def provisionWork():
    threads = []
    t1 = threading.Thread(target=go, args=["https://www.signupgenius.com/index.cfm?go=s.signup&urlid=overlake&view=standard"])
    t2 = threading.Thread(target=go, args=["https://www.signupgenius.com/go/10c0c4caca92aa5fbc07-march"])
    t3 = threading.Thread(target=go, args=["https://www.signupgenius.com/go/8050944a4af2ea4fb6-march2"])
    t4 = threading.Thread(target=go, args=["https://www.signupgenius.com/go/8050944a4af2ea4fb6-march3"])
    t5 = threading.Thread(target=go, args=["https://www.signupgenius.com/go/8050944a4af2ea4fb6-march4"])
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)
    threads.append(t5)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def main():
    global f
    f = open("log.txt", "w")
    print("Hello! Welcome to the covid vaccine appointment alerter!")
    print("If this is your first time running this program, we advise you test that the alert sound plays for you.")
    print("You can test it by clicking the 'T' key.")
    print("Otherwise, if you want to use the alert service, simply click 'R' and the service will run in the background!")
    print("Once an appointment opening is found an airhorn alert will play to alert you to the opening.")
    user_choice = input("Type 'R' to run the service or type 'T' to test the alert sound. If you want to quit, type 'Q'. \n(R/T/Q) ")
    while(user_choice.upper() != "Q"):
        if user_choice.upper() == "T":
            playsound('./sound/alert.mp3')

        elif user_choice.upper() == "R":
            schedule.every(15).seconds.do(provisionWork)
            while True:
                print(timestamp() + "Preparing service...\n")
                f.write(timestamp() + "Preparing service...\n")
                schedule.run_pending()
                time.sleep(1)
        else:
            print("Input not recognized. Please try again.")
            f.write("Input not recognized. Please try again.\n")

        user_choice = input("Type 'R' to run the service or type 'T' to test the alert sound. If you want to quit, type 'Q'. \n(R/T/Q) ")
        
    f.close()




           
if __name__ == "__main__":
    main()