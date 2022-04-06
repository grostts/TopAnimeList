import requests
from bs4 import BeautifulSoup
import json


def get_data():
    url = "https://myanimelist.net/topanime.php"
    headers = {
        "user-agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko)"
                      " Version/11.0 Mobile/15A5341f Safari/604.1"
    }

    animes_data_list = []

    # req = requests.get(headers=headers, url=url)
    #
    # with open(f'myanimelist_data.html', 'w', encoding='utf-8') as file:
    #     file.write(req.text)

    with open(f'myanimelist_data.html', 'r', encoding='utf-8') as file:
        src = file.read()


    soup = BeautifulSoup(src, 'lxml')
    animes = soup.find_all(class_="hoverinfo_trigger fl-l ml12 mr8")

    anime_urls = []
    anime_names= []
    for anime in animes:
        anime_href = anime.get("href")
        anime_urls.append(anime_href)
        anime_names.append(anime_href.split("/")[5])


    # for i in range(len(anime_urls)):
    for i in range(3):

        req = requests.get(headers=headers, url=anime_urls[i])
        with open(f'data/{anime_names[i]}.html', 'w', encoding="utf-8") as file:
            file.write(req.text)

        with open(f'data/{anime_names[i]}.html', 'r', encoding="utf-8") as file:
            src1 = file.read()

        soup = BeautifulSoup(src1, "lxml")

        # Get raiting
        try:
            anime_raiting = soup.find(class_="fl-l score").text
        except Exception:
            anime_raiting = "No anime rating"

        # Get episodes
        try:
            anime_episodes = soup.find_all("div", class_="spaceit_pad")[5].text.split(':')[1].strip()
        except Exception:
            anime_episodes = "No number episodes"

        # Get studio
        try:
            anime_studio = soup.find_all("div", class_="spaceit_pad")[12].text.split(':')[1].strip()
        except Exception:
            anime_studio = "No anime studios"

        # Get genre
        try:
            anime_genre = soup.find_all("div", class_="spaceit_pad")[14].text.split(':')[1].strip().replace("         ", " ")
        except Exception:
            anime_genre = "No anime genre"

        # Get description
        try:
            anime_description = soup.find("tr").find("p").text
        except Exception:
            anime_description = "No anime description"

        # Get poster
        try:
            anime_poster = soup.find("div", class_="leftside").find('img').get("data-src")
        except Exception:
            anime_poster = "No anime poster"


        animes_data_list.append(
            {
                "name": anime_names[i],
                "genres": anime_genre,
                "score": anime_raiting,
                "poster": anime_poster,
                "episodes": anime_episodes,
                "description": anime_description
            }
        )


    with open("anime_data.json", "a", encoding="utf-8") as file:
        json.dump(animes_data_list, file, indent=4, ensure_ascii=False)


get_data()