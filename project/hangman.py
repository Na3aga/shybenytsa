# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import re
import string

WORDLIST_FILENAME = "words.txt"
guesses_left = 0
letters_guessed = []
secret_word = ""



def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    true_letters = 0 #number of letters guessed
    for letter in letters_guessed:
       for i in secret_word:
           if i == letter:
               true_letters+=1

    if true_letters==len(secret_word): #compares len of word with number of letters guessed
        return True
    else:
        return False



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = "_" * len(secret_word)  # fully not guessed word
    for letter in letters_guessed:
        for i in range(len(secret_word)):
            if secret_word[i] == letter:
                result = result[:i] + letter + result[i + 1:] #show letter number i if it is guessed

    return result



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    result = string.ascii_lowercase
    for guessed in letters_guessed:
        result = result.replace(guessed,"")
    return result


def is_correct_guess(letter,letters_guessed):
    global secret_word
    global guesses_left
    print(" ")
    if len(letter)>1:
        print("-please enter only one letter")
        guesses_left = guesses_left - 1
        return False
    if not re.match(r"[a-z]{1}",letter):
        print("-please enter a lowcase letter")
        guesses_left = guesses_left - 1
        return False

    avaliable_letters = get_available_letters(letters_guessed)
    for i in avaliable_letters:
        if i == letter: return is_right_guess(letter,secret_word)
    print("-You have already used this letter")
    guesses_left -= 1
    return False



def is_right_guess(letter, secret_word):
    global guesses_left
    global letters_guessed
    for i in secret_word:
        if i == letter:
            print(" Good guess: ",end="")
            return True
    print("Ooops!It is not in my word... ",end="")
    guesses_left -= 1
    return True

def get_new_guess(guesses_left,secret_word,letters_guessed):
    print(" You have "+str(guesses_left)+" guesses left .")
    print(" Avaliable letters: "+get_available_letters(letters_guessed))
    letter = input(" Enter your guess(one letter): ")
    if is_correct_guess(letter,letters_guessed):
        letters_guessed.append(letter)
        print(get_guessed_word(secret_word,letters_guessed))
        return letters_guessed
    print("Ooops!It is not not correct: "+get_guessed_word(secret_word,letters_guessed))
    return letters_guessed



def hangman():
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    global secret_word
    global guesses_left
    global letters_guessed
    length = len(secret_word)
    guesses_left = 6
    letters_guessed=[]
    print("\n\n Welcome to the game Hangman!!!\n I am thinking of a word that is "+str(length)+" letters long.\n "+"-"*47)
    while(guesses_left>=1):
        old = get_guessed_word(secret_word,letters_guessed)
        letters_guessed = get_new_guess(guesses_left,secret_word,letters_guessed)
        new = get_guessed_word(secret_word,letters_guessed)
        if is_word_guessed(secret_word, letters_guessed):
            print("\n\n\n And you won!!! The word is " + secret_word)
            guesses_left == 0
            return
    print("\n Hangman game stopped!!!")
    if is_word_guessed(secret_word,letters_guessed):
        print(" And you won!!! The word is " + secret_word)
    else:
        print(" You have used all your chances")
        print(" And you lost ... The word was - " + secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    result = False
    if len(my_word)==len(other_word):
        for i in range(len(my_word)):
            if my_word[i]==other_word[i]:
                result = True
            if my_word[i] != "_" and my_word[i] != other_word[i]:
                    return False
    return result

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    print(" This is all words that are possible answers: ")

    for other_word in wordlist:
        if match_with_gaps(my_word,other_word):
            print(other_word,end=", ")
    print("\n")
    return None



def hangman_with_hints():
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    global secret_word
    global guesses_left
    global letters_guessed
    length = len(secret_word)
    guesses_left = 6
    letters_guessed = []
    print("\n\n Welcome to the game Hangman!!!\n I am thinking of a word that is " + str(
        length) + " letters long.\n " + "-" * 47)
    while (guesses_left >= 1):
        old = get_guessed_word(secret_word, letters_guessed)
        letters_guessed = get_new_guess(guesses_left, secret_word, letters_guessed)
        new = get_guessed_word(secret_word, letters_guessed)
        if is_word_guessed(secret_word, letters_guessed):
            print(" And you won!!! The word is " + secret_word)
            guesses_left == 0
            return
        show_possible_matches(get_guessed_word(secret_word,letters_guessed))

    print("\n You have ran out of all your guesses.")
    if is_word_guessed(secret_word, letters_guessed):
        print(" And you won!!! The word is "+secret_word)
    else:
        print("And you lost ... The word was - "+secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # pass
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    secret_word = choose_word(wordlist)
    # hangman(secret_word)
    hangman_with_hints()
