import random
import nltk
from nltk.corpus import cmudict
from g2p_en import G2p

nltk.download('cmudict')
pron_dict = cmudict.dict()

def get_phonemes(word):
    word = word.lower()
    if word in pron_dict:
        return pron_dict[word][0]
    else:
        g2p = G2p()
        phonemes = g2p(word)
        return phonemes

def find_syllable_break(phonemes):
    vowels = ['A', 'E', 'I', 'O', 'U']
    syllable_breaks = [i for i, phoneme in enumerate(phonemes) if any(vowel in phoneme for vowel in vowels)]

    if syllable_breaks:
        return random.choice(syllable_breaks)
    return None

def phonemes_to_graphemes(phonemes):
    phoneme_grapheme = {
        'AA': ['a', 'ah'], 'AE': ['a', 'ae'], 'AH': ['a', 'u', 'uh'], 'AO': ['o', 'aw'], 'AW': ['ow', 'au'], 'AY': ['ay', 'ai', 'ey'],
        'B': ['b'], 'CH': ['ch'], 'D': ['d'], 'DH': ['th'], 'EH': ['e', 'eh'], 'ER': ['er', 'ur', 'ir'],
        'EY': ['ay', 'ai', 'ey'], 'F': ['f'], 'G': ['g'], 'HH': ['h'], 'IH': ['i', 'ih'], 'IY': ['ee', 'ie', 'i'],
        'JH': ['j'], 'K': ['k'], 'L': ['l'], 'M': ['m'], 'N': ['n'], 'NG': ['ng'],
        'OW': ['ow', 'o'], 'OY': ['oy', 'oi'], 'P': ['p'], 'R': ['r'], 'S': ['s'], 'SH': ['sh'],
        'T': ['t'], 'TH': ['th'], 'UH': ['u', 'uh'], 'UW': ['oo', 'u'], 'V': ['v'], 'W': ['w'],
        'Y': ['y'], 'Z': ['z'], 'ZH': ['zh']
    }
    
    phonemes = [phoneme[:-1] if phoneme[-1].isdigit() else phoneme for phoneme in phonemes]
    graphemes = [random.choice(phoneme_grapheme.get(phoneme, [''])) for phoneme in phonemes]
    return ''.join(graphemes)

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
    word = phonemes_to_graphemes(merged_phonemes)
    return word.capitalize()
