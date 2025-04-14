# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Abdullah Saadi
# Collaborators : None
# Time spent    : 72 hours (approx)

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand_cpy length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    #convert the string to lowercase letters only
    word = word.lower()
    
    first_component = 0
    for letter in word:
        first_component += SCRABBLE_LETTER_VALUES[letter]
    
    second_component = 7 * len(word) - 3 * (n - len(word))
    if(second_component < 1):
        second_component = 1
    
    score = first_component * second_component
    return score
    

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand_cpy):
    """
    Displays the letters currently in the hand_cpy.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand_cpy: dictionary (string -> int)
    """
    
    for letter in hand_cpy.keys():
        for j in range(hand_cpy[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
        #wildcard '*'
        hand['*'] = 1
    
    for i in range(num_vowels + 1, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand_cpy by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #convert word to lowercase
    word = word.lower()
    # make a copy/clone of current hand 
    new_hand = hand.copy()
    # or new_hand = dict(hand)
    
    for letter in word:
        if letter in hand.keys():           #Letters in word that don't appear in hand would be ignored.
            if new_hand[letter] > 0:     #If letter appears more frequently in word than in hand then excessive occurances are ignored.
                new_hand[letter] -= 1
        
    return new_hand
    

#utility function
def compare_with_wildcard(wild_word, match_word):
    if(len(wild_word) != len(match_word)):
        return False
    for wild_letter, match_letter in zip(wild_word, match_word):
        if(wild_letter == "*" and match_letter not in "aeiou"):
            return False
        elif(wild_letter != match_letter):
            return False
    
    return True

#    
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand_cpy. Otherwise, returns False.
    Does not mutate hand_cpy or word_list.
   
    word: string
    hand_cpy: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower();
    
    #verify the word is made from characters from the current hand_cpy
    hand_cpy = hand.copy()
    for letter in word:
        if hand_cpy.get(letter,0) > 0:
            hand_cpy[letter] -= 1
        else:
            #print("False because not comprised of letters of letters in the hand_cpy")
            return False
    
    #returns the index at which wildcard occurs
    wildcard_idx = word.find('*')
    
    #if no wildcard in the hand
    if(wildcard_idx == -1):
        for list_word in word_list:
            if(list_word == word):
                #print("Word match without wildcard" + list_word)
                return True
        #the word didn't match with any word in the word_list
        return False
    
    #verfiy presence in word_list       
    for list_word in word_list:                                 #iterate over all words in word_list
        if( compare_with_wildcard(word,list_word)):                 
            return True
        else:
            continue                                            #if current list word doesn't match word, move to the next word in the list 
            
    #print("False because no match with words in word_list")
    return False
#
# Problem #5: Playing a hand_cpy
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand_cpy.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    hand_len = 0
    for letter in hand.keys():
        if(hand[letter] != 0):
            hand_len += 1;

    return hand_len
    
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function

#
# Problem #6: Playing a game
#
    hand_score = 0
 
    hand_cpy = dict(hand)       #all changes are made to a clone of hand dictionary. The orignal hand remains same
    hand_length = calculate_handlen(hand_cpy) 
    while(True):
        print("Current hand: ")
        display_hand(hand_cpy)
        word = input("Enter word, or \"!!\" to indicate that you are finished: ")
        
        if(word == "!!"):          #user decide to quit before hand
            break;
        
        if(is_valid_word(word, hand_cpy, word_list)):
            word_score = get_word_score(word, hand_length)
            hand_score += word_score
            print("\"" + word + "\"" + " earned ", word_score , "points")
            print("Total: ", hand_score , "points")
        else:
            print("This is not a valid word. Please chose a valid word.")
            
        hand_cpy = update_hand(hand_cpy,word)
        hand_length = calculate_handlen(hand_cpy) 
        if(hand_length == 0):
            print("Ran out of letters. ")
            break;
        print();
        print();
        
    print("Total score for this hand_cpy: " , hand_score , "points")
    return hand_score

#
# procedure you will use to substitute a letter in a hand_cpy
#

def substitute_hand(hand, old_letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    new_letter = random.choice(VOWELS + CONSONANTS)
    
    #make sure the letter doesn't already exisist in the hand
    while(new_letter in hand.keys()):
        new_letter = random.choice(VOWELS + CONSONANTS)
        
    old_letter_count = hand.get(old_letter, 0)
    if(old_letter_count > 0):
        #add new letter to the hand
        hand[new_letter] = old_letter_count;
        #remove occurances of old letter
        del(hand[old_letter])
            
       
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand_cpy into a total score for the 
      entire series
 
    * For each hand_cpy, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand_cpy, ask the user if they would like to replay the hand_cpy.
      If the user inputs 'yes', they will replay the hand_cpy and keep 
      the better of the two scores for that hand_cpy.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand_cpy does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    total_score = 0
    num_hands = int(input("Enter total number of hands: "))
    
    #REPLAY PREVIOUS hand
    replay = False
    while(num_hands > 0):
        if( not replay):
            print("New hand will be dealt...")
            hand = deal_hand(HAND_SIZE)
        print("Current hand: ")
        display_hand(hand)
        
        print()
        #subsitition if asked to:
        substitute_decision = input("Would you like to subsitite a letter? ").lower()
        if(substitute_decision == "yes"):
            subsitited_letter = input("Which letter would you like to replace: ")
            substitute_hand(hand,subsitited_letter)
        
        print()
        total_score += play_hand(hand , word_list)
        
        num_hands -= 1
        print("----------")
        #ask the user if they would like to replay the previous hand, if there is any hand left to play
        if(num_hands > 0):
            replay_decision = input("Would you like to replay the hand? ").lower()
            if(replay_decision == "yes"):
                print("I would replay the hand for next term.")
                replay = True
            else:
                replay = False
        
    
    print("Total score over all hands: ", total_score)
    
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    
   
    
    