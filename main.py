import cloudscraper
from bs4 import BeautifulSoup
import re

def get_first_three_numbers():
    url = "https://temp-number.com/countries/United-Kingdom"
    scraper = cloudscraper.create_scraper()
    resp = scraper.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n")
    matches = re.findall(r'44\d{10}', text)
    seen = set()
    unique = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            unique.append(m)
    return unique[:3]
def get_last_three_sms(num:list):
    url = f"https://temp-number.com/temporary-numbers/United-Kingdom/{number}/1"
    scraper = cloudscraper.create_scraper()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
    }
    resp = scraper.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n")
    res = []
    text = text.split('From')
    for tex in text:
        if 'FACEBOOK'.lower() in tex.lower():
            res.append(tex.strip())
    return res

if __name__ == "__main__":
    num = get_first_three_numbers()
    for number in num:
        try:
            msgs = get_last_three_sms(number)[0]
            match = re.search(r'\b\d{6}\b', msgs)
            code = match.group()
            print(code)
        except Exception as e:
            print("Not Message!", e)
