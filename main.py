from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition as sr  # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой
import socket

"""##########################___STARTING_PROGRAMM___##########################"""

def start(recognizer, microphone):
    recognized_data = ""
    waiting = True

    while waiting:
        with microphone as sourse:
            recognizer.adjust_for_ambient_noise(sourse, duration=1)
            print("Ожидаю вызова...")
            audio = recognizer.listen(sourse, phrase_time_limit=None)

            with open("wait_for_call.wav", "wb") as file:
                file.write(audio.get_wav_data())

            try:
                print("Перевожу...")
                recognized_data = recognizer.recognize_google(audio, language="RU-ru").lower()
            except sr.UnknownValueError:
                pass
            print(recognized_data)
            if "джин" in recognized_data:
                waiting = False
            recognized_data=""

    os.remove("wait_for_call.wav")
    return listen_for_command(recognizer,microphone)


def listen_for_command(recognizer, microphone):

    with microphone as sourse:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(sourse, duration=1)

        try:
            print("Ожидаю команду...")
            audio = recognizer.listen(sourse, phrase_time_limit=None)

            with open("wait_for_command.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except sr.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Перевожу...")
            recognized_data = recognizer.recognize_google(audio, language="RU-ru").lower()

            execute_command_with_name(recognized_data)

        except sr.UnknownValueError:
            pass

        except sr.RequestError:
            print("Trying to use offline recognition...")
        os.remove("wait_for_command.wav")
        return execute_command_with_name(recognized_data)

commands = {
    "greeting": ["привет", "здравствуй", "добрый день", "доброе утро", "добрый вечер"],
    'searching': ["найти", "найди"],
    "opening": ["открой", "запусти"],
    "writing": ["записывай", "конcпектируй"],
    "waiting": ["слушаю вас", "я во внимании"],
    "special_commands": ["за работу"],
    "graduation": ["спасибо", "благодарю", "умница", "молодец"],
    "answer_for_graduation": ["обращайтесь", "к вашим услугам"]
}

def execute_command_with_name(command_name):
    print(command_name)
    command = ""
    for key in commands.keys():
        if command_name in commands[key]:
            command = key
    if command == "greeting":
        return greeting()
    elif command == "searching":
        return searching()
    elif command == "opening":
        return opening()
    elif command == "writing":
        return writing()
    elif command == "special_commands":
        return special_commands()
    elif command == "graduation":
        return graduation()
    elif command == "answer_for_graduation":
        return answer_for_graduation()
    else:
        return "Команда не распознана"

"""##########################___COMMANDS___##########################"""

def greeting():
    pass

def searching():
    pass

def opening():
    pass

def writing():
    pass

def special_commands():
    pass

def graduation():
    pass

def answer_for_graduation():
    pass


"""##########################___SETUP___##########################"""

def f():
    return "Соединение разорвано"

if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("www.example.com", 80))
        print("Connected successfully!")

        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        while True:
            voice_input = start(recognizer, microphone)

            print(voice_input)
    except socket.error as e:
        print(f"Connection failed: {e}")

    finally:
        sock.close()
