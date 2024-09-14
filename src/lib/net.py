import requests


def get(link: str) -> str:
    return requests.get(link, timeout=8, allow_redirects=True).text


def download(link: str, dist: str) -> None:
    with open(dist, "tw", encoding="utf-8") as file:
        file.write(get(link))
