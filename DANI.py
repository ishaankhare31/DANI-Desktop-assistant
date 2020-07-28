import pyttsx3
import speech_recognition as sr
import wikipedia
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id) 
engine.setProperty('voice',voices[0].id) #id 0 is female voice in my system

# for speaking 
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    speak("hello Shikhar!!!, welcome to your project DANI. How can I help u today?")

def Describe():
    speak("I am project DANI, an AI Desktop manager cum web browser automater, made by Shikhar Gupta")
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.enery_threshold = 400
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')
        print("user said :" + query)

    except Exception as e:
        speak("Please say that again.")
        return "None"

    return query


def new_tab(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

def new_links(driver):
    query = query.replace("open", "")
    if 'youtube' in query:
        driver.get("https://youtube.com")

    elif 'google' in query:
        driver.get("https://google.com")

    elif 'stackoverflow' in query:
        driver.get("https://stackoverflow.com")

    elif 'facebook' in query:
        driver.get("https://facebook.com")

    elif 'gmail' in query:
        driver.get("https://gmail.com")

    elif 'rediffmail' in query:
        driver.get("https://rediffmail.com")

    else:
        speak("sorry!!! i dont have links to the site.")
        speak("Redirecting to google dot com")
        driver.get("https://google.com")

def Time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak("the time is " + strTime)


####main function 
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        #description for the project
        if 'describe' in query:
            Describe()

        #searching on wikipedia
        elif 'wikipedia' in query:
            speak("Searching wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia.." + results)
            print(results)

            
        #opening youtube and searching
        elif 'open youtube' in query:
            #webbrowser.get(chromedir).open("youtube.com")
            speak("Launching youtube")
            driver = webdriver.Chrome()
            driver.get("https://www.youtube.com")
            driver.maximize_window()
            while True:
                query = takeCommand().lower()
                if 'close' in query or 'exit' in query:
                    driver.quit()
                    speak("returning to old tasks")
                    break

                elif 'search' in query:
                    query = query.replace("search","")
                    inputEle = driver.find_element_by_css_selector('input[name=search_query]')
                    inputEle.send_keys(query)
                    inputEle.send_keys(Keys.ENTER)

                elif 'new tab' in query:
                    new_tab(driver)
                    total_tabs += 1

                elif 'open' in query:
                    new_links(driver)

        #searching on google       
        elif 'google' in query:
            speak("Launching Google")
            driver = webdriver.Chrome()
            driver.get("https://www.google.com")
            driver.maximize_window()
            total_tabs = 1
            page = "a"
            while True:
                query = takeCommand().lower()
                if 'close' in query or 'exit' in query:
                    driver.quit()
                    speak("returning to old tasks")
                    break
                    
                elif 'search' in query:
                    query = query.replace("search","")
                    inputEle = driver.find_element_by_css_selector('input[name=q]')
                    inputEle.send_keys(query)
                    inputEle.send_keys(Keys.ENTER)

                elif 'new tab' in query:
                    new_tab(driver)
                    total_tabs += 1

                elif 'open' in query:
                    new_links(driver)

        elif 'time' in query:
            Time()

        #exit from project               
        elif 'exit' in query or 'bye bye' in query:
            speak("Bye bye sir.... see you soon again")
            exit()
        
        
    