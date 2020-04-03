import time
import os 
import re
import sys
from utility import *
import warnings
import sys
warnings.filterwarnings("ignore")
# for x in range (0,5):  
#     b = "Loading" + "." * x
#     print (b, end="\r")
# #     time.sleep(1)


# from mock import patch
# with patch('sys.stdout', devnull):
#     with patch('sys.stderr', devnull):
#         pass

# def get_text(filename):
# 	with open(filename,'r') as fh:
# 		return fh.read()

def traverse(para,db_dir,audio_collection):
	def preprocess(para):
		
		return ' '.join(para.split())
	para = preprocess(para)
	
	

	count = 0
	res = re.finditer(r'\w+',para)
	num_lines = len(para.split('\n'))+1
	print(num_lines)
	for i in res:
		count +=1
		
		to_print = para[:i.start()] + '\x1b[6;30;42m' + i.group() + '\x1b[0m' + para[i.end():]
		

		for j in range(200):
			sys.stdout.write("\x1b[1A\x1b[2K")
		print(to_print)
		audio_collection.speak(i.group().lower())
		time.sleep(delay_time)

def split_on(string,breakers):
	chunk = ''
	for i in string:
		if i in breakers:
			yield (chunk,i)
			chunk=''
		else:
			chunk+=i
	yield (chunk,'')	


def next_chunk(text_file):
	count_dots = 0
	remaining = ''
	remaining_count = 0
	breakers = ['.', ',']
	with open(text_file) as fh:
		for line in fh:
			ret_remain = True
			count_dots = remaining_count
			chunk = remaining
			count = line.count('.')+line.count(',')
			if count+count_dots>5:
				remaining_count = 0
				remaining = ''
				j = 0 
				for l,breaker in split_on(line,breakers):
					if j+count_dots<15:
						chunk += l+breaker
						count_dots+=1
						count-=1
						j+=1
					else:
						remaining_count+=1
						remaining +=l+breaker
				
				count = 0
				ret_remain = False
				yield chunk,count_dots
				count_dots = 0
				chunk = ''

			else:
				chunk += line
				remaining = chunk
				count_dots +=count
				remaining_count = count_dots
				
				ret_remain = True
		if ret_remain:
			yield remaining,count_dots
		
		

def reader(text_file,db_dir):
	audio_collection = AudioCollector(db_dir)
	audio_collection.load_word_audio_dic()
	print("collection created.")

	for chunk,count in next_chunk(text_file):
		# print(chunk)
		# print("*****"*12)
		# print(c)
		# print("*****"*12)
		# continue
		traverse(chunk,db_dir,audio_collection)


# para = get_text('story.txt')

# traverse(para)

#db_dir = 'db/english_audio/'
text_file = sys.argv[1]
db_dir = sys.argv[2]
delay_time = float(sys.argv[3])
reader(text_file,db_dir)
