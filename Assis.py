import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
from datetime import date
import pywhatkit
import os
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import wikipedia
import pyautogui
from email.message import EmailMessage
from tkinter import *
from tkinter import filedialog
import imghdr


listener = sr.Recognizer()
listener_2 = sr.Recognizer()

engine = pyttsx3.init()

voices= engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)

rate= engine.getProperty("rate")
engine.setProperty("rate", 150)

path="C:\\Program Files\\chromedriver.exe"

next=False
countSong=0 

lst=[]      #.............list for save the path of the attachment to send to the 'send_email' function



def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.stop()


def get_command():
    with sr.Microphone() as source:  
        print("\nlistening...")
        listener.pause_threshold = 1
        
        voice= listener.listen(source, phrase_time_limit=5)
        #listener.dynamic_energy_threshold = False
        try:
            print("recognizing...")
            command= listener.recognize_google(voice, language='en-IN')
            print(command+'\n')
        
        except Exception:
            print("I didn't catch it\n")
            speak("I didn't catch it")
            return "None"
        return command

def date():
    date= datetime.datetime.now().strftime("%B %d, %Y")
    print(date)
    speak("It's" +date)

def music_offline(next,ftime):
    music_source= "D:\\MC\\The Official UK Top 40 Singles Chart (06.11.2020) Mp3 (320kbps) [Hunter]\\The Official UK Top 40 Singles Chart (06.11.2020)"
    songs= os.listdir(music_source)
    
    if ftime==True:
        print(songs)
    else:
        pass
    
    global countSong
    
    if next==True:
                       
        countSong+=1
        songFile= os.startfile(os.path.join(music_source, songs[countSong]))    
    else:
        
        songFile= os.startfile(os.path.join(music_source, songs[countSong]))
            
def find(command):
    findThing= command.replace("find","")

    time.sleep(1)
    pyautogui.click(171,747)
    time.sleep(2)
    pyautogui.write(findThing)  

    speak("Here is what I got for you")  

def go_to_fimsFolder():
    pyautogui.click(22,746)
    time.sleep(2)
    pyautogui.click(47,585)
    time.sleep(1)
    pyautogui.click(86,354)
    time.sleep(1)
    pyautogui.doubleClick(221,121)

    speak("Here is the list of your fims in your computer")

   
def interface():
    print("--------Please fill the blank fields and press the send button------------")
    speak("Please fill the blank fields and press the send button")
    
    root=Toplevel()        

    reciever_email = StringVar()
    subject = StringVar()
    attachment = StringVar()

    def get_textbox():
        text= txt.get('1.0', END)
        send_email(text)

    def file_explorer():
        filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a Attachment", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
        l4.configure(text= filename, font="arial 8")

        lst.append(filename) 

    def destroy():
        root.destroy()
        speak("You cancelled the process")

    def send_email(d):
        useremail= "tharindahp@gmail.com"
        password= "seethepositiveside"

        a = reciever_email.get()
        b = subject.get()
        c = attachment.get()

        msg = EmailMessage()
        msg['Subject'] = b
        msg['From'] = useremail
        msg['To'] = a
        msg.set_content(d)

        directory = f'{lst[0]}'
        print(f'\nPath of the attachment: {lst[0]}\n')
        
        if directory[-3:] == 'pdf':
            with open(directory , 'rb') as f:
                data = f.read()
                file_name = f.name 
                msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=file_name)

        else:
            with open(directory , 'rb') as f:
                data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name 
                msg.add_attachment(data, maintype='image', subtype=file_type , filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(useremail, password)
            smtp.send_message(msg)
        
        print("\nYour Email was successfully sent\n")
        speak("Your Email was successfully sent")
       
    
    root.title("Email")

    c=Canvas(root, bg="Gray", width=700, height=520)
    c.pack()

    l1=Label(c, text="Reciever's Email", font="arial 12 bold")
    l1.place(x=20, y=30)
    e1=Entry(c, width=55, font="arial 12", textvar= reciever_email)
    e1.place(x=180, y=30)

    l2=Label(c, text="Subject", font="arial 12 bold")
    l2.place(x=20, y=70)
    e2=Entry(c, width=55, font="arial 12", textvar= subject)
    e2.place(x=180, y=70)

    l3=Label(c, text="Attachment", font="arial 12 bold")
    l3.place(x=20, y=110)
    l4=Label(c, width=55)
    l4.place(x=180, y=110)
    btn=Button(c, text="Acces", font="arial 8 bold", width=8, command= file_explorer)
    btn.place(x=615, y=110)
    
    l5=Label(c, text="Message", font="arial 12 bold")
    l5.place(x=20, y=150)

    txt=Text(c, font="arial 12", width=73, height=16)
    txt.place(x=20, y=180)

    text= txt.get('1.0', END)
            
    btn1=Button(c, text="Send", font="arial 12 bold", width=8, command=get_textbox)
    btn1.place(x=220, y=480)

    btn2=Button(c, text="Exit", font="arial 12 bold", width=8, command=destroy)
    btn2.place(x=380, y=480)
    
    root.mainloop()



def download_song(songName):
    driver_1= webdriver.Chrome(path)
    driver_1.get("https://musicpleer24.com/") 
    search= driver_1.find_element_by_id("searchField")
    search.send_keys(songName)
    search.send_keys(Keys.RETURN)

    time.sleep(3)

    speak("Now you can choose the exact one and click on it")


def go_to_wikipedia():
    driver_2= webdriver.Chrome(path)
    driver_2.get("https://www.wikipedia.org/")
    driver_2.implicitly_wait(1)
    #time.sleep(1)

    try:

        with sr.Microphone() as source:
            
            speak("What do you want to search?")
            print("listening...")

            voice= listener.listen(source, phrase_time_limit=6)
            print("recognizing...")
            thing= listener_2.recognize_google(voice, language="en-IN")

            driver_2.maximize_window()

            search= driver_2.find_element_by_id("searchInput")
            search.send_keys(thing)
            search.send_keys(Keys.RETURN)

            speak("Here is what I found")

    except Exception:
        print("Couldn't hear it.")
        speak("Sorry, I couldn't hear it")

def go_to_google(command):
    editCommand= command.replace("search google", "")
    try:

        driver_3= webdriver.Chrome(path)
        driver_3.get("https://www.google.com/")

        search= driver_3.find_element_by_name("q")
        search.send_keys(editCommand)
        time.sleep(1)
        search.send_keys(Keys.RETURN)

        driver_3.maximize_window()
        
        time.sleep(1)
        speak("Here is what I found on google")

    except Exception:
        print("N")

def play_on_yt(command):
    song= command.replace("play", "")
    pywhatkit.playonyt(song)
    time.sleep(2)
    speak(f'Playing {song} on youtube')

def get_from_wikipedia(command):
    
    try:
        data= wikipedia.summary(command, sentences=2)
        speak("According to wikipedia")
        print(data)
        speak(data)
    except Exception:
        print("sorry, I couldn't get there")
        speak("sorry, I couldn't get there")

def time():
    time= datetime.datetime.now().strftime(' %I:%M %p ')
    print(time)
    speak(f'Current time is{time}')



def start():
    
    command= get_command().lower()

    if "open gmail" in command:
        webbrowser.open("mail.google.com/mail/u/0/#inbox")
        speak("Opening Gmail")

    elif "open youtube" in command:
        webbrowser.open("youtube.com")
        speak("Opening Youtube") 

    elif "search google" in command:
        go_to_google(command)
            
    elif "play music offline"in command:
        music_offline(next=False, ftime=True)   

    elif "next song" in command:
        music_offline(next=True, ftime=False)


    elif "the date" in command:
        date()

    elif "time" in command:
        time()
    
    elif "wikipedia"  in command:
        go_to_wikipedia()

    elif "find" in command:
        find(command)
    
    elif "play" in command:
        play_on_yt(command)
                     
    elif "download" and "song" in command:
        songName= command.replace("download the song", "")
        download_song(songName)

    elif "send an email" or "send a mail" or "send mail" in command:    
        interface()       

    elif "show"  and "films" in command:
        go_to_fimsFolder()
    
    elif "who is" or "what is" or "where is" or "tell me about" in command:
        get_from_wikipedia(command)              
    
    else:
        go_to_google(command)


