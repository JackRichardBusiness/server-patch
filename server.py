print("Loading resources...")
from firebase import firebase
from googletrans import Translator
import chatterbot
from time import sleep
from subprocess import PIPE
from subprocess import Popen
import os
zipcode = "01602"
url = 'server/' + zipcode
waiting = 0
translator = Translator()
times = 0
database = firebase.FirebaseApplication("https://sabrina-415a1.firebaseio.com")
try:
        latest = database.get("server/update", "patch")
        current = open("serverPatch.txt", "r")
        if not current == latest:
                os.system("python3 /home/pi/run.py")
        chatbot = chatterbot.ChatBot("Sabrina")
        print("Starting server...")
        print("Reporting status...")
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        database.put(url, 'status', 'online')
        database.put(url, 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
        print("Reported.")
        print("Starting <SuperBot> ...")
        chatbot.set_trainer(chatterbot.trainers.ChatterBotCorpusTrainer)
        database.put(url, 'job', 'training with corpus')
        chatbot.train("chatterbot.corpus.english")
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        database.put(url, 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
        chatbot.set_trainer(chatterbot.trainers.ListTrainer)
        database.put(url, 'job', 'training with database')
        result = database.get('lang/en', None)
        for key in result.keys():
                chatbot.train([key, result.get(key)])
        print("Started all services...")
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        database.put(url, 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
        while True:
                times = times + 1
                print("Starting job...")
                cmd = database.get(url, None)
                if cmd.get('cmd') == '1':
                        database.put(url, 'status', 'offline')
                        database.put(url, 'temp', 'not recordable')
                        database.put(url, 'job', 'none')
                        database.put(url, 'cmd', '0')
                        os.system('sudo shutdown')
                        exit()
                elif cmd.get('cmd') == '2':
                        database.put(url, 'status', 'offline')
                        database.put(url, 'temp', 'not recordable')
                        database.put(url, 'job', 'none')
                        database.put(url, 'cmd', '0')
                        os.system('sudo reboot')
                else:
                        print("Beginning jobs...")
                        database.put(url, 'job', 'getting responses')
                        database.put(url, 'status', 'working')
                results = database.get('unknown/en', None)
                try:
                        for keys in results.keys():
                                resultsO = database.get("lang/en", None)
                                dic = {}
                                words = unknown.split(" ")
                                for result in resultsO.keys():
                                        match = 0
                                        overall = len(result.split(" "))+1
                                        for word in result.split(" "):
                                                for wor in words:
                                                        if wor == word:
                                                                match += 1
                                        dic[int(str(match/overall*100).split(".")[0])] = result
                                if int(max(dic.keys())) > 60:
                                    print("Possible match found!")
                                    database.put('lang/en', keys, results0.get(str(dic.get(max(dic.keys())))))
                                    database.delete('unknown/en/', keys)
                                else:
                                        database.put('lang/en', keys, str(chatbot.get_response(keys)))
                                        database.delete('unknown/en/', keys)
                except:
                        print("None to correct")
                print("Completed <SuperBot> conversation help.")
                process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
                database.put(url, 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
                database.put(url, 'job', 'resting')
                database.put(url, 'status', 'sleeping')
                print("Beginning rest...")
                sleep(10)
                print("Rest time over.")
                if times > 30:
                        database = firebase.FirebaseApplication('https://sabrina-415a1.firebaseio.com')
                        times = 0
except Exception as e:
        try:
                database.put(url, 'status', 'error')
                database.put(url, 'error', str(e))
                database.put(url, 'job', 'rebooting')
                os.system('sudo reboot')
        except:
                file = open('errorlog.txt', 'w')
                file.write(str(e))
                file.close()
                os.system('sudo reboot')


