import speech_recognition as sr
import os
import re
import wikipedia
import webbrowser
import sys
import requests
import subprocess
from pyowm import OWM
from bs4 import BeautifulSoup
from time import strftime
from requests_xml import XMLSession

def logicResponse(audio):
    print (audio)
    if audio:
        for line in audio.splitlines():
            os.system(line)

def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("You said : " + command + "\n")
    except sr.UnknownValueError:
        print(".....")
        command = myCommand()
    return command

def assistant(command):

    if 'open' in command and 'moodle' not in command:
        regex = re.search('open (.+)', command)
        if regex:
            domain = regex.group(1)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            logicResponse("Opening " + domain)
        else:
            pass

    elif 'open moodle' in command:
        webbrowser.open('https://moodle.iiit.ac.in/my/')
        logicResponse("Opening moodle")

    elif 'hello' in command or 'hey' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            logicResponse('Hello Sudhansh. Good morning')
        elif 12 <= day_time < 18:
            logicResponse('Hello Sudhansh. Good afternoon')
        else:
            logicResponse('Hello Sudhansh. Good evening')

    elif 'shutdown' in command or 'bye' in command:
        logicResponse('Bye bye. Have a nice day')
        sys.exit()

    elif 'joke' in command:
        try:
            url = requests.get("https://icanhazdadjoke.com")
            html = url.text
            url.close()
            soup = BeautifulSoup(html, 'html.parser')
            joke = soup.find("p", {'class': 'subtitle'}).string.strip()
            logicResponse(joke)
        except Exception as e:
            print("Oops! Out of jokes!")
    
    elif 'news' in command or "headlines" in command:
        try:
            news_url="https://news.google.com/news/rss"
            session = XMLSession()
            r = session.get(news_url)
            news_list = r.xml.xpath("//item/title")
            for news in news_list[:15]:
                print(news.text)
        except Exception as e:
                print(e)

    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            logicResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        logicResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                print(wikipedia.summary(reg_ex.group(1)))
        except Exception as e:
                logicResponse(e)

    elif 'launch' in command:
        regex = re.search('launch (.*)', command)
        if regex:
            appname = regex.group(1)
            app = appname + '.app'
            subprocess.Popen(["open","/Applications/"+app], stdout=subprocess.PIPE)
            logicResponse("Launching " + appname)
        else:
            logicResponse("App not found")


logicResponse("Hi! I'm Logic, your personal assistant.")
while (True):
    assistant(myCommand())