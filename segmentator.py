import spacy
import csv
import openpyxl

nlp = spacy.load('hr_core_news_sm')
datoteka = "C:\\Users\\milab\\OneDrive - FFUNIZG\\FFZG\\IV\\Obrada prirodnog jezika\\Projekt\\osvrti_opj.tsv"

def extract_first_column(tsv_file):
    first_column = []
    with open(tsv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            if row:
                row = row[0].strip("[]")
                first_column.append(row)
    return first_column

recenzije = extract_first_column(datoteka)

recenice = []

for row in recenzije:
    doc = nlp(row)
    rec_recenice = [sent.text for sent in doc.sents]
    for recenica in rec_recenice:
        recenice.append(recenica)
    recenice.append("\n")

workbook = openpyxl.load_workbook("korpus_anotacija_final.xlsx")
worksheet = workbook.active

column = "A"
for i, value in enumerate(recenice, start=1):
    cell=f"{column}{i}"
    worksheet[cell] = value

workbook.save("korpus_anotacija_final.xlsx")