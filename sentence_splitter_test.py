# Somajo sentence Splitter
from somajo import SoMaJo

tokenizer = SoMaJo("de_CMC", split_camel_case=False)

# note that paragraphs are allowed to contain newlines


#paragraphs = ["der beste Betreuer?\n-- ProfSmith! : )",
#              "Was machst du morgen Abend?! Lust auf Film?;-)"]

#sentences = tokenizer.tokenize_text(paragraphs)
#for sentence in sentences:
#    for token in sentence:
#        print("{}\t{}\t{}".format(token.text, token.token_class, token.extra_info))
#    print()

sentences = tokenizer.tokenize_text_file("C:/Users/karam/PycharmProjects/skillExtraction/metajob/jobPost_1.txt", paragraph_separator="single_newlines")

#for i,sentence in enumerate(sentences):
#    print(i)
#    for token in sentence:
#        print(token.text)
 #   print()

with open("C:/Users/karam/PycharmProjects/skillExtraction/SentenceSplitterComparison.txt",'a') as f:
    f.write("SoMaJo")
    for i,sentence in enumerate(sentences):
        f.write(str(i)+"\n")
        for token in sentence:
            f.write(token.text+"\n")
    f.write("\n"+"="*30)



#=======================================================================================
# wtp sentence splitter

from pathlib import Path
from itertools import chain
from cleantext import clean
from tqdm import tqdm
from wtpsplit import WtP
from lingua import Language, LanguageDetectorBuilder
# from numba import jit,cuda,njit,vectorize,uint32,f8,uint8



def preprocess_text(text: str) -> str:
	lang = "de"
	text = clean(text,
	             fix_unicode=True,  # fix various unicode errors
	             to_ascii=True,  # transliterate to closest ASCII representation
	             lower=True,  # lowercase text
	             no_line_breaks=False,  # fully strip line breaks as opposed to only normalizing them
	             no_urls=True,  # replace all URLs with a special token
	             no_emails=True,  # replace all email addresses with a special token
	             no_phone_numbers=True,  # replace all phone numbers with a special token
	             no_numbers=False,  # replace all numbers with a special token
	             no_digits=False,  # replace all digits with a special token
	             no_currency_symbols=False,  # replace all currency symbols with a special token
	             no_punct=False,  # remove punctuations
	             replace_with_punct="",  # instead of removing punctuations you may replace them
	             replace_with_url="<URL>",
	             replace_with_email="<EMAIL>",
	             replace_with_phone_number="<PHONE>",
	             replace_with_number="<NUMBER>",
	             replace_with_digit="0",
	             replace_with_currency_symbol="<CUR>",
	             lang=lang  # set to 'de' for German special handling
	             )

	return text

def sentenceExtractor():
    wtp = WtP("wtp-canine-s-12l")  # "wtp-bert-mini")
    wtp.half().to("cuda")
    languages = [Language.GERMAN, Language.ENGLISH]
    dir = "C:/Users/karam/PycharmProjects/skillExtraction/metajob/jobPost_1.txt"
    with open(dir,'r', encoding="utf8") as f:
        text_lines = list(filter(None, (l.strip() for l in f.readlines())))

        # text_lines = list(filter(None, (preprocess_text(l) for l in text_lines)))
        sents = list(wtp.split(text_lines, lang_code="de", style="ud"))

    with open("C:/Users/karam/PycharmProjects/skillExtraction/SentenceSplitterComparison.txt",'w+') as f:
        f.write("wtpsplit"+"\n\n")
        for i,sentence in enumerate(chain.from_iterable(sents)):
            f.write(str(i)+"\n")
            f.write(sentence+"\n")
        f.write("\n"+"="*20)


if __name__ == "__main__" :
	sentenceExtractor()

#==============================================================
# Spacy sentence splitter
import spacy
from spacy.lang.de.examples import sentences
nlp = spacy.load("de_core_news_sm")
dir = "C:/Users/karam/PycharmProjects/skillExtraction/metajob/jobPost_1.txt"
with open(dir,'r',encoding="utf-8") as f:
    doc = f.read()
doc = nlp(doc)
for i,sent in enumerate(doc.sents):
    print(str(i)+"\n")
    print(sent.text)
    for token in sent:
        print(token.text, token.pos_, token.dep_)
    print('----')

#==============================================================
# NLTK sentence splitter
from nltk.tokenize import sent_tokenize, word_tokenize
from itertools import chain
import nltk
nltk.download("punkt")

dir = "C:/Users/karam/PycharmProjects/skillExtraction/metajob/jobPost_1.txt"
print("\n nltk Sentence Tokenizer \n")
with open(dir,'r',encoding="utf-8") as f:
    doc = f.read()
with open("C:/Users/karam/PycharmProjects/skillExtraction/SentenceSplitterComparison.txt",'a') as f:

    for i,sent in enumerate(sent_tokenize(doc)):
        print(str(i)+"\n")
        print(sent+"\n")
    print('='*30)
