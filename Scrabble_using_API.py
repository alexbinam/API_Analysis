# -*- coding: utf-8 -*-
#Create a game of scrabble

import random
import requests
import itertools

score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}

letters = ["a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "e", "e", "e", "e", "f", "f", "g", "g", "h", "h",
           "i", "i","i", "i", "j", "k", "k", "l", "l", "l", "m", "m", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r",
           "s", "s", "s", "s", "t", "t", "t", "t", "u", "u", "u", "v", "w", "x", "y", "z"]

def rand_letters(number):
    return [letters[i] for i in sorted(random.sample(range(len(letters)), number))]

def scrabble_score(word):
    for i in word:
        i = i.lower()
    total = 0
    for letter in word: #looping through each letter in the word
        for leter in score: #score is in global scope and therefore can be called
            if letter == leter: #need to compare both the letter in the word to the letter in the scoreboard
                total = total + score[leter] #indexing the scoreboard and adding to running total
    return total

def check_in_list(word, lst):
    in_list = False
    for let in word:
        if let in lst:
            lst.remove(let)
            in_list = True
        elif let not in lst:
            return False
        
    return in_list

#using Oxford API Call
def check_if_word(word):
    app_id = '21eaf678'
    app_key = '73741ffaf2bbcd50b71fdd99905a2b32'
    language = 'en'
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    try:    
        r.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        return False

#check to see if letter combo can give me a word
        
def letter_combo_check(lst):
    new_lists = []
    for i in range(1, len(lst)+1):
       new_lists.append( list(''.join(p) for p in itertools.permutations(lst, i)))
    for item in new_lists:
        for word in item:
            if check_if_word(word) == True:
                is_valid = True
                return is_valid
            else:
                is_valid = False


num = 7
letter_list = rand_letters(num)
while letter_combo_check(letter_list) == False:
    letter_list = rand_letters(num)

print(letter_list)
new_list = letter_list[:]
wrd = input("Enter a word: ")
while check_in_list(wrd, letter_list) == False or check_if_word(wrd) == False:
    print("You didn't use the letters given or it wasn't a word. Try again.")
    letter_list = new_list[:]
    print(letter_list)
    wrd = input("Enter a word: ")
else:
    print("This is your score:", scrabble_score(wrd))




