print("Loading resources...")
from firebase import firebase
import chatterbot
from time import sleep
from subprocess import PIPE
from subprocess import Popen
import os
url = 'server/'
database = firebase.FirebaseApplication("https://sabrina-415a1.firebaseio.com")
status = firebase.FirebaseApplication("https://sabrina-415a1-01602.firebaseio.com")
file = open("serverPatch.txt", "r")
status.put(url, 'version', str(file.read()))
file.close()
def update(statusStr, job):
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        status.put(url, 'status', statusStr)
        status.put(url, 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
        status.put(url, 'job', job)
try:
        chatbot = chatterbot.ChatBot("Sabrina")
        print("Starting server...")
        print("Reporting status...")
        print("Reported.")
        update("online", "training")
        chatbot.set_trainer(chatterbot.trainers.ListTrainer)
        result = database.get('lang/en', None)
        for key in result.keys():
                chatbot.train([result.get(key+"/native0", None), result.get(key+"/native0")])
        print("Started all services...")
        update("working", "beginning jobs")
        while True:
                print("Starting job...")
                cmd = status.get(url, None)
                if cmd.get('cmd') == '1':
                        update("offline", "none")
                        status.put(url, 'temp', 'not recordable')
                        status.put(url, 'cmd', '0')
                        os.system('sudo shutdown 0')
                        exit()
                elif cmd.get('cmd') == '2':
                        update("offline", "none")
                        status.put(url, 'temp', 'not recordable')
                        status.put(url, 'cmd', '0')
                        os.system('sudo reboot')
                elif cmd.get('cmd') == '3':
                        update("working", "running command")
                        os.system(str(cmd.get("shell")))
                        status.delete(url, 'shell')
                        status.put(url, 'cmd', '0')
                else:
                        print("Beginning jobs...")
                        update("working", "finding unknown")
                results = database.get('unknown/en', None)
                try:
                        unknowns = database.get("unknown/en/", None)
                        for unknown in unknowns.keys():
                                results = database.get("lang/en", None)
                                dic = {}
                                words = unknown.split(" ")
                                for result in results.keys():
                                        match = 0
                                        overall = len(result.split(" "))+1
                                        for word in result.split(" "):
                                                for wor in words:
                                                        if wor == word:
                                                                match += 1
                                        dic[int(str(match/overall*100).split(".")[0])] = result
                                if int(max(dic.keys())) > 60:
                                        print(results.get(str(dic.get(max(dic.keys())))))
                                        database.delete('unknown/en', unknown)
                                        database.put("lang/en", unknown, str(results.get(str(dic.get(max(dic.keys()))))))
                                else:
                                        database.delete('unknown/en', unknown)
                                        database.put("lang/en", unknown, str(chatbot.get_response(unknown)))
                except:
                        print("None to correct")
                print("Completed <SuperBot> conversation help.")
                update("sleeping", "none")
                print("Beginning rest...")
                sleep(30)
                database = firebase.FirebaseApplication("https://sabrina-415a1.firebaseio.com")
                print("Rest time over.")
except Exception as e:
        try:
                status.put(url, 'status', 'error')
                status.put(url, 'error', str(e))
                status.put(url, 'job', 'rebooting')
                os.system('sudo reboot')
        except:
                file = open('errorlog.txt', 'w')
                file.write(str(e))
                file.close()
                os.system('sudo reboot')


