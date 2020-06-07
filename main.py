import os
import json
import getpass
import requests
import subprocess as s
import speech_recognition as sr
from gtts import gTTS
from time import sleep
from config import Database
from datetime import datetime
from playsound import playsound


def remove_all_audios():
    for file in os.listdir('audios'):
        os.remove('audios/{0}'.format(file))

def remove_audio(filename):
    if os.path.exists('audios/{0}.mp3'.format(filename)) is True:
        os.remove('audios/{0}.mp3'.format(filename))

def gtts_playsound(audio_name, text):
    remove_audio(audio_name)
    tts = gTTS(text, lang='pt-br')
    tts.save('audios/{0}.mp3'.format(audio_name))
    # Reproduz uma Mensagem de boas vindas
    playsound('audios/{0}.mp3'.format(audio_name))

def send_command(micro, result):
    waiting_command = True
    while(waiting_command is True):
        with sr.Microphone() as source:
            # Chama a funcao de reducao de ruido disponivel na speech_recognition
            micro.adjust_for_ambient_noise(source)
            # Armazena a informacao de audio na variavel
            command = micro.listen(source)
        try:
            command = micro.recognize_google(command, language='pt-BR')
            waiting_command = False
        except Exception:
            continue
    # Faça o comando
    if 'placa de vídeo' in command:
        gtts_playsound('vga_check', 'Abrindo dados da sua placa de vídeo')
        s.Popen('C:/Program Files/AMD/CNext/CNext/RadeonSoftware.exe')
    elif 'desempenho' in command:
        gtts_playsound('check_system', 'Abrindo dados de Hardware')
        s.Popen('C:/Program Files/WindowsApps/Microsoft.XboxGamingOverlay_5.220.4292.0_x64__8wekyb3d8bbwe/GameBar.exe')
    elif 'Call of Duty' in command or 'call of duty' in command:
        gtts_playsound('cod_warzone', 'Abrindo Call of Duty Warzone')
        s.Popen('"C:/Program Files (x86)/Call of Duty Modern Warfare/Modern Warfare Launcher.exe"')
    elif 'GTA' in command or 'gta' in command:
        gtts_playsound('gta', 'Abrindo GTA 5')
        s.Popen('com.epicgames.launcher://apps/9d2d0eb64d5c44529cece33fe2a46482?action=launch&silent=true')
    elif 'previsão' in command or 'Bom dia' in command:
        response = requests.get('https://api.hgbrasil.com/weather', allow_redirects=False)
        forecasts = json.loads(response.content)['results']['forecast']
        # Pega a data atual e converte em (dia/mes ex 06/06)
        date_now = datetime.now().strftime('%d/%m')
        for forecast in forecasts:
            if str(forecast['date']) == str(date_now):
                if 'Bom dia' in command:
                    gtts_playsound('temperature', '''
                    Bom dia senhor {0}. Hoje é dia {1} A previsão do tempo para o dia de hoje é máxima de {2} graus e mínima de {3} graus com chances de {4}'''.format(
                        result[1],
                        date_now,
                        forecast['max'],
                        forecast['min'],
                        forecast['description']))
                else:
                    gtts_playsound('temperature', 'A previsão do tempo para o dia de hoje é máxima de {0} graus e mínima de {1} graus com chances de {2}'.format(forecast['max'], forecast['min'], forecast['description']))
                break
    elif 'ambiente' in command:
        gtts_playsound('workdesk', 'Preparando o seu ambiente de trabalho, tenha um ótimo trabalho!')
        # Abrir Visual Studio
        s.Popen(['C:/Users/Vinícius Valle/AppData/Local/Programs/Microsoft VS Code/Code.exe',
                #  '-g C:/Users/Vinícius Valle/Documents/Take5/take5_api',
                #  '-g C:/Users/Vinícius Valle/Documents/Take5/etraining-vue'
                ])
        # Abrir GitHub
        s.Popen('C:/Users/Vinícius Valle/AppData/Local/GitHubDesktop/GitHubDesktop.exe')
        # Abrir HeidiSQL
        s.Popen('C:/Program Files/HeidiSQL/heidisql.exe')
        # Abrir Chrome
        s.Popen(['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', 'https://meet.google.com/pyf-vxry-nnc?authuser=1', 'gmail.com', 'take5.monday.com'])
        # Abrir Telegram
        s.Popen('C:/Users/Vinícius Valle/AppData/Roaming/Telegram Desktop/Telegram.exe')
    elif 'desligar' in command:
        remove_all_audios()
        exit()
    send_command(micro, result)

def authenticated():
    gtts_playsound('ready_to_voice', 'Informe o seu código de acesso')
    # input('Informe o seu código de acesso', access_token)
    access_token = getpass.getpass('Código de acesso: ')
    return access_token


def initial_system():
    # Remove os aúdios pré-existents
    # Inicia a conexão com o banco de dados
    connection = Database()
    print('''
    ----------------------------------------------------------------------------
    |                     TESS - VIRTUAL ASSISTANT 1.0                         |
    ----------------------------------------------------------------------------
    ''')
    # Mensagem de boas vindas do sistema
    gtts_playsound('hello', 'Bem vindo à Tess')

    # Instancia microfone
    micro = sr.Recognizer()

    # Inícia o módulo de autenticação
    access_token = authenticated()

    # Valida o código de acesso
    result = connection.find_access_token(access_token)
    if result:
        print('Acesso liberado...')
        gtts_playsound('authenticated', 'Código de acesso aceito, seja bem vindo {0}'.format(result[1]))
        send_command(micro, result)
    else:
        gtts_playsound('not_authenticated', 'Código de acesso inválido, tente novamente')
        authenticated(micro)


initial_system()
