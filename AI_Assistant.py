from datetime import datetime
import json
import os
import random
from getpass import getuser
from time import sleep
from webbrowser import open as webopen

from pytube import YouTube
from ipregistry import IpregistryClient
import speech_recognition as sr
import wikipedia
from cv2 import QRCodeDetector, VideoCapture
from pyjokes import get_joke
from pyttsx3 import init
from qrcode import make
from requests import get
from speedtest import Speedtest
from newsapi import NewsApiClient

#Text To Speech

engine = init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
file_obj = open("config.json", "r")
json_file = json.load(file_obj)
file_obj.close()
name = json_file["assistant_name"]
user_name = json_file["user_name"]
news_api_key = json_file["news_api_key"]
engine.setProperty('voice',voices[json_file["voice_id"]].id)
engine.setProperty("rate", json_file["sound_rate"])

def speak(audio):  #here audio is var which contain text
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.now().hour)

    rest_of_wish = " sir i am virtual assistent "+name
    if hour >= 0 and hour<12:
        speak("good morning"+rest_of_wish)
    elif hour>=12 and hour<18:
        speak("good afternoon"+rest_of_wish) 
    else:
        speak("good evening"+rest_of_wish)
    speak("How may I help you?")  

#now convert audio to text
# 
def takecom():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening....")
        audio = r.listen(source)
    try:
        print("Recognising.")
        text = r.recognize_google(audio, language='en-in')
        print(text)
    except Exception as E:                #For Error handling
        print(E) 
        return "none"
    return text

#for main function                               
if __name__ == "__main__":
    try:
        wish()

        while True:
            query = takecom().lower()

            if name.lower() in query or 'aleksa' in query or "bye" in query:

                if "wikipedia" in query:
                    counter = False
                    speak("searching details....Please Wait")
                    query.replace("wikipedia","")
                    results = wikipedia.summary(query,sentences=2)
                    print(results)
                    speak(results)

                elif 'download youtube video' in query or 'download yt video' in query:
                    counter=False
                    speak("Type the link below")
                    link = input("Type the link: ")

                    yt = YouTube(link)
                    speak("Downloading "+yt.title+". Please Wait")
                    mp4files = yt.streams.get_highest_resolution()

                    mp4files.download(os.path.join(os.path.expanduser("~"), "Downloads"))
                    speak("Video has been downloaded")

                elif 'open google drive' in query:
                    counter=False
                    webopen("https://drive.google.com")
                    speak("opening google drive")

                elif 'open bing' in query or 'open microsoft bing' in query:
                    counter=False
                    webopen("https://bing.com")
                    speak("opening bing")

                elif 'google classroom' in query or 'open classroom' in query:
                    counter = False
                    webopen("https://classroom.google.com")
                    speak("opening Google Classroom")

                elif 'open twitter' in query or 'opwn twitter web' in query:
                    counter = False
                    webopen("https://www.twitter.com")
                    speak("opening twitter")

                elif 'where am i' in query:
                    counter=False
                    client = IpregistryClient("tryout")  
                    ipInfo = client.lookup() 
                    res = "You are in "+ipInfo.location["city"]
                    print(res)
                    speak(res)

                elif "what is today's news" in query or "what's today's news" in query or "what is the news" in query or "tell me the news" in query or "tell me today's news" in query:
                    counter=False
                    newsapi = NewsApiClient(api_key=news_api_key)
                    top_headlines = newsapi.get_top_headlines(country='in')
                    if top_headlines["status"] == "ok":
                        no = False
                        per = 5
                        i = 0
                        for article in top_headlines["articles"]:
                            try:
                                print(article["title"]+". "+article["description"])
                                speak(article["title"]+". "+article["description"])
                                if i == per:
                                    speak("Would you like to hear more?")
                                    while True:
                                        query = takecom().lower()
                                        if 'yes' in query:
                                            speak("Ok")
                                            per +=5
                                            break
                                        elif 'no' in query:
                                            speak("Ok")
                                            no = True
                                            break
                                        else:
                                            speak("Please say yes or no")
                                    if no == True:
                                        break
                                i = i + 1
                            except:
                                break

                elif 'what is the time' in query:
                    counter=False
                    res = "It's "+datetime.now().strftime("%I %M %p")
                    speak(res)
                    speak(res)

                elif 'what is google' in query:
                    counter=False
                    print("Google LLC is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware.")
                    speak("Google LLC is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, a search engine, cloud computing, software, and hardware.")

                elif 'what is microsoft' in query:
                    counter=False
                    print("Microsoft Corporation is an American multinational technology corporation which produces computer software, consumer electronics, personal computers, and related services.")
                    speak("Microsoft Corporation is an American multinational technology corporation which produces computer software, consumer electronics, personal computers, and related services.")

                elif 'what is github' in query:
                    counter=False
                    print("GitHub, Inc. is a provider of Internet hosting for software development and version control using Git. It offers the distributed version control and source code management functionality of Git, plus its own features.")
                    speak("GitHub, Inc. is a provider of Internet hosting for software development and version control using Git. It offers the distributed version control and source code management functionality of Git, plus its own features.")

                elif 'what is Delhi' in query or 'what is delhi' in query:
                    counter=False
                    print("Delhi, officially the National Capital Territory (NCT) of Delhi, is a city and a union territory of India containing New Delhi, the capital of India. Straddling the Yamuna river, but primarily its western or right bank, Delhi shares borders with the state of Uttar Pradesh in the east and with the state of Haryana in the remaining directions. ")
                    speak("Delhi, officially the National Capital Territory (NCT) of Delhi, is a city and a union territory of India containing New Delhi, the capital of India. Straddling the Yamuna river, but primarily its western or right bank, Delhi shares borders with the state of Uttar Pradesh in the east and with the state of Haryana in the remaining directions. ")

                elif 'open gmail' in query:
                    counter = False
                    webopen("https://mail.google.com")
                    speak("opening google mail")

                elif 'open heroku' in query:
                    counter=False
                    speak("opening heroku")
                    webopen("https://www.heroku.com")

                elif 'open stackoverflow' in query or 'open coding community' in query or 'open stack overflow' in query:
                    counter=False
                    webopen("https://www.stackoverflow.com")
                    speak("Opening Stackoverflow")

                elif 'open google meet' in query or 'open google mi' in query or 'open google me' in query:
                    counter=False
                    webopen("https://meet.google.com")
                    speak("Opening Google Meet")

                elif 'open spotify' in query:
                    counter=False
                    webopen("https://open.spotify.com/")
                    speak("Opening spotify")

                elif 'open microsoft news' in query or 'microsoft news' in query or 'windows news' in query:
                    counter=False
                    webopen("https://microsoftnews.msn.com/")
                    speak("opening microsoft news")

                elif 'open google news' in query or 'open news' in query or 'google news' in query:
                    counter=False
                    webopen("https://news.google.com")
                    speak("opening google news")

                elif 'open youtube' in query or "open video online" in query:
                    counter = False
                    webopen("www.youtube.com")
                    speak("opening youtube")

                elif 'open mitraelectronics' in query:
                    webopen("https://mitraelectronics.herokuapp.com")
                    speak("opening Mitra Electronics website")

                elif 'send message to' in query or 'send message to' in query:
                    person = query.replace('send message to', '')
                    speak('What message should I send to' + person)
                    parsed_message = takecom()
                    parsed_message.replace('the message is', '')
                    speak("What is his phone number")
                    phone_no = input("Enter phone number with country code")
                    get('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + parsed_message)

                elif 'check internet speed' in query or 'internet speed' in query or 'check computer internet speed' in query:
                    counter = False
                    speed = Speedtest()
                    speak("Checking internet speed. Please wait")
                    res_ = "Your download speed is " + str(format((speed.download()/ 1024 / 1024), ".3f")) + " megabits per second and your upload speed is " + str(format((speed.upload()/1024/1024), ".3f")) + " megabits per second"
                    print(res_)
                    speak(res_)

                elif 'open github' in query:
                    counter = False
                    webopen("https://www.github.com")
                    speak("opening github")

                elif 'open google earth' in query or 'open earth' in query:
                    counter = False
                    webopen("https://earth.google.com")
                    speak("opening google earth")

                elif 'open google photos' in query:
                    counter = False
                    webopen("https://photos.google.com")
                    speak("opening google earth")

                elif 'open bitbucket' in query:
                    counter = False
                    webopen("https://www.bitbucket.com")
                    speak("opening bitbucket")

                elif 'open gitlab' in query:
                    counter = False
                    webopen("https://www.gitlab.com")
                    speak("opening gitlub")

                elif 'open facebook' in query or 'open fb' in query:
                    counter = False
                    webopen("https://www.facebook.com")
                    speak("opening facebook") 

                elif 'open instagram' in query or 'open insta' in query:
                    counter = False
                    webopen("https://www.instagram.com")
                    speak("opening instagram")
                    
                elif 'open yahoo' in query:
                    counter = False
                    webopen("https://www.yahoo.com")
                    speak("opening yahoo") 
                    
                elif 'open snapdeal' in query:
                    counter = False
                    webopen("https://www.snapdeal.com") 
                    speak("opening snapdeal")  

                elif 'open indian shop' in query or 'open amazon.in' in query or 'open amazon india' in query:
                    counter = False
                    webopen("https://www.amazon.in")
                    speak("opening amazon.in") 
                    
                elif 'open amazon' in query or 'shop online' in query:
                    counter = False
                    webopen("https://www.amazon.com")
                    speak("opening amazon.com")

                elif 'open flipkart' in query:
                    counter = False
                    webopen("https://www.flipkart.com")
                    speak("opening flipkart")   
                elif 'open ebay' in query:
                    counter = False
                    webopen("https://www.ebay.com")
                    speak("opening ebay")

                elif 'download google chrome' in query or 'install google chrome' in query or 'download chrome' in query or 'install chrome' in query:
                    counter = False
                    try:
                        speak("Downloading Google Chrome installer")
                        r = get("https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7B28F63426-8F8C-D6D5-6709-B36D653ACF14%7D%26lang%3Den-GB%26browser%3D4%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe", allow_redirects=True)
                        open(f"C:\\Users\\{getuser()}\\Downloads\\ChromeSetup.exe", 'wb').write(r.content)
                        speak("Downloaded Google Chrome Installer Sucessfully! Opening downloads folder")
                        os.startfile(f"C:\\Users\\{getuser()}\\Downloads")
                    except:
                        speak("No Internet, couldn't download Google Chrome")

                elif "open google chrome" in query or "open chrome" in query or "chrome" in query:
                    counter=False
                    try:
                        if os.path.exists("C:\Program Files\Google\Chrome\Application\chrome.exe") == True:
                            os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
                            speak("Opening Google Chrome")

                        else:
                            speak("Google Chrome is not installed. If you want to download Google Chrome, say download Google Chrome")

                    except:
                        speak("An error occured. Propably Google Chrome is not installed. If you want to download Google Chrome, say download Google Chrome")

                elif "download whatsapp" in query or "install whatsapp" in query or "install whatsapp desktop" in query or "download whatsapp desktop" in query:
                    counter=False
                    try:
                        speak("Downloading Whatsapp Desktop")
                        r = get("https://web.whatsapp.com/desktop/windows/release/x64/WhatsAppSetup.exe", allow_redirects=True)
                        open(f"C:\\Users\\{getuser()}\\Downloads\\WhatsAppSetup.exe", 'wb').write(r.content)
                        speak("Downloaded Whatsapp Desktop Sucessfully! Opening downloads folder")
                        os.startfile(f"C:\\Users\\{getuser()}\\Downloads")
                    except:
                        speak("No Internet, couldn't download Whatsapp desktop")

                elif "install zoom client" in query or "download zoom client" in query or "install zoom" in query or "download zoom" in query:
                    counter=False
                    try:
                        speak("Downloading Zoom Client")
                        r = get("https://zoom.us/client/latest/ZoomInstaller.exe", allow_redirects=True)
                        open(f"C:\\Users\\{getuser()}\\Downloads\\ZoomInstaller.exe", 'wb').write(r.content)
                        speak("Downloaded Zoom client Sucessfully! Opening downloads folder")
                        os.startfile(f"C:\\Users\\{getuser()}\\Downloads")
                    except:
                        speak("No Internet, couldn't download Zoom client")

                elif 'open zoom web' in query:
                    counter = False
                    webopen("https://us04web.zoom.us")
                    speak("opening zoom web")

                elif 'install visual studio code' in query or 'install vs code' in query or 'download vs code' in query or 'download visual studio code' in query:
                    counter=False
                    try:
                        speak("Downloading Visual Studio Code")
                        r = get("https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user", allow_redirects=True)
                        open(f"C:\\Users\\{getuser()}\\Downloads\\vs-code-win32-x64-user.exe", 'wb').write(r.content)
                        speak("Downloaded Visual Studio Code Sucessfully! Opening downloads folder")
                        os.startfile(f"C:\\Users\\{getuser()}\\Downloads")
                    except:
                        speak("No Internet, couldn't download Visual Studio Code")

                elif 'open visual studio code' in query or 'open vs code' in query or 'open vsc' in query or 'open code editor' in query or 'open default code' in query:
                    counter=False
                    try:
                        if os.path.exists(f"C:\\Users\\{getuser()}\\AppData\\Local\\Programs\\Microsoft VS Code") == True:
                            os.startfile(f"C:\\Users\\{getuser()}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
                            speak("Opening Visual Studio Code")

                        else:
                            speak("Visual Studio Code is not installed. If you want to download Visual Studio Code, say download Visual Studio Code")

                    except:
                        speak("An error occured. Propably Visual Studio Code is not installed. If you want to download Visual Studio Code, say download Visual Studio Code")

                elif 'open zoom desktop' in query or 'open zoom client' in query or "open zoom" in query:
                    counter=False
                    try:
                        if os.path.exists(f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Zoom\\bin"):
                            os.startfile(f"C:\\Users\\{getuser()}\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
                            speak("Opening Zoom")
                        else:
                            speak("Zoom Client app is not installed. If you want to open zoom in the browser, say open zoom web")

                    except:
                        speak("An error occured. Propably Zoom Client is not installed. If you want to open zoom in the browser, say open zoom web")

                elif 'open whatsapp desktop' in query:
                    counter=False
                    try:
                        if os.path.exists(f"C:\\Users\\{getuser()}\\AppData\\Local\\WhatsApp"):
                            os.startfile(f"C:\\Users\\{getuser()}\\AppData\\Local\\WhatsApp\\WhatsApp.exe")
                            speak("Opening Whatsapp Desktop")

                        else:
                            speak("Whatsapp Desktop app is not installed. If you want to open whatsapp web in the browser, say open whatsapp web")

                    except:
                        speak("An error occured. Propably Whatsapp Desktop app is not installed. If you want to open whatsapp web in the browser, say open whatsapp web")

                elif 'open google' in query:
                    counter = False
                    webopen("https://www.google.com")
                    speak("opening google")

                elif 'open whatsapp web' in query:
                    counter=False
                    webopen("https://web.whatsapp.com")
                    speak("Opening Whatsapp Web")

                elif 'open whatsapp' in query:
                    speak("Opening Whatsapp Web, if you want to open whatsapp desktop, say open whatsapp desktop")
                    webopen("https://web.whatsapp.com")

                elif 'create qr code' in query:
                    counter = False
                    print("What is the link of the website that you want to create qr code for")
                    speak("What is the link of the website that you want to create qr code for")
                    link = takecom()
                    if link == 'none':
                        break
                    else:
                        qrcodeimg = make(link)
                        qrcodeimg.save(f'C:\\Users\\{getuser()}\\Downloads\\qr.jpg')
                        print("QR code created sucessfully. File name is qr.jpg")
                        speak("QR code created sucessfully. File name is qr.jpg")

                elif "tell me a joke" in query or "i want a joke" in query or "tell me a funny joke" in query or "i want a funny joke" in query:
                    counter = False
                    joke_temp = get_joke()
                    print(joke_temp)
                    speak(joke_temp.lower())
                    counter = True
                
                elif 'open file explorer' in query or 'open file manager' in query or 'open this pc' in query:
                    counter = False
                    os.system('explorer')
                    speak("File Explorer opened sucessfully")

                elif 'open command prompt' in query or 'open cmd' in query:
                    counter = False
                    os.startfile("C:\Windows\system32\cmd.exe")
                    speak("Cmd opened sucessfully")

                elif "that was a funny one" in query or "that was a funny joke" in query:
                    if counter == True:
                        print("Would you like another one?")
                        speak("would you like another one?")
                        yesorno = takecom().lower()
                        if "yes" in yesorno or "yeah" in yesorno:
                            print("Ok. here's another one")
                            speak("ok. here's another one")
                            joke_temp = get_joke()
                            print(joke_temp)
                            speak(joke_temp.lower())
                            counter = True
                        else:
                            print("Ok")
                            speak("Ok")
                            counter = False

                    else:
                        print("Would you like a joke?")
                        speak("would you like a joke?")
                        yesorno = takecom().lower()
                        if "yes" in yesorno or "yeah" in yesorno:
                            print("Ok. here's a joke")
                            speak("ok. here's a joke")
                            joke_temp = get_joke()
                            print(joke_temp)
                            speak(joke_temp.lower())
                            counter = True
                        else:
                            print("Ok")
                            speak("Ok")
                            counter = False


                elif 'music from pc' in query or "music" in query:
                    counter = False
                    speak("ok i am playing music. a quick note , if you want me to play music, put all your music in the music folder and just say, play music from pc")
                    music_dir = rf'C:\Users\{getuser()}\Music'
                    musics = os.listdir(music_dir)
                    if musics[0] == 'desktop.ini':
                        musics.remove(0)
                    print(musics)
                    os.startfile(os.path.join(music_dir,musics[random.randint(0, len(musics))]))
                elif 'video from pc' in query or "video" in query:
                    counter = False
                    speak("ok i am playing videos. a quick note , if you want me to play videos, put all your videos in the videos folder and just say, play video from pc")
                    video_dir = rf"C:\\Users\\{getuser()}\\Videos"
                    videos = os.listdir(video_dir)
                    if videos[0] == 'desktop.ini':
                        videos.remove(0)
                    os.startfile(os.path.join(video_dir,videos[random.randint(0, len(videos))]))  
                elif 'good bye' in query or 'goodbye' in query:
                    counter = False
                    speak("good bye")
                    exit()
                elif "shutdown" in query:
                    counter = False
                    speak("Shutting down pc in 5 seconds")
                    sleep(5)
                    os.system('shutdown -s') 

                elif 'play song in spotify' in query:
                    counter=False
                    webopen("https://open.spotify.com/track/6sJz0KMqV4iaaxjlRr9dp3?si=46c504d441ff4855")
                    speak("Playing egiye de")

                elif "what\'s up" in query or 'how are you' in query:
                    counter = False
                    stMsgs = ['I am fine!','i am okay ! How are you']
                    ans_q = random.choice(stMsgs)
                    speak(ans_q)  
                    ans_take_from_user_how_are_you = takecom()
                    if 'fine' in ans_take_from_user_how_are_you or 'happy' in ans_take_from_user_how_are_you or 'ok' in ans_take_from_user_how_are_you:
                        speak('okey..')  
                    elif 'not' in ans_take_from_user_how_are_you or 'sad' in ans_take_from_user_how_are_you or 'upset' in ans_take_from_user_how_are_you:
                        speak('oh sorry..')  

                elif 'make you' in query or 'created you' in query or 'develop you' in query:
                    counter = False
                    ans_m = "Ishan Mitra Created me ! I give a  Lot of Thanks to Him "
                    print(ans_m)
                    speak(ans_m)

                elif "who are you" in query or "about you" in query or "your details" in query:
                    counter = False
                    about = "I am "+name+" an A I based computer program but I can help you lot like a your close friend ! Try to give me simple commands, like playing music or video from your directory i also play video and song from web or online ! i can also entain you "
                    print(about)
                    speak(about)

                elif "hello" in query or "hi" in query or "hello "+name in query:
                    counter = False
                    hel = "Hello "+user_name+" ! How May i Help you.."
                    print(hel)
                    speak(hel)

                elif "is my name" in query or "will you call me" in query:
                    speak("Your name is "+user_name)

                elif 'read qrcode' in query or 'scan qrcode' in query or 'read qr code' in query or 'scan qr code' in query:
                    capture = VideoCapture(0)
                    read_qr = QRCodeDetector()
                    val, points, straight_qrcode = read_qr.detectAndDecode(capture.read())
                    capture.close()
                    speak(val)

                elif 'set alarm to' in query or 'start alarm to' in query:
                    speak("This feature is comming soon...")

                elif "your name" in query or "sweat name" in query:
                    counter = False
                    na_me = "Thanks for Asking my name is "+name  
                    print(na_me)
                    speak(na_me)
                elif "you feeling" in query:
                    counter = False
                    print("feeling Very good after meeting with you")
                    speak("feeling Very good after meeting with you") 
                elif query == 'none':
                    counter = False
                    continue 
                elif 'exit' in query or 'abort' in query or 'stop' in query or 'bye' in query or 'quit' in query :
                    counter = False
                    ex_exit = "Bye! Have a nice day!"
                    speak(ex_exit.lower())
                    exit()    
                elif 'ok' in query:
                    counter = False
                    speak("Good!!!")

                
                elif 'what is 2 + 2' in query or '2 + 2' in query or 'answer 2 + 2' in query:
                    speak("4")
                elif 'what is 1 + 1' in query or '1 + 1' in query or 'answer 1 + 1' in query:
                    speak("2")

                elif 'how to go on a tour in kashmir' in query:
                    speak(""" Question. What is the best time to visit Kashmir?.
Answer. Before considering one of the Kashmir packages, you need to know in detail about the seasons of Kashmir and which more favourable for travel. Otherwise a year-round destination, it would be ideal to travel to Kashmir in the summer to fall months between March and October. You can see its blossoming gardens, hear the bird song, take in sweeping views of the alpine meadows and simply watch Srinagar’s Dal Lake hustle back to life. Visit Pahalgam between April and November for some rafting and horse-riding. For golf, come between April and November. But if snow is your thing and you care for some snowboarding and skiing, head to Gulmarg between December and first half of March.

Question. Are there enough ATMs all across Kashmir?.
Answer. While you finalise one of the Kashmir tour packages, you need to be aware of how much cash you should be carrying and the number of ATMs at your disposal. The ATM network of Kashmir is quite vast, and you shouldn’t have difficulty spotting an ATM while travelling. However, it makes sense to always carry sufficient - not copious - cash at all times while travelling, because many an ATM could be out of order or have run out of cash. Srinagar has plenty of ATMs and withdrawing cash is not at all an issue, but it is not quite the same with Pahalgam and Gulmarg. There are fewer ATMs in these areas, so best to carry enough cash on you when venturing beyond Srinagar.

Question. What is the local mode of transport in Kashmir?.
Answer. Though all the Kashmir travel packages you browse through will provide for your transportation, it is imperative to know how you can commute locally. Though the significant modes of transport in Kashmir are taxis and mini bus, you will also come across ample auto-rickshaws and luxury coaches. You can ride aboard a Jammu & Kashmir Tourism Development Corporation bus or a Jammu & Kashmir State Road Transport Corporation bus that have a fleet of luxury coaches as well for local sightseeing within Kashmir. Else hire a tourist taxi that takes you to the local sights and also for trips outside Srinagar. The most preferred local transport is the mini bus which operates through the city and also in the suburban areas. They travel on a pre-fixed route. For shorter distances, rely on nothing other than the ubiquitous auto-rickshaws.

Question. Are there direct flights from New Delhi to Kashmir?.
Answer. There are direct flights from New Delhi’s Indira Gandhi International Airport to Sheikh ul-Alam International Airport also called the Srinagar Airport. Significant carriers like SpiceJet, AirAsia, GoAir, Vistara, IndiGo, Air India operate on this route, with the journey time of a non-stop New Delhi to Srinagar flight being approximately 1.5 hours. A well-served route, flights are available at a great frequency through the day.

Question. How can I go to Srinagar by train?.
Answer. There are no direct trains to Srinagar from any of the major cities. If you really wish to travel by train only, then you can take a train till Jammu or Udhampur and travel from there to Srinagar by the local DEMU train or by bus or taxi. However, the most convenient way to travel to Srinagar is by air.

Question. Will there be snow in May in Kashmir?.
Answer. If you are visiting Kashmir in May, you will not find snow in the lower reaches. However, you could still find snow in higher altitudes such as Pahalgam or Gulmarg. Otherwise the temperature will be pleasant in the lower reaches too.

Question. What should I buy in Jammu and Kashmir?
Answer. Some of the best things to buy while you are on a Kashmir tour package are Kashmiri dry fruits, saffron, honey, and salt tea. In addition, you can buy locally produced woollen textile products like shawls, stoles, ponchos etc. The traditional Kashmiri embroidery is famous across the world and you can buy embroidered apparel as well from Kashmir. Some high-quality souvenirs to bring back from Jammu Kashmir include walnut wood products, silver ware, copper and brass utensils and more.

Question. When does the tulip festival in Kashmir take place?.
Answer. The Indira Gandhi Memorial Tulip Garden in Srinagar hosts the tulip festival every year in the spring season - in April - when you can see an array of tulips in wondrous colours bloom to form an extremely photogenic landmark. Backed by the serene Dal Lake, the blossoming daffodils and hyacinths along with the iconic tulips draw in nature and photography lovers from all over the world to this gorgeous tulip garden in Srinagar.

Question. What are the things to do in Gulmarg?.
Answer. Outside of taking in the splendid natural setting of Gulmarg with its mountains and green valleys, you are recommended a few other activities such as a gondola ride, trekking to Alpather Lake from the Gondola Phase 2 station. Gulmarg is filled with trekking routes but the most popular of them is the trek to Alpather Lake. In the winter months, skiing among other snow-activities like snowboarding are in full swing. However, to sum it up, the activities you cannot miss in Gulmarg other than the gondola ride and Alpather Lake trek include Apharwat Peak, Gulmarg golf course, Maharani temple, St. Mary’s Church, Maharaja Palace, Strawberry Valley, Children’s Park, Khilanmarg, Ningle Nallah and Ferozpur Nallah.

Question. What are the places I can visit in Kashmir?.
Answer. Your Kashmir holiday should include a visit to Srinagar, Pahalgam, Gulmarg, Sonamarg, Anantnag, Sonmarg, Awantipora, Aru Valley, Dachigam National Park, Harwan among others. A typical itinerary for Kashmir would be made up of stay in a houseboat on Dal Lake, a night in Gulmarg, a night in Pahalgam, about three nights in Srinagar and a day trip to Sonamarg.""")

                else:
                        counter=False    
                        query = query.replace(name.lower(), '')
                        query = query.replace('aleksa', '')
                        print(query)
                        res = get("http://127.0.0.1:8000/?query="+query).text
                        print(res)
                        speak(res)
    except Exception as E:
        print(E)
