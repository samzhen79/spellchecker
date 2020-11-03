import time, re, datetime, sys
from difflib import SequenceMatcher

def options (num):	#Alot of menus in this code, might aswell make a function for it. When given any a number of options, it will ensure a valid option is selected.

	while True:
		try:

			#This effectively replaces the previous line, to the user this means the terminal stays in the same place.
			sys.stdout.write('\x1b[1A'+'\x1b[2K')

			prompt = int(input("Please choose an option by entering its corresponding number: "))

			if prompt in set (num): #If prompt is part of the given options then it will return the value of the chosen option

				#This clears the terminal 
				sys.stdout.write('\x1bc')

				return(prompt)
			
			else: #If any integer that is not a valid option is inputted

				time.sleep(0.5)
				sys.stdout.write('\x1b[1A'+'\x1b[2K')
				input("This is not a valid option. Press enter to try again...")
				time.sleep(0.5)

		except ValueError: #If any none integer is inputted

			time.sleep(0.5)
			sys.stdout.write('\x1b[1A'+'\x1b[2K')
			input("You did not enter a number. Press enter to try again...")
			time.sleep(0.5)

def initialmenu(): #Starting menu to allow user to choose how they want to use the program
	
	sys.stdout.write('\x1bc')
	
	#Nice looking title + border thing.
	print("\n\u2554"+"\u2550"*14+"\u2557"
		"\n\u2551 Spellchecker \u2551"
		"\n\u255a"+"\u2550"*14+"\u255d")

	print("\n 1. Spellcheck a sentence"
		"\n 2. Spellcheck a file" 
		"\n 0. Quit program\n\n")

	option = options({1, 2, 0})

	if option == 1:

		sentence = input("Please enter your sentence: ")

		time.sleep(0.5)
		string, summary = spellcheck(sentence)

	elif option == 2:
		while True:
			try:


				filename = input("\nPlease enter the filename: ")
				f = open(filename, "r") 
				file = f.read()
				f.close()

				break
			
			except FileNotFoundError:

				time.sleep(0.5)

				print("\nCannot find the file with filename " + filename + ".\n")

				print("\n1. To try another filename"
					"\n2. To return to initial menu\n\n")

				option = options({1, 2})

				if option == 1:

					break

				elif option == 2:

					initialmenu()

		string, summary = spellcheck(file)

	else:
		return

	while True:
		try:

			time.sleep(0.5)
			filewrite = input("\nPlease enter a filename to create: ")
			f = open(filewrite, "x")
			loglist = string.split() #Technically don't need to do this as we could instead return a list from the spellcheck function,
									 #But this retains the previous functionality of the code if I wanted to change it back in the future.
			logstring = ""

			for word in loglist: #This formats the text file as a long list of words
				logstring = (logstring + "\n" + word)

			f.write(summary + logstring)
			f.close()
			break
			
		except FileExistsError:

			time.sleep(0.5)
			input("\nA file with the name " + filename + " already exists. Press enter to try again...")
			time.sleep(0.5)

	sys.stdout.write('\x1bc')

	print("\n 1. Return to starting menu" 
		"\n 0. Quit program\n\n")

	option = options({1, 0})

	if option == 1:

		initialmenu()

	else:

		return

def spellcheck(checkstring):

	starttime = datetime.datetime.now() #Gets the current date and time.
	startcounter = time.perf_counter() #Gets the current counter value. This will be used later to find the total elapsed time in seconds.

	cleanstring = re.sub(r"[^\w\s]|[\b\d+\b]", "", checkstring.lower()) #Removes punctuation and numbers from text. Also makes everything lowercase.
	checklist = cleanstring.split() #Splits the words in the text into items of a list
	string = cleanstring #Will be used for the new file after spellcheck

	f = open("EnglishWords.txt", "r")
	wordslist = (f.read()).splitlines() #Splits the words in the file by line into items of a list
	f.close()

	#Assigning variables for statistics

	totalwordcount, correctwordcount, incorrectwordcount, addDictionary, suggestionCount = 0, 0, 0, 0, 0

	for word in checklist: #Loops through each word of the list that we are spellchecking
		time.sleep(0.3)
		if (word in wordslist) == False: #Checks if the word is in the EnglishWords.txt list

			sys.stdout.write('\x1b[1A'+'\x1b[2K')

			print(word + " is spelt incorrectly")
			time.sleep(0.5)

			print("\n 1. Ignore"
			"\n 2. Mark" 
			"\n 3. Add to dictionary"
			"\n 4. Suggest likely correct spelling\n\n")

			option = options({1, 2, 3, 4})

			if option == 1: #This will ignore the current word but increase the incorrect word count

				incorrectwordcount += 1

			elif option == 2: #This will replace the word with itself with question marks around it

				string = string.replace(word, "?" + word + "?", 1) #Adds question marks around the word in the string
				incorrectwordcount += 1
			

			elif option == 3: #This will add the word to the dictionary and also the list of english words so it does not get flagged again during the loop

				f = open("EnglishWords.txt", "a")
				f.write("\n" + word) #Adds the word to the end of the dictionary
				f.close()
				wordslist.append(word)#Also updates the list we are currently checking against
				addDictionary += 1
			

			elif option == 4: #This will suggest a word to replace the mispelt word and gives the user and option to accept or reject the word

				suggestionRatio = float(0)

				#Loops through the list of english words and compares it with the mispelt word
				for x in wordslist: 
					test = SequenceMatcher(None, word, x).ratio()

					if test >= suggestionRatio: #This replaces the suggestion everytime a word with a better ratio is found

						suggestionRatio = test
						suggestion = x

				print("\nSuggestion: " + suggestion)
				time.sleep(0.5)

				print("\n 1. Use suggestion"
					"\n 2. Reject suggestion\n\n")
				time.sleep(0.5)

				option = options({1, 2})

				if option == 1: #Replace the word with the suggestion

					string = string.replace(word, suggestion, 1)
					correctwordcount += 1
					suggestionCount += 1

				else: #Mark as incorrect, with the question marks

					string = string.replace(word, "?" + word + "?", 1)
					incorrectwordcount += 1

			print("\n") #Keeps the checking line on the same line of the terminal by repositioning it.

		else: 

			sys.stdout.write('\x1b[1A'+'\x1b[2K')
			print("Checking: " + word) #Shows the checked word, this should always output a word which is correctly spelt

			correctwordcount += 1

		totalwordcount += 1 

	summary = ("Summary:" + 
		"\nDate and time of spellcheck: " + starttime.strftime("D%d-M%m-Y%Y H%H:M%M:S%S") +
		"\nSeconds elapsed during spellcheck: " + str(round((time.perf_counter() - startcounter),1)) + "s" + 
		"\nTotal number of words: " + str(totalwordcount) + 
		"\nCorrectly spelt words: " + str(correctwordcount) + 
		"\nIncorrectly spelt words: " + str(incorrectwordcount) +
		"\nWords added to dictionary: " + str(addDictionary) +
		"\nWords replaced by suggestion: " + str(suggestionCount) + 
		"\n")

	return(string, summary)

initialmenu()