import pyttsx

def sayAnswer(answer):
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-42)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'english-us')
    engine.say(answer)
    engine.runAndWait()
