import sys, re
from HashTable import HashTable

def check_word(hashTable, text):
    """ given a string, return string of action: delete or get frequency of. """
    
    if text[0] == "-":
        text = text[1:]
        return '"{}" has been deleted.'.format(text) if hashTable.delete(text) else 'Cannot delete. "{}" does not appear.'.format(text)
    else:
        num_occ = hashTable.get(text)
        return '"{}" does not appear.'.format(text) if num_occ == None else '"{}" appears {} time(s).'.format(text, num_occ)

def fill_from_string(hashTable, text):
    """ fills a given hashTable with a given string, text """

    split_up_test = re.split(r"[^\w{w}']+", text)

    for s in split_up_test:
        curr_string = remove_39(s.lower())
        if curr_string == None:
            continue
        elif hashTable.contains(curr_string):
            old_val = hashTable.get(curr_string) + 1
            hashTable.put(curr_string, old_val)
            pass
        else:
            hashTable.put(curr_string, 1)


def remove_39(string):
    """ Removes trailing and starting 's. Returns the modified string """

    if(string == None or len(string) == 0):
        return None
    
    if(len(string) == 1 ):
        return None if string[0] == 39 else string 
    
    x = 0
    while(x < len(string) and string[x] == "'"):
        x += 1

    string = string[x:]

    x = len(string) - 1
    while(x >= 0 and string[x] == "'"):
        x -= 1

    return string[:x + 1] if x != 0 else None

def main(argv):
    """ This program counts the frequency of words froma given file

    This program uses a hashTable, implemented via Linearprobing. 
    After reading from a file, given from the command line,
    the user can either:
        - get the frequency of a word by just entering the word
        - deleting a word by appending a - to the front of the word they
          would like to delete. e.g. -bye
    to exit, just press enter.

    Ana-Lea N; CSCI 361; 11/22/2020; For Extra Credit
    """
    #check arguments
    if len(argv) == 0:
        print('No arguements found. Exiting...')
        sys.exit(0)
    elif len(argv) > 1:
        print('Multiple arguments found. Running WordFreq3 on the first argument, "{}", entered.'.format(argv[0]))

    read_data = ""
    # file check
    try:
        f = open(argv[0], 'r')
        read_data = f.read()
        f.close()
    except FileNotFoundError:
        print(f'File "{argv[0]}" was not found. Exiting...')
        sys.exit(-1)
    except IOError:
        print(f'File "{argv[0]}" does not have read permission. Exiting...')
        sys.exit(-1)
    except Exception:
        print("Please check your input. Exiting...")
        sys.exit(-1)
    
    word_counter = HashTable()

    #read file, init hashTabe
    fill_from_string(word_counter, read_data)

    #Welcolme Messages
    print(f"This text contains {word_counter.size()} distinct words.")
    user_said = input("Please enter a word to get its frequency, or hit enter to leave.\n").strip().lower()

    #scan user input
    while user_said != "":
        user_said = input(f"{check_word(word_counter, user_said)}\n").strip().lower()

    #goodbye
    print("Goodbye, have a nice day.")
    return

if __name__ == "__main__":
    main(sys.argv[1:])