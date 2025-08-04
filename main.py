from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой

def start(recognizer, microphone):
    recognized_data = ""
    waiting = True

    while waiting:
        with microphone as sourse:
            print("Ожидаю вызова...")
            audio = recognizer.listen(sourse, phrase_time_limit=None)
            with open("wait_for_call.wav", "wb") as file:
                file.write(audio.get_wav_data())

            try:
                print("Перевожу...")
                recognized_data = recognizer.recognize_google(audio, language="RU-ru").lower()
            except speech_recognition.UnknownValueError:
                pass
            print(recognized_data)
            if "привет" in recognized_data:
                waiting = False
            recognized_data=""

    os.remove("wait_for_call.wav")
    return listen_for_command(recognizer,microphone)

def listen_for_command(recognizer, microphone):

    with microphone as sourse:
        recognized_data = ""

        try:
            print("Ожидаю команду...")
            audio = recognizer.listen(sourse, phrase_time_limit=None)

            with open("wait_for_command.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            print("Перевожу...")
            recognized_data = recognizer.recognize_google(audio, language="RU-ru").lower()
        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит попытка
        # использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")
        os.remove("wait_for_command.wav")
        return recognized_data


if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        # и удалением записанного в микрофон аудио
        voice_input = start(recognizer, microphone)
        print(voice_input)

