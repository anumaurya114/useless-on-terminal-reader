from tqdm import tqdm
import os
from pydub import AudioSegment 
import sys
def flac_to_wav(old_path,new_path):
	newAudio = AudioSegment.from_file(old_path)

	 

	newAudio.export(new_path, bitrate ='192k', format ="wav")

def main(old_dir='db/eng-wcp-us_flac/flac/',new_dir='db/english_audio/'):
	try:
		os.mkdir(new_dir)
	except:
		pass
	for file in tqdm(os.listdir(old_dir)[:]):
		
		if '.flac' in file:
			word = file.split('.')[0].split('-')[-1]
			# print(word)
			old_path = os.path.join(old_dir,file)
			new_path = os.path.join(new_dir , word+'.wav')
			flac_to_wav(old_path,new_path)
			# break

old_dir = sys.argv[1]
new_dir = sys.argv[2]
print('from ',old_dir,' to ',new_dir)
main(old_dir,new_dir)
