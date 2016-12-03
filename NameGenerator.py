# Initial code base on this website:
# http://www.pythoncoding.com/areas/basics/random-word-generator/


import random
def generateRandomName(numOfBits, upper=False, capitalize=True):

	bits=[]
	vowels="aeiou"
	consonants = "bcdfghjklmnpqrstvwxyz"
	letters="abcdefghijklmnopqrstuvwxyz"
	#Create all possible 2 letter combinations
	for ch in letters:
		for v in vowels:
			bits.append(ch+v)
		for c in consonants:
			if c not in "jhqvwxy":
				bits.append(c+c)
	
	#Trying to avoid swear words and odd literals
	bits.remove("fu")
	bits.remove("hi")
	bits.remove("cu")
	bits.remove("co")
	bits.remove("mo")
	bits.remove("xo")
	word=""
	
	
	#Randomize the number of 2 letter combinations to generate if -ve number used as arg
	if numOfBits < 0:
		numOfBits=random.randint(1, 5)
	
	rnd=len(bits)-1
		
	for i in range(0,numOfBits):
		#print(word)
		bit = ''
		
		#If we have a partial word
		if word != '':
			#Check for preceeding double consonants
			if word[-1] in consonants:
				if word[-2] in consonants:
					
					#Pick something that does not start with a consonant (3 consonants looks odd)
					#print("double consonant")
					while bit == '' or bit[0] not in vowels:
						bit = bits[random.randint(1, rnd)]
						#print("\t\t" + bit)
					word = word + bit
				#If consonant+vowel are last two letters, then choose any random 2 letter combo
				else:
					word=word+bits[random.randint(1, rnd)]
			
			#Check for preceeding double vowels
			elif word[-1] in vowels:
				if word[-2] in vowels:
					
					#Pick something that does not start with a vowel (3 vowels looks odd)
					#print("double vowel")
					while bit == '' or bit[0] not in consonants:
						bit = bits[random.randint(1, rnd)]
						#print("\t\t" + bit)
					word = word + bit
				#If vowel+consonant are last two letters, then choose any random 2 letter combo
				else:
					word = word + bits[random.randint(1, rnd)]
					
		#If we are starting
		else:
			
			#Randomize a starting 2 letter combo and don't start with double consonant
			bit = bits[random.randint(1, rnd)]
			#print("Initial: " + bit)
			while bit[0] in consonants and bit[1] in consonants:
				bit = bits[random.randint(1, rnd)]
				#print("Regenerated Initial: " + bit)
			word = word + bit
	
	#Add last letter to word, check for doubles and put the opposite
	if word[-1] in vowels and word[-2] in vowels:
		word = word+consonants[random.randrange(0, 21)]
		
	elif word[-1] in consonants and word[-2] in consonants:
		word = word+vowels[random.randrange(0, 5)]
		
	else:
		word=word+letters[random.randrange(0,25)]


	if (capitalize):
		word=word.capitalize()
	if (upper):
		word = word.upper()
	return word

'''
for i in range(1,1000):
		print(generateRandomName(-1, True))
'''
