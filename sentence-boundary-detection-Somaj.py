from pathlib import Path
from itertools import chain
from cleantext import clean
from tqdm import tqdm
from wtpsplit import WtP
from lingua import Language, LanguageDetectorBuilder
# from numba import jit,cuda,njit,vectorize,uint32,f8,uint8
from somajo import SoMaJo

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
	tokenizer = SoMaJo("de_CMC", split_camel_case=False)
	languages = [Language.GERMAN, Language.ENGLISH]
	detector = LanguageDetectorBuilder.from_languages(*languages).with_preloaded_language_models().build()


	for file in tqdm(list(Path("C:/Users/karam/PycharmProjects/skillExtraction/metajob").glob("*.txt"))):
		if not file.with_suffix(".sents").exists():
			with file.open("rt", encoding="utf8") as f:
				text_lines = list(filter(None, (l.strip() for l in f.readlines())))

				if detector.compute_language_confidence(" ".join(text_lines), Language.GERMAN) < 0.8:
					print("Ignore non-german file: ", file.name)
					continue

				f.seek(0)
				sents = tokenizer.tokenize_text_file(f, paragraph_separator="single_newlines")

				with file.with_suffix(".sents").open("wt", encoding="utf8") as rf:
					for sentence in sents:
						rf.write("\n")
						for token in sentence:
							rf.write(token.text)

					print(f"{file.name}")


if __name__ == "__main__" :
	sentenceExtractor()