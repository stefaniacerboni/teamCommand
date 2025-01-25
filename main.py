from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def scrape_live_game(player_name="fragola"):
    url = f"https://lolpros.gg/player/{player_name}#live-game"

    options = Options()
    options.add_argument("--headless")  # run in headless mode
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)  # Give time for the JS to load and update the DOM; adjust as needed

    # Retrieve the updated HTML
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Find each "team" container
    team_containers = soup.find_all("div", class_="team")

    results = {}
    for team_container in team_containers:
        # 1) Extract the team name (e.g., "Blue team", "Red team")
        team_name_el = team_container.find("div", class_="team-name")
        if not team_name_el:
            continue
        team_name = team_name_el.get_text(strip=True)

        # 2) For each player in this team, find the "player-display" sections
        player_displays = team_container.find_all("div", class_="player-display")
        players = []

        for player in player_displays:
            # a) Player name
            name_el = player.find("a", class_="player-name")
            if not name_el:
                name_el = player.find("span", class_="player-name")

            if name_el:
                player_name = name_el.get_text(strip=True)
            else:
                player_name = "Unknown"

            # b) Optional: Champion name
            champion_div = player.find("div", class_="champion")
            if champion_div:
                champ_span = champion_div.find("span", class_="hint--top")
                if champ_span and champ_span.has_attr("aria-label"):
                    champion_name = champ_span["aria-label"]
                else:
                    champion_name = "Unknown Champion"
            else:
                champion_name = "Unknown Champion"

            players.append({
                "player_name": player_name,
                "champion_name": champion_name
            })

        results[team_name] = players

    res_string = ""
    # Print or use the parsed data
    for team, players in results.items():
        res_string += f"{team} :"
        print(f"\nTeam: {team}")
        for p in players:
            res_string += f" - {p['player_name']} ( {p['champion_name'] } ) "
            print(f" - {p['player_name']} - {p['champion_name']} ")

    return res_string


if __name__ == "__main__":
    print(scrape_live_game("fragola"))
