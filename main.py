import re
import sys

#text-to-speech
try:
	import pyttsx3
	tts_enabled = True
	tts = pyttsx3.init()
	tts.setProperty('rate', 150)
except ModuleNotFoundError:
	tts_enabled = False

def main():
	if len(sys.argv) == 3:
		is_command_line = True
	elif len(sys.argv) == 1:
		is_command_line = False
	else:
		print('Program usage:\nmain.py\nmain.py word1 word2')
		sys.exit()
	
	if not is_command_line:
		print('***spoonerism program***')
		print('(aka proonerism spogram)')
		print('This program takes two given words and generates a spoonerism of them.')
		print('This means that the consonants before a word\'s first vowel are swapped between words.')
		if tts_enabled:
			print('After generating the new words, text-to-speech will attempt to say them.')
		else:
			print('\npyttsx3 not installed! To enable text-to-speech please install pyttsx3 using "python -m pip install pyttsx3".')
		print()
	
	loop = True
	while loop:
		words = []
		if is_command_line:
			words = [sys.argv[1], sys.argv[2]]
			if not validateWords(words):
				sys.exit()
			#don't loop for command line usage
			loop = False
			
		else:
			words = getValidWords('Enter the two words separated by a space: ')
			
		word1_split = splitWord(words[0])
		word2_split = splitWord(words[1])
		new_word1 = word2_split[0] + word1_split[1]
		new_word2 = word1_split[0] + word2_split[1]
		
		print(words[0] + ' ' + words[1] + ' ---> ' + new_word1 + ' ' + new_word2 + '\n')
		
		if tts_enabled:
			sayWords(words, new_word1, new_word2)
	
#returns two valid words inputted by the user
def getValidWords(message):
	while True:
		words = input(message).lower().split()
		if not validateWords(words):
			continue
		return words
		
#checks to make sure a word is valid
#the word must contain only alphabetic characters and at least one vowel
#returns the truthiness of the word
def validateWords(words):
	if len(words) != 2:
		print('Please enter exactly two words separated by a space.')
		return False
	for word in words:
		if re.search('[^a-z]', word):
			print('Both words must contain only alphabetic characters.')
			return False
		if re.search('^[^aeiouy]*$', word):
			print('Both words must contain at least one vowel.')
			return False
		if re.search('^[^b-df-hj-np-tv-xyz]*$', word):
			print('Both words must contain at least one consonant.')
			return False
	return True

#returns a word split at its first consonants
def splitWord(word):
	#y is consonant
	if word[0] == 'y':
		first_vowel = re.search('[aeiou]', word)
	#y is vowel
	else:
		first_vowel = re.search('[aeiouy]', word)

	first_vowel_index = first_vowel.start()
	return [word[:first_vowel_index], word[first_vowel_index:]]
	
#use text-to-speech on the generated words
def sayWords(words, new_word1, new_word2):
	tts.say(words[0] + ' ' + words[1])
	tts.say(new_word1 + ' ' + new_word2)
	tts.runAndWait()
	
main()