import requests as rq
from bs4 import BeautifulSoup

def scrape(name, typeName, year):
    songsList = list()
    baseUrl = "https://www.tunefind.com"
    urlPath = getUrlPath(name,typeName,year)

    res = rq.get(f"{baseUrl}{urlPath}")
    soup = BeautifulSoup(res.content,"html.parser",from_encoding="utf-8")
    if typeName == "show":
        mainContainer = soup.find(class_= lambda el:el and el.startswith("MainList_container__"))
        for path in {el.get("href") for el in mainContainer.findAll("a")}:
            res = rq.get(f"{baseUrl}{path}")
            soup = BeautifulSoup(res.content,"html.parser",from_encoding="utf-8")
            mainContainer = soup.find(class_= lambda el:el and el.startswith("MainList_container__"))
            items = mainContainer.findAll("h3", class_=lambda el:el and el.startswith("EpisodeListItem_title__"))
            for item in items:
                linkItem = item.find("a")
                pathLink = linkItem.get("href")
                season, episode, episodeName = linkItem.string.split(" · ")
                res = rq.get(f"{baseUrl}{pathLink}")
                soup = BeautifulSoup(res.content, "html.parser",from_encoding="utf-8")
                songList = soup.findAll("div", class_=lambda el:el and el.startswith("SongRow_container__"))
                for song in songList:
                    title = song.find("a",class_=lambda el:el and el.startswith("SongTitle_link__")).string.strip()
                    artist = song.find("a",class_=lambda el:el and el.startswith("Subtitle_subtitle__")).string.strip()
                    songsList.append({"title":title, "artist":artist, "season":season, "episode":episode, "episodeName":episodeName})

    elif typeName == "movie":
        songList = soup.findAll("div", class_=lambda el:el and el.startswith("SongRow_container__"))
        for song in songList:
            title = song.find("a",class_=lambda el:el and el.startswith("SongTitle_link__")).string.strip()
            artist = song.find("a",class_=lambda el:el and el.startswith("Subtitle_subtitle__")).string.strip()
            songsList.append({"title":title, "artist":artist})

    return songsList

def getUrlPath(name: str, typeName: str, year: str):
    if typeName == "show":
        return f"/{typeName}/{name}"
    elif typeName == "movie":
        return f"/{typeName}/{name}-{year}"
