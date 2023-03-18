import random
import nltk
from nltk.corpus import cmudict
from g2p_en import G2p

nltk.download('cmudict')
pron_dict = cmudict.dict()
g2p = G2p()

def get_phonemes(word):
    word = word.lower()
    if word in pron_dict:
        return pron_dict[word][0]
    return []

def find_syllable_break(phonemes):
    vowels = ['A', 'E', 'I', 'O', 'U']
    syllable_breaks = [i for i, phoneme in enumerate(phonemes) if any(vowel in phoneme for vowel in vowels)]

    if syllable_breaks:
        return random.choice(syllable_breaks)
    return None

def merge_words(word1, word2):
    phonemes1 = get_phonemes(word1)
    phonemes2 = get_phonemes(word2)

    if not phonemes1 or not phonemes2:
        return "Unable to merge words"

    break_point1 = find_syllable_break(phonemes1)
    break_point2 = find_syllable_break(phonemes2)

    if break_point1 is None or break_point2 is None:
        return "Unable to merge words"

    merged_phonemes = phonemes1[:break_point1] + phonemes2[break_point2:]
    merged_word = g2p(merged_phonemes)
    return ''.join(merged_word).capitalize()


word1 = "Shark"
word2 = "Goat"
merged_word = merge_words(word1, word2)
print(merged_word)
