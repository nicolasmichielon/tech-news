import requests
from bs4 import BeautifulSoup

links = []
subtexts = []

# Grab the links and subtexts from the Hacker News websit, going from page 1 to page 20
for p in range(1, 20):
    res = requests.get(f'https://news.ycombinator.com/news?p={p}')
    soup = BeautifulSoup(res.text, 'html.parser')
    link = soup.select('.titlelink')
    subtext = soup.select('.subtext')
    links.extend(link)
    subtexts.extend(subtext)

# Sort stories by votes


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


# Creates a list of dictionaries with the title, link and votes of each story that has 100 or more likes
def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


# Stores the list of dictionaries
news = create_custom_hn(links, subtexts)
