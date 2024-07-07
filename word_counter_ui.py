import streamlit as st
import re
import math

# Define the set of stop words
STOP_WORDS = set([
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f",
    "g", "h", "i", "j", "&", "am", "an", "and", "are", "aren't", "as", "at",
    "be", "but", "by", "can", "cannot", "cant", "can't", "does", "doesn't",
    "doing", "done", "don't", "did", "didn't", "do", "etc", "ex", "for", "from",
    "got", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he",
    "he'd", "he'll", "her", "hers", "herself", "he's", "him", "himself", "his",
    "i'd", "if", "i'll", "i'm", "in", "into", "is", "isn't", "it", "it'd",
    "it'll", "its", "it's", "itself", "i've", "me", "mr", "mrs", "my", "myself",
    "no", "not", "of", "off", "oh", "ok", "okay", "on", "or", "our", "ours",
    "ourselves", "out", "per", "said", "she", "she'd", "she'll", "she's", "so",
    "than", "that", "that'll", "thats", "that's", "that've", "the", "their",
    "theirs", "them", "themselves", "then", "there", "there'd", "there'll",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "to", "too", "up", "us", "use", "used", "uses", "was",
    "wasn't", "way", "we", "we'd", "well", "we'll", "went", "were", "we're",
    "weren't", "we've", "what", "what's", "where", "where's", "which", "who",
    "who'd", "who'll", "who's", "whose", "why", "will", "with", "won't", "would",
    "wouldn't", "yes", "yet", "you", "you'd", "you'll", "your", "you're",
    "yours", "yourself", "yourselves", "you've"
])

WHITE_LIST = set(['U.S.A.', 'U.S.'])

class WordCountPro:
    def __init__(self, text, simple_words):
        self.text = text
        self.simple_words = simple_words
        self.sentence_count = self.count_sentences(text)
        self.word_count = self.count_words(text)
        self.characters_count = self.count_characters(text)

    def count_sentences(self, text):
        sentences = re.findall(r'[^.!?]*[.!?]', text)
        return len(sentences)

    def count_words(self, text):
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def count_characters(self, text):
        return len(text)

    def get_reading_level(self):
        index = self.get_index()
        if index > 10:
            return 'College Graduate'
        elif index > 9:
            return 'College'
        elif index > 8:
            return '11-12th Grade'
        elif index > 7:
            return '9-10th Grade'
        elif index > 6:
            return '7-8th Grade'
        elif index > 5:
            return '5-6th Grade'
        else:
            return '< 4th Grade'

    def get_index(self):
        difficult_words = self.get_difficult_words()
        word_list = self.get_word_list()
        if word_list:
            dale_chall_index = 0.1579 * (100.0 * len(difficult_words) / len(word_list)) + 0.0496 * (len(word_list) / self.sentence_count)
            if len(difficult_words) / len(word_list) > 0.05:
                dale_chall_index += 3.6365
            return round(dale_chall_index, 1)
        return 0

    def get_word_list(self):
        words = re.sub(r'\d', '', self.text)
        words = re.sub(r"['-]", '', words)
        words = words.lower().split()
        return words

    def get_difficult_words(self):
        word_list = self.get_word_list()
        return [word for word in word_list if word not in self.simple_words]

    def reading_time(self):
        words_per_minute = 275
        duration = self.word_count / words_per_minute
        if duration < 1:
            return f"{math.ceil(duration * 60)} sec"
        elif duration < 60:
            minutes = int(duration)
            seconds = round((duration % 1) * 60)
            return f"{minutes} min {seconds} sec"
        else:
            hours = int(duration // 60)
            minutes = round((duration % 60))
            return f"{hours} hr {minutes} min"

    def speaking_time(self):
        words_per_minute = 180
        duration = self.word_count / words_per_minute
        if duration < 1:
            return f"{math.ceil(duration * 60)} sec"
        elif duration < 60:
            minutes = int(duration)
            seconds = round((duration % 1) * 60)
            return f"{minutes} min {seconds} sec"
        else:
            hours = int(duration // 60)
            minutes = round((duration % 60))
            return f"{hours} hr {minutes} min"

    def count_paragraphs(self):
        paragraphs = re.findall(r'\n\n|\n', self.text)
        return len(paragraphs) + 1

# Streamlit application starts here
st.title("Text Analysis Tool")

# Text input area
st.write("Enter your text below:")
text_input = st.text_area("Text to analyze", height=200)

# Simple words input area
st.write("Enter simple words separated by commas:")
simple_words_input = st.text_input("Simple words")

# Button to trigger the analysis
if st.button("Analyze Text"):
    # Process simple words input
    simple_words = {word.strip(): 1 for word in simple_words_input.split(',')}
    
    # Create an instance of WordCountPro
    word_counter = WordCountPro(text_input, simple_words)
    
    # Display the analysis results
    st.write(f"**Paragraphs Count:** {word_counter.count_paragraphs()}")
    st.write(f"**Reading Level:** {word_counter.get_reading_level()}")
    st.write(f"**Reading Time:** {word_counter.reading_time()}")
    st.write(f"**Speaking Time:** {word_counter.speaking_time()}")
    st.write(f"**Sentence Count:** {word_counter.sentence_count}")
    st.write(f"**Word Count:** {word_counter.word_count}")
    st.write(f"**Characters Count:** {word_counter.characters_count}")
