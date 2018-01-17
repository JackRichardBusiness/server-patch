print("Loading resources...")
from firebase import firebase
from googletrans import Translator
import chatterbot
from time import sleep
from subprocess import PIPE
from subprocess import Popen
import os
waiting = 0
translator = Translator()
database = firebase.FirebaseApplication("https://sabrina-415a1.firebaseio.com")
def getBusy():
	print('Getting busy...')
	waiting = 0
	database.put('server/01602', 'job', 'updating')
	os.system('sudo apt-get update')
	os.system('sudo apt-get upgrade')
try:
	chatbot = chatterbot.ChatBot("Sabrina")
	print("Starting server...")
	print("Reporting status...")
	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
	database.put('server/01602', 'status', 'online')
	database.put('server/01602', 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
	print("Reported.")
	print("Starting <SuperBot> ...")
	chatbot.set_trainer(chatterbot.trainers.ChatterBotCorpusTrainer)
	database.put('server/01602', 'job', 'training with corpus')
	chatbot.train("chatterbot.corpus.english")
	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
	database.put('server/01602', 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
	chatbot.set_trainer(chatterbot.trainers.ListTrainer)
	database.put('server/01602', 'job', 'training with database')
	result = database.get('lang/en', None)
	for key in result.keys():
		chatbot.train([key, result.get(key)])
	print("Started all services...")
	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
	database.put('server/01602', 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
	while True:
		print("Starting job...")
		cmd = database.get('server/01602/', None)
		if cmd.get('cmd') == '1':
			database.put('server/01602', 'status', 'offline')
			database.put('server/01602', 'temp', 'not recordable')
			database.put('server/01602', 'job', 'none')
			database.put('server/01602', 'cmd', '0')
			os.system('sudo shutdown')
			exit()
		elif cmd.get('cmd') == '2':
			database.put('server/01602', 'status', 'offline')
			database.put('server/01602', 'temp', 'not recordable')
			database.put('server/01602', 'job', 'none')
			database.put('server/01602', 'cmd', '0')
			os.system('sudo reboot')
		else:
			print("Beginning jobs...")
			database.put('server/01602', 'job', 'getting responses')
			database.put('server/01602', 'status', 'working')
		results = database.get('unknown/en', None)
		try:
			for keys in results.keys():
				database.put('lang/en', keys, str(chatbot.get_response(keys)))
				database.delete('unknown/en/', keys)
		except:
			print("None to correct")
		print("Completed <SuperBot> conversation help.")
		process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
		database.put('server/01602', 'temp', str(process.communicate()).split('temp=')[1].split('C')[0].replace("""'""", "") + "C")
		database.put('server/01602', 'job', 'resting')
		database.put('server/01602', 'status', 'sleeping')
		waiting = waiting + 1
		if waiting > 30:
			getBusy()
		print("Beginning rest...")
		sleep(10)
		print("Rest time over.")
except Exception as e:
	try:
		database.put('server/01602', 'status', 'error')
		database.put('server/01602', 'error', str(e))
		database.put('server/01602', 'job', 'rebooting')
		os.system('sudo reboot')
	except:
		file = open('errorlog.txt', 'w')
		file.write(str(e))
		file.close()
		os.system('sudo reboot')
