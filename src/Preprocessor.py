from typing import List
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

class Preprocessor:
    def __init__(self, stop_path="assets/stop-words.txt"):
        self.processed = []
        with open(stop_path, "r") as f:
            self.stop_words = [w.strip("\n") for w in f.readlines()]

    def strip_punctuation(self):
        """
            Splits the whole string into words and removes all punctuation using regexp
        """
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        self.processed = tokenizer.tokenize(self.raw_text)

    def to_lower(self):
        """
            Do I need to explain this?
        """
        self.processed = [w.lower() for w in self.processed]

    def remove_stop_words(self):
        """
            Removes all words, that match anything from nltk.stopwords or stop-words.txt
        """
        self.processed = [
            word for word in self.processed
            if word not in self.stop_words
            if word not in stopwords.words("english")
        ]

    def lemmatize_verbs(self):
        """
            Replaces all verbs in the list with it's infinitive using wordnet
        """
        pos_tagged = nltk.pos_tag(self.processed)
        self.processed = [
            pt[0] if pt[1] != "VB" else WordNetLemmatizer().lemmatize(pt[0]) for pt in pos_tagged
        ]

    def stem(self):
        """
            Removes needless suffixes and preffixes from the words leaving the stem
        """
        ps = PorterStemmer()
        self.processed = [
            ps.stem(word) for word in self.processed
        ]

    def process(self, raw_text: str) -> List:
        """
            Returns a list of words
        """
        self.raw_text = raw_text
        self.strip_punctuation()
        self.to_lower()
        self.remove_stop_words()
        self.stem()
        self.lemmatize_verbs()

        return self.processed


if __name__ == "__main__":
    # To run this you will need download some nltk packages

    # nltk.download("punkt")
    # nltk.download("averaged_perceptron_tagger")
    # nltk.download("wordnet")
    # nltk.download("stopwords")

    p = Preprocessor()
    with open("/assets/articles/Why we fight about Iran", 'r') as f:
        print(p.process(f.read()))
