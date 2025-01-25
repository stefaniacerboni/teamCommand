from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from flask import Flask, request

app = Flask(__name__)


def scrape_live_game(player_name="fragola"):
    url = f"https://lolpros.gg/player/{player_name}#live-game"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    team_containers = soup.find_all("div", class_="team")
    results = {}

    for team_container in team_containers:
        team_name_el = team_container.find("div", class_="team-name")
        if not team_name_el:
            continue
        team_name = team_name_el.get_text(strip=True)
        player_displays = team_container.find_all("div", class_="player-display")

        players = []
        for player in player_displays:
            name_el = player.find("a", class_="player-name") or player.find("span", class_="player-name")
            player_name = name_el.get_text(strip=True) if name_el else "Unknown"

            champion_div = player.find("div", class_="champion")
            if champion_div:
                champ_span = champion_div.find("span", class_="hint--top")
                champion_name = champ_span["aria-label"] if (
                            champ_span and champ_span.has_attr("aria-label")) else "Unknown Champion"
            else:
                champion_name = "Unknown Champion"

            players.append({
                "player_name": player_name,
                "champion_name": champion_name
            })
        results[team_name] = players

    # Build a simple string response (or JSON)
    res_string = ""
    for team, players in results.items():
        res_string += f"{team} :"
        for p in players:
            res_string += f" - {p['player_name']} ( {p['champion_name']} ) "
    return res_string


@app.route("/")
def hello():
    # For example, read ?name=fragola from query param
    player_name = request.args.get("name", "fragola")
    data = scrape_live_game(player_name)
    return data


# Only run directly if local:
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
