import os
from pydub import AudioSegment 
from pydub.playback import play
import pickle
import sys
from gtts import gTTS

# import sys, os
# _stderr = sys.stderr
# _stdout = sys.stdout
# null = open(os.devnull,'wb')
# sys.stdout = sys.stderr = null
# sys.stderr = _stderr
# sys.stdout = _stdout

class AudioCollector:
	def __init__(self,db_dir):
		# f = open('../db/word_audio_dic','rb')
		# word_audio_dic = pickle.load(f)

		
		# self.dic = word_audio_dic
		# print(sorted([i for i in self.dic.keys() if len(i) and i[0]=='w']))
		# exit(0)
		self.word_audio_dic = {}
		self.db_dir = db_dir
	def speak(self,word):
		if word in self.word_audio_dic.keys():
			if os.path.isfile(os.path.join(self.db_dir,self.word_audio_dic[word])):
				self.play_audiof(os.path.join(self.db_dir,self.word_audio_dic[word]))
			else:
				# print("Here error")
				self.speak_the_word(word)
		else:
			#print("word not in collection")
			self.speak_the_word(word)



# def speech_recognizer(audio):
# 	return "Text result recognized"

	def text2audiof(self,text,filename='good.mp3'):
		tts = gTTS(text=text, lang='en',slow=True)

		tts.save(filename)
		os.system(filename)

	def play_audio(self,audio):
		play(audio)

	def mp3_to_wav(self,filename,new_dir='.'):
		newAudio = AudioSegment.from_file(os.path.join(filename))

		new_filename = filename.split('.')[0]+'.wav'

		newAudio.export(os.path.join(new_dir,new_filename), bitrate ='192k', format ="wav")

	# def audio2textf(self,audio,filename):
	# 	with open(filename,'w') as fh:
	# 		fh.write(audio2text(audio))

	# def audio2text(self,audio):
	# 	text = speech_recognizer(audio)
	# 	return text

	def play_audiof(self,filename='good.wav'):
		song = AudioSegment.from_wav(filename)
		play(song)
		# for j in range(3):
		# 		sys.stdout.write("\x1b[1A\x1b[2K")

	def speak_the_word(self,word):
		self.text2audiof(word,word+'.mp3')
		self.mp3_to_wav(word+'.mp3',self.db_dir)
		try:
			self.play_audiof(os.path.join(self.db_dir,word+'.wav'))
		except:
			pass
		try:
			os.remove(word+'.mp3')
		except:
			pass
		self.word_audio_dic[word] = word+'.wav'
		#print(self.word_audio_dic)
		self.save_word_audio_dic()

	
	def save_word_audio_dic(self):
		
		with open(os.path.join('word_audio_dic'),'wb+') as fh:
			pickle.dump(self.word_audio_dic,fh)
		
	def load_word_audio_dic(self):
		if os.path.isfile(os.path.join('word_audio_dic')):

			with open(os.path.join('word_audio_dic'),'rb') as fh:
				self.word_audio_dic = pickle.load(fh)
		else:
			
			try:
				self.create_word_audio_dic()
				#print(self.word_audio_dic)
				self.save_word_audio_dic()
				self.load_word_audio_dic()
			except Exception as e:
				raise ValueError("Could not create word audio dic "+ str(e))
		
	def create_word_audio_dic(self):
		self.word_audio_dic = {}
		for file in os.listdir(self.db_dir):
			self.word_audio_dic[file.split('.')[0]] = file



	# def get_audio(self,filename):
	# 	newAudio = AudioSegment.from_file(filename)
	# 	return newAudio

	# def get_audio_for_word(word):
	# 	text2audiof(word,'good.mp3')
	# 	mp3_to_wav('good.mp3')
	# 	return get_audio('good.wav')