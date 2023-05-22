import speech_recognition as sr
import sounddevice as sd
import wavio as wv
import pyttsx3
import webbrowser
import psutil
import datetime
import time


def iaFala(fala):
    engine = pyttsx3.init()
    engine.say(fala)
    engine.runAndWait()


def pesquisaggl(fala):
    frase = fala
    search = frase.replace("Pesquisar", "")
    search2 = search.replace("pesquisar", "")
    webbrowser.open(f"https://www.google.com/search?q={search2}")


def grava():
    freq = 48000
    duration = 5
    gravacao = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    print("Fale agora!")
    sd.wait()
    wv.write("minhavoz.wav", gravacao, freq, sampwidth=2)


iaFala("Olá sou a Clhoe o que deseja?")

import time

ativo = True
pausado = False

while True:
    grava()
    r = sr.Recognizer()
    filename = "minhavoz.wav"
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="pt-br")
            print("Você disse:" + text)
            fala = text.lower()
        except sr.UnknownValueError:
            print("Não foi possível entender a fala")
            fala = ""

    if ativo and not pausado: 
        if fala == "bom dia" or fala == "boa tarde" or fala == "boa noite":
            iaFala(
                "Para você também! "
                "Agora são: " + datetime.datetime.now().strftime("%H:%M")
            )

        word = "pesquisar"
        if fala not in ["bom dia", "boa tarde", "boa noite"]:
            if word in fala:
                time.sleep(2)
                pesquisaggl(fala)

        if fala == "abrir o youtube":
            webbrowser.open("https://www.youtube.com/")
        elif fala == "abrir o chat gpt":
            webbrowser.open("https://chat.openai.com/")
        elif fala == "abrir o instagram":
            webbrowser.open("https://www.instagram.com/")

        powerOff = "sair"
        if fala == powerOff:
            iaFala("Desligando...")
            for proc in psutil.process_iter(["name"]):
                if "chrome" in proc.info["name"]:
                    proc.kill()
                if "edge" in proc.info["name"]:
                    proc.kill()
                if "firefox" in proc.info["name"]:
                    proc.kill()
            break

        if fala == "pausar":
            iaFala("Pausando...")
            pausado = True  

    elif ativo and pausado:  
        if fala == "iniciar":
            iaFala("Retomando...")
            pausado = False  
