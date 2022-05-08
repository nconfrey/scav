# Item 33 Bumblewords

(33) Like the New York Times Spelling Bee, but wish it had a hard mode? Then you’ll love this Item. It will go live on National Puzzle Day at buzz.pythonanywhere.com. Feel free to use whatever resources
you’d like to complete it, and go fast! `[`10 points for making Queen Bee, 8/5/3 bonus points for 1st 2nd and 3rd to complete it`]` (Em + Nick)

### The Challenge

Like NYT "Spelling Bee" game, except you can't see the letters!

Here is the NYT version:

![an animated gif displaying how the original "spelling bee" is played](https://compote.slate.com/images/88f480e9-692c-43bf-802b-98aed8da18e6.gif?width=1200&rect=580x387&offset=0x0)

Here is the Scav 2022 Item 33 version:

<img src="./img/blank_bumblewords.png?raw=true" alt="item 33s version of 'spelling bee'" width="200" />


😱😱😱

### The Solve

First, a clarification from the judges:

> The word list was taken from the 100k list from
https://www.norvig.com/ngrams/ and then I took the top 25k of that, so
if a word is/isn't present, that's why. (FYI, this was on the Captain's
Breakfast notes)

1. **Reverse engineer the API** using google chrome devtools network by getting lucky on a few words. Once we had the response for a valid word, we could start brute forcing.
2. **Get a visual**. The frontend maps each hexagon as a number from 1-7. Click each in a known pattern, submit the request, then check devtools to understand the mapping from the request. Here's what we've got: <img src="./img/bumblewords_with_numbers.png?raw=true" alt="honeycombs with numbers" width="200" />
3. **Brute force all 4 letter (minimum length) words**! See [bumblewords.js](./bumblewords.js).
4. **Download the source words** list from https://www.norvig.com/ngrams/count_1w100k.txt. Only consider the first 25k lines. Process it so it's clean using [process_word_file.py](./process_word_file.py).
5. **Next, generate all possible 7 letter permutations.** `26!/(26-7)! = 3315312000`. That's a lot. How can we reduce the search space?
6. **Reduce the search space** by reviewing some of the found words (see [foundwords.js](./foundwords.js)) manually and look for patterns! What do you see? I saw this one: `[ 3, 5, 5, 5 ], // WHAT??? triple letter?`. Based on the possible words, letter 5 could only be "e", "i", or "m". Letter 3 could only be "i", "w", "s", or "h". So now we only have `26!/(26-5)! * 3 * 4 = 118404000`. Is my approach 100% optimized? No. But close enough. We have a `96.4%` decrease in search space to work with now :)
7. **Reveal the honeycomb letters** ([reveal_honeycomb_letters.py](./reveal_honeycomb_letters.py)) by computing all 118404000 permutations of 7 unique letters, then iterating over the 40 known combinations. Map the numbers to letters to form "words," then check to see if those words are contained in the set of source words (use a set object for constant time lookup). If all 40 words are from the source list, you've found a candidate for mapping the bumble tiles to letters. <img src="./img/bumblewords_with_letters.png?raw=true" alt="found the honeycomb letters" width="200" />
8. **Have some fun**! Play the game the normal way for a little bit. Come up with some 5 letter words and see if the generated mapping was correct. Ask your teammates to join in. Laugh a little 😁
9. **Find valid words** and map them back to numbers ([find_all_valid_words.py](./find_all_valid_words.py)). There are 25k words. For each word, see if the letters are a subset of the 7 honeycomb letters. If so, make sure the required letter (in this case, "e") is also in the word. This is a valid word.
10. **Map valid words back to numbers**. For example "rmipent" has a 1-indexed positional mapping `r->1, m->2, i->3, p->4, e->5, n->6, t->7`.
11. **Automate the remaining valid words via server fetches**. I reused [bumblewords.js](./bumblewords.js).
12. **`data["victory"] == true`** --> You are the Queenbee.


### The Celebration

I obtained Queenbee status on March 6 2014 (aka Thursday, May 5, 2022 @ 4:15pm) 👑🐝🎉 -- the 3rd challenger to complete.

<img src="./img/bumblewords_queenbee.jpg?raw=true" alt="queen bee evidence" width="200" />
