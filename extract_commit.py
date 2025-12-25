import requests
from bs4 import BeautifulSoup

def extract_commit_details(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Author username
    author = None
    author_link = soup.find("a", {"rel": "author"})
    if author_link:
        author = author_link.text.strip()

    # Commit message
    message = None
    message_tag = soup.find("div", class_="commit-title")
    if message_tag:
        message = message_tag.text.strip()

    # Commit timestamp
    timestamp = None
    time_tag = soup.find("relative-time")
    if time_tag:
        timestamp = time_tag.get("datetime")

    # Author email (may not always exist)
    email = None
    email_tag = soup.find("a", href=lambda x: x and x.startswith("mailto:"))
    if email_tag:
        email = email_tag.text.strip()

    return {
        "author": author,
        "message": message,
        "timestamp": timestamp,
        "email": email
    }
