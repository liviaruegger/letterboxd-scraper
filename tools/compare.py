from watchlist import get_complete_watchlist_data
from film import get_film, parse_film_data
from utils import save_to_csv


def compare_watchlists(user1: str, user2: str):
    watchlist1 = [
        f["endpoint"]
        for f in get_complete_watchlist_data(
            username=user1, complete_data=False
        )
    ]
    watchlist2 = [
        f["endpoint"]
        for f in get_complete_watchlist_data(
            username=user2, complete_data=False
        )
    ]

    film_data = []
    films_in_common = set(watchlist1).intersection(set(watchlist2))
    print(f"\n --- found {len(films_in_common)} films in common ---")
    
    print(f"\n === Collecting film details ===")
    for endpoint in films_in_common:
        film_data.append(parse_film_data(get_film(endpoint)))

    return film_data


def save_comparison_to_csv(
    user1: str, user2: str, sort_by_rating: bool = False
) -> None:
    data = compare_watchlists(user1, user2)

    if sort_by_rating:
        data = sorted(data, key=lambda x: x["average_rating"], reverse=True)

    save_to_csv(data, f"{user1}_and_{user2}.csv")


if __name__ == "__main__":
    user1 = input("Enter user: ")
    user2 = input("Enter another user: ")

    save_comparison_to_csv(user1, user2, True)
