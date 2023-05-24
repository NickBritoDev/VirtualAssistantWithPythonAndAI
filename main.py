import re
import threading
import winsound
import pygame 
import speech_recognition as sr
import sounddevice as sd
import wavio as wv
import pyttsx3
import webbrowser
import psutil
import datetime
import time
import wikipedia
import pywhatkit
import os

alarme_ativo = False
ativo = True
pausado = False


def iaFala(fala):
    engine = pyttsx3.init()
    engine.say(fala)
    engine.runAndWait()


def criar_alarme(hora, minutos, arquivo_audio):
    global alarme_ativo
    hora = int(hora)
    minutos = int(minutos)

    alarme = hora * 60 + minutos
    agora = time.localtime()
    agora_minutos = agora.tm_hour * 60 + agora.tm_min

    if agora_minutos >= alarme:
        alarme += 24 * 60

    tempo_restante = alarme - agora_minutos

    print(f"Alarme criado para {hora}:{minutos:02d}.")
    iaFala(f"Alarme criado para {hora}:{minutos:02d}.")
    print(
        f"Tempo restante: {tempo_restante // 60} horas {tempo_restante % 60} minutos."
    )
    iaFala(
        f"Tempo restante: {tempo_restante // 60} horas {tempo_restante % 60} minutos."
    )

    time.sleep(tempo_restante * 60)
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo_audio)
    pygame.mixer.music.play()


def criar_alarme_thread(hora, minutos, arquivo_audio):
    global alarme_ativo
    alarme_ativo = True
    thread = threading.Thread(target=criar_alarme, args=(hora, minutos, arquivo_audio))
    thread.start()


def parar_alarme():
    global alarme_ativo
    alarme_ativo = False
    pygame.mixer.music.stop()


def pesquisa_google(fala):
    frase = fala
    search = frase.replace("Pesquisar", "")
    search2 = search.replace("pesquisar", "")
    webbrowser.open(f"https://www.google.com/search?q={search2}")


def pesquisa_wikipedia(fala):
    frase = fala
    search = frase.replace("procure por", "")
    wikipedia.set_lang("pt")
    try:
        resultado = wikipedia.summary(search, 2)
        print(resultado)
        iaFala(resultado)
    except wikipedia.exceptions.PageError:
        print("Desculpe, não foram encontrados resultados para a pesquisa.")
        iaFala("Desculpe, não foram encontrados resultados para a pesquisa.")


def pesquisa_youtube(fala):
    musica = fala.replace("toque", "")
    pywhatkit.playonyt(musica)
    iaFala("Tocando...")
    print("Tocando...")


def grava():
    freq = 48000
    duration = 5
    gravacao = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    print("Fale agora!")
    sd.wait()
    wv.write("minhavoz.wav", gravacao, freq, sampwidth=2)


iaFala("Olá sou a Chloe o que deseja?")

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

    # saudação com hora atual
    if ativo and not pausado:
        if fala == "bom dia" or fala == "boa tarde" or fala == "boa noite":
            iaFala(
                "Para você também! "
                "Agora são: " + datetime.datetime.now().strftime("%H:%M")
            )

        # cria um novo alarme
        if fala.startswith("criar alarme"):
            parametros = re.findall(r"\d+", fala)
            if len(parametros) >= 2:
                hora, minutos = parametros[:2]
                arquivo_audio = "sound.mp3"
                criar_alarme_thread(hora, minutos, arquivo_audio)
            else:
                iaFala(
                    "Desculpe, o comando está incorreto. Por favor, especifique a hora e os minutos."
                )
                print(
                    "Desculpe, o comando está incorreto. Por favor, especifique a hora e os minutos."
                )
        # deliga o alarme
        elif fala == "deligar alarme":
            parar_alarme()

        # pesquisa no google
        word = "pesquisar"
        if fala not in ["bom dia", "boa tarde", "boa noite"]:
            if word in fala:
                time.sleep(2)
                pesquisa_google(fala)

        # pesquisa no wikipedia
        if fala.startswith("procure por"):
            search_query = fala.replace("procure por", "").strip()
            time.sleep(2)
            pesquisa_wikipedia(search_query)

        # pesquisa no youtube
        if fala.startswith("toque"):
            pesquisa_youtube(fala)

        # executa comando especificos
        if fala == "abrir o youtube":
            webbrowser.open("https://www.youtube.com/")
        elif fala == "abrir o chat gpt":
            webbrowser.open("https://chat.openai.com/")
        elif fala == "abrir o instagram":
            webbrowser.open("https://www.instagram.com/")
        elif fala == "abrir o facebook":
            webbrowser.open("https://www.facebook.com/")
        elif fala == "abrir a bet":
            webbrowser.open("https://www.bet365.com/")
        elif fala == "abrir o mercado livre":
            webbrowser.open("https://www.mercadolivre.com.br/")
        elif fala == "abrir a amazon":
            webbrowser.open("https://www.amazon.com/")
        elif fala == "abrir o linkedin":
            webbrowser.open("https://www.linkedin.com/")
        elif fala == "abrir o github":
            webbrowser.open("https://github.com/")
        elif fala == "abrir a twitch":
            webbrowser.open("https://www.twitch.tv/")
        elif fala == "abrir o pinterest":
            webbrowser.open("https://br.pinterest.com/")

        # deliga e fecha o navegador
        powerOff = "sair"
        if fala == powerOff:
            iaFala("Desligando...")
            for proc in psutil.process_iter(["name"]):
                if "chrome" in proc.info["name"]:
                    proc.kill()
            break

        # pausa os comandos e fica em escuta esperando comando para iniciar
        if fala == "pausar":
            iaFala("Pausando...")
            print("Pausando...")
            pausado = True

    # reinicia a escuta de comandos
    elif ativo and pausado:
        if fala == "iniciar":
            iaFala("iniciando...")
            print("iniciando...")
            pausado = False
