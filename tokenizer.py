import spacy
import pandas as pd
nlp = spacy.load("hr_core_news_sm")

data_frame = pd.read_excel("korpus_anotacija_final.xlsx")
second_column = data_frame.iloc[:, 1].astype(str).values.tolist()
second_column_string = " ".join(second_column)

print(len(second_column_string))

doc = nlp(second_column_string)

token_count = len(doc)

print("Token count: ", token_count)

out = []

seen = set()

for word in doc:
    if word.text not in seen:
        out.append(word)
    seen.add(word.text)

print(f"Unique tokens: {len(out)}")