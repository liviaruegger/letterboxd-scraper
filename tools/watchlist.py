from bs4 import BeautifulSoup

from film import get_film, parse_film_data
from utils import request_with_retry, save_to_csv


def get_watchlist_page(username: str, page: int) -> str:
    url = f"https://letterboxd.com/{username}/watchlist/page/{page}"
    print("Requesting:", url)

    response = request_with_retry(url)
    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to retrieve the watchlist")


def parse_watchlist_page(
    html_content: str, complete_data: bool = False
) -> list[dict[str, str]]:
    soup = BeautifulSoup(html_content, "html.parser")

    films = []

    # Find all poster items in the watchlist
    movie_items = soup.find_all("li", class_="poster-container")

    for item in movie_items:
        # Extract basic info from each poster
        poster_item = item.find(
            "div", class_=lambda x: x and "film-poster" in x
        )
        endpoint = poster_item.get("data-target-link")
        id = poster_item.get("data-film-id")

        film_info = {"id": id, "endpoint": endpoint}
        if complete_data:
            film_info.pop("endpoint")
            film_info.update(parse_film_data(get_film(endpoint)))

        films.append(film_info)

    print(f"Filmes extraidos da pagina: {len(films)}")

    return films


def get_complete_watchlist_data(
    username: str, complete_data: bool = False
) -> list[dict[str, str]]:
    film_data = []

    page = 1

    print(f"\n === Collecting page {page} ===")
    watchlist_html = get_watchlist_page(username, page)
    page_film_data = parse_watchlist_page(watchlist_html, complete_data)
    print(f"Total coletado: {len(page_film_data)}")

    while page_film_data:
        film_data += page_film_data
        page += 1

        print(f"\n === Collecting page {page} ===")
        watchlist_html = get_watchlist_page(username, page)
        page_film_data = parse_watchlist_page(watchlist_html, complete_data)
        print(f"Total coletado: {len(film_data) + len(page_film_data)}")

    return film_data


def save_watchlist_to_csv(username: str) -> None:
    save_to_csv(
        get_complete_watchlist_data(username=username, complete_data=True),
        f"{username}_watchlist.csv",
    )


if __name__ == "__main__":
    save_watchlist_to_csv("zanalivia")
