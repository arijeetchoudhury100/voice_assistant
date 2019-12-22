import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import os
import sys
import smtplib
import wikipedia as wk
import requests
import json
from random import randint
from geopy.geocoders import Nominatim

def text_to_speech(my_audio):
    '''
    this function converts the text(string) to audio
    '''
    engine.say(my_audio)
    engine.runAndWait()

def speech_to_text():
    '''
    this function listens for user commands and converts them into a string
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #wait for 1second after inactivity to declare the command as complete
        r.pause_threshold = 1
        print('Waiting for command...')
        audio = r.listen(source)
    try:
        print('Recognising...')
        command = r.recognize_google(audio,language='en-in')
        print('Command:',command)
    except:
        print('try again!!')
        return "None"
    return command

def showWeatherDetails(city):
    '''
    this function returns the weather summary, temperature and humidity for the specified city
    '''
    geolocator = Nominatim(user_agent='my-user')
    api_key = '2b9430c0adef2115645fefaef5562800'
    url = 'https://api.darksky.net/forecast/' + api_key +'/'
    
    #get latitude and longitude for the city using geopy
    lat = lon = 0.0
    while True:
        try:
            location = geolocator.geocode(city)
            lat = location.latitude
            lon = location.longitude
            #print(lat,lon)
            break
        except:
            print('timed out')
    url = url + str(lat) + ',' + str(lon)

    #get the weather details using darksky APi
    response = requests.get(url)
    x = response.json()
    data = x['currently']
    return data['summary'],data['temperature'],data['humidity']

def displayTasks():
    tasks = ['1. Open Google','2. Open Youtube','3. Open Browser','4. Send an email','5. Run Sublime Text','6. <topic> wikipedia',
            '7. Play a song','8. Open visual studio code','9. Open command prompt','10. Poweroff/Shutdown',
            '11. Log out','12. Show weather details','**say "quit" to exit**']
    for task in tasks:
        print(task)

#create pyttsx3 object
engine = pyttsx3.init('sapi5')

#set the voice(male/female) and voice rate
my_voices = engine.getProperty('voices')
engine.setProperty('rate',200)
arguments = sys.argv
if len(arguments) < 2:
    print('Usage: python',arguments[0],'<male/female>')
    sys.exit()
if(arguments[1] == 'male'):
    engine.setProperty('voice',my_voices[0].id)
elif(arguments[1] == 'female'):
    engine.setProperty('voice',my_voices[1].id)

#start the voice assistant
text_to_speech('Welcome Sir, how may I help you? Here are the commands I support!')
displayTasks()
while(True):
    command = speech_to_text().lower()
    if 'text' in command:
        text_to_speech('opening sublime text...')
        os.system('C:\\"Program Files"\\"Sublime Text 3"\\sublime_text')
    elif 'open browser' in command:
        text_to_speech('opening mozilla firefox')
        os.system('C:\\"Program Files"\\"Mozilla Firefox"\\firefox')
    elif 'open google' in command:
        text_to_speech('opening google')
        wb.open('https://www.google.com')
    elif 'open youtube' in command:
        text_to_speech('opening youtube')
        wb.open('https://www.youtube.com')
    elif 'send mail' in  command:
        #create an SMTP object
        s = smtplib.SMTP('smtp.gmail.com',587)
        #start secure connection
        s.starttls()
        try:
            text_to_speech('please enter your gmail id and password')
            my_id = input('Enter your gmail id')
            my_pass = input('Enter your password')
            #login to gmail account
            s.login(my_id,my_pass)
            text_to_speech('Login successful!')
            print('logged in')
            
            text_to_speech('whom do u want to send the email?')
            to_id = input('Enter destination email: ')
            text_to_speech('Enter your message')
            message = input("Enter message: ")
            #send mail
            s.sendmail(my_id,to_id,msg=message)
            text_to_speech('message has been sent')
        except Exception as e:
            text_to_speech('cannot send message')
            print(e)
        s.quit()
    elif 'wikipedia' in command:
        to_search = command.replace('wikipedia','')
        summary = wk.summary(to_search,sentences=3)
        text_to_speech(summary)
    elif 'song' in command:
        music = 'G:\\music\\'
        music_list = os.listdir(music)
        #print(music_list)
        to_play = music_list[randint(0,len(music_list)-1)]
        selected = to_play.replace('.mp3','')
        text_to_speech('playing '+selected)
        os.startfile(music+to_play)
    elif 'code' in command:
        try:
            text_to_speech('opening visual studio code')
            os.system('start code')
        except:
            text_to_speech('Path to code not added')
    elif 'weather' in command:
        text_to_speech('please specify a city')
        city = input('Enter city: ')
        text_to_speech('please wait while I fetch the weather details')
        summ,temp,hum = showWeatherDetails(city)
        say = 'The weather is ' + str(summ) + ', temperature is ' + str(temp) + ' farenheits and humidity is ' + str(float(hum)*100) + ' percent' 
        text_to_speech(say)
        print(say)
    elif 'command' in command:
        text_to_speech('opening command prompt')
        os.system('start cmd')
    elif 'shut' in command or 'power' in command:
        text_to_speech('shutting down the system..')
        print('shutting down..')
        os.system('shutdowwn /s')
    elif 'log' in command:
        text_to_speech('logging out..')
        print('logginng out')
        os.system('shutdown /l')
    elif 'quit' in command:
        text_to_speech('hope you liked me, see you soon')
        break