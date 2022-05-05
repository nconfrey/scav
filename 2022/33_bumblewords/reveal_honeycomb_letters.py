"""
We used this to reverse engineer the honeycomb from letters

('found a possibility!!:\t', 'rmipent')
all possibilities
['rmipent'] meaning 1->r, 2->m, 3->i, and so on.
"""

# note: all words end with a \n character. Consider that when checking
#       for set membership
def get_words_set():
    words = []
    with open("words_clean.txt", "r") as f:
        words = f.readlines()
    return set(words)

def get_found_words():
    # src foundwords.js via bumblewords.js
    return [
        [ 4, 5, 1, 2 ],
        [ 7, 5, 1, 2 ],
        [ 3, 6, 5, 7 ],
        [ 6, 3, 6, 5 ],
        [ 7, 5, 1, 3 ],
        [ 7, 5, 2, 4 ],
        [ 7, 5, 5, 6 ],
        [ 7, 5, 6, 7 ],
        [ 7, 3, 1, 5 ],
        [ 7, 3, 2, 5 ],
        [ 7, 3, 5, 1 ],
        [ 7, 1, 5, 5 ],
        [ 6, 3, 7, 5 ],
        [ 5, 3, 6, 5 ],
        [ 5, 2, 3, 7 ],
        [ 5, 1, 3, 6 ],
        [ 5, 1, 3, 5 ],
        [ 4, 5, 5, 4 ],
        [ 4, 5, 5, 1 ],
        [ 4, 5, 6, 6 ],
        [ 4, 5, 7, 5 ],
        [ 4, 3, 4, 5 ],
        [ 4, 3, 5, 1 ],
        [ 4, 3, 6, 5 ],
        [ 4, 1, 5, 4 ],
        [ 3, 7, 5, 2 ],
        [ 3, 6, 7, 5 ],
        [ 3, 5, 5, 5 ],
        [ 2, 5, 2, 5 ],
        [ 2, 5, 3, 6 ],
        [ 2, 5, 5, 7 ],
        [ 2, 5, 5, 1 ],
        [ 2, 5, 6, 7 ],
        [ 2, 3, 2, 5 ],
        [ 2, 3, 6, 5 ],
        [ 1, 5, 6, 7 ],
        [ 1, 5, 6, 5 ],
        [ 1, 3, 4, 5 ],
        [ 1, 3, 7, 5 ],
    ]

def get_alphabet_str():
    return "abcdefghijklmnopqrstuvwxyz"

# yep, more globals, sry
words_set = get_words_set()
found_words = get_found_words()
def check_validity_of_letter_mapping(letters):
    tolerance = 6
    for numbers in found_words:
        real_word_arr = []
        for number in numbers:
            real_word_arr.append(letters[number-1])
        word = "".join(real_word_arr)
        if (word+"\n") not in words_set:
            # print("trying word: ", word)
            return False
            # if tolerance:
            #     tolerance -= 1
            # else:
            #     return False

    print("yeet!!:\t", letters)
    return True

def generate_letter_mapping_possibilities(letters, agg):
    if len(letters) == 7:
        if check_validity_of_letter_mapping(letters):
            print("found a possibility!!:\t", letters)
            agg.append(letters)
        return

    if len(letters) == 2:
        generate_letter_mapping_possibilities(letters+"i", agg)
        generate_letter_mapping_possibilities(letters+"w", agg)
        generate_letter_mapping_possibilities(letters+"s", agg)
        # generate_letter_mapping_possibilities(letters+"h", agg)
        return

    if len(letters) == 4:
        # relatively sure letter 5 is "e"
        generate_letter_mapping_possibilities(letters+"e", agg)
        generate_letter_mapping_possibilities(letters+"o", agg)
        # generate_letter_mapping_possibilities(letters+"m", agg)
        return

    for letter in get_alphabet_str():
        if letter not in letters:
            generate_letter_mapping_possibilities(letters+letter, agg)


if __name__ == "__main__":
    possibilities_agg = []
    generate_letter_mapping_possibilities("", possibilities_agg)

    print("all possibilities")
    print(possibilities_agg)

    # print(check_validity_of_letter_mapping("abcdefg"))

