from bs4 import BeautifulSoup as bs
import requests
import csv

MAINURL = "https://www.recenzijefilmova.com/komedije-filmovi/"
PAGENUMBER = 25


def get_links():
    """Funkcija get_links() dohvaća sve linkove sa prvih BROJ_STRANICA sa MAIN_URL-a te ih vraća u obliku liste."""
    links = []
    for i in range(1, PAGENUMBER + 1):
        url = MAINURL + "page/" + str(i)
        print("Fetching links from page " + str(i))
        response = requests.get(url)
        html = response.content
        soup = bs(html, "lxml")
        items = soup.find_all("div", {"id": "tdi_39"})
        for item in items:
            for h3 in item.find_all("h3", {"class": "entry-title td-module-title"}):
                link = h3.find("a", href=True)["href"]
                if "recenzija" in link:
                    links.append(link)

    return links


def get_review_data(url):
    """Funkcija vraća sljedeće sa određenog URL-a u obliku dictionary: author, date, score, impression, review."""
    review_dict = {}
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")
    print("Fetching review from " + url)

    author = ""
    author_elem = soup.find("a", {"class", "tdb-author-name"})
    if author_elem is not None:
        author = author_elem.getText()
    review_dict["author"] = author

    time = soup.find("time", {"class": "entry-date updated td-module-date"})
    date = time.getText()
    review_dict["date"] = date

    score_elem = soup.find("div", {"class": "td-review-final-score"})
    score = ""
    if score_elem is not None:
        score = score_elem.getText()
    review_dict["score"] = score

    impression = ""
    impression_elem = soup.find("div", {"class": "td-review-summary-content"})
    if impression_elem is not None:
        impression = impression_elem.getText()
    review_dict["impression"] = impression

    div = soup.find("div", {"data-td-block-uid": "tdi_68"}).find("div", {"class": "tdb-block-inner td-fix-index"})
    review = ""
    for child in div.findChildren(recursive=False):
        if child.name == "p":
            review += child.getText(strip=True).replace("<br>", "").replace("</br>", "")

        if child.name == "iframe":
            break
    review = "[" + review + "]"
    review_dict["review"] = review
    review_dict["url"] = url

    return review_dict


with open("osvrti_opj.tsv", "w", newline = "", encoding = "utf-8") as review_file:
    review_writer = csv.writer(review_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    review_writer.writerow(["review", "overall_score", "first_impression", "review_date", "reviewer", "home_url"])

    links = get_links()
    print("Found " + str(len(links)) + " links")
    for link in links:
        review = get_review_data(link)
        review_writer.writerow([review.get("review"), review.get("score"), review.get("impression"), review.get("date"), review.get("author"), review.get("url")])