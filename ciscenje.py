import re

dat_r = open("osvrti_opj.txt", "r", encoding = "utf-8")

punctuation_matches = []

for red in dat_r:
    punctuation_pattern = r"[\"#$%&'()*+,\-./:;<=>?@[\]\\\^_`{|}~]"
    punctuation_matches = re.findall(punctuation_pattern, red)

frek_dist = []

for znak in punctuation_matches:
    if znak not in frek_dist:
        frek_dist.append(znak)

print(frek_dist) # OUTPUT: ['[', '-', ',', '(', ')', ':', '/']

r = open("osvrti_opj.txt", "r", encoding = "utf-8").read()

re_interpunkcija = r"(?<=[.,:!?])(?=[^\s])"

novo = re.sub(re_interpunkcija, r" ", r)

dat_w = open("osvrti_opj_pokusaj.txt", "w", encoding = "utf-8")

dat_w.write(novo)

dat_w.close()
