"""
All 4 letter words are already found, so only words of len >= 5
Word must include the letter "e"
Word must be in words_clean.txt
"""

possible_letters = "rmipent"
required_letter = "e"

def get_words_list():
    words = []
    with open("words_clean.txt", "r") as f:
        words = f.readlines()
    stripped_words = []
    for word in words:
        stripped_words.append(word.split("\n")[0])
    return stripped_words

def get_longest_word_length():
    words = []
    longest = 0
    with open("words_clean.txt", "r") as f:
        words = f.readlines()
    stripped_words = []
    for word in words:
        if len(word.split("\n")[0]) > longest:
            longest = len(word.split("\n")[0])
    return longest


def get_valid_words(min_len):
    valid_words = []
    words_list = get_words_list()
    valid_letters_set = set(possible_letters)

    for word in words_list:
        if len(word) < min_len:
            continue
        word_letters_set = set(word)
        if required_letter in word_letters_set and word_letters_set.issubset(valid_letters_set):
            valid_words.append(word)
    return valid_words

def convert_valid_words_to_numbers_arrays(min_len):
    numbers_arrays = []
    letters_to_numbers_map = {}
    for idx, val in enumerate(possible_letters):
        letters_to_numbers_map[val] = idx + 1

    valid_words = get_valid_words(min_len)
    for word in valid_words:
        numbers_arrays.append(
            map(lambda letter: letters_to_numbers_map[letter], word))
    return numbers_arrays

if __name__ == "__main__":
    print(get_longest_word_length())
    valid_numbers_arrays = convert_valid_words_to_numbers_arrays(5)
    print("".join(str(valid_numbers_arrays)))


"""
Remaining valid words (as output from get_valid_words()):

"internet",
"enter",
"printer",
"peter",
"entire",
"prime",
"permit",
"retirement",
"meter",
"empire",
"premier",
"inner",
"inter",
"eminem",
"intent",
"titten",
"pierre",
"pepper",
"interim",
"timer",
"premiere",
"merit",
"reprint",
"petite",
"interpret",
"primer",
"terrier",
"trent",
"interpreter",
"intern",
"retire",
"pertinent",
"piper",
"ripper",
"terri",
"preteen",
"irene",
"renee",
"perimeter",
"metre",
"eminent",
"ernie",
"miner",
"printprinter",
"entre",
"petit",
"imminent",
"intermittent",
"tempe",
"terre",
"temper",
"minnie",
"renter",
"merritt",
"trimmer",
"nineteen",
"etienne",
"ritter",
"meier",
"peppermint",
"permittee",
"remit"
"""