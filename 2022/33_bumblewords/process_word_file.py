words_raw = ""
with open("count_1w100k_first_25k.txt", "r") as word_list_file:
    words_raw = word_list_file.readlines()

with open("words_clean.txt", "w+") as f:
    for word in words_raw:
        f.write(word.split("\t")[0].lower())
        f.write("\n")
