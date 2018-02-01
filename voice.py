import scikits.audiolab as audiolab
import scipy, os
from google.cloud import storage
from firebase import firebase
database = firebase.FirebaseApplication('https://sabrina-415a1.firebaseio.com')
client = storage.Client()
bucket = client.get_bucket('sabrina-415a1.appspot.com')
os.chdir("Documents/Sabrina - Diana")
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
results = database.get('lang/en', None)
for sentence in results.values():
    sentence = sentence.replace("!", "").replace(", ", " ").replace(". ", " ").replace(".", "").lower()
    usedChars = []
    current = 0
    words = sentence.split(" ")
    try:
        for word in words:
            exec(chars[current]+", fs, enc = audiolab.wavread("+'"'+word+'.wav"'+")")
            usedChars += chars[current]
            current += 1
        exec("stack = scipy.vstack("+str(usedChars).replace("[", "(").replace("]", ")").replace("'", "")+")")
        audiolab.wavwrite(stack, sentence+".wav", fs, enc)
    except:
        continue
    blob = bucket.blob(sentence+".wav")
    blob.upload_from_filename(sentence+".wav")
