import requests, json, flask

with open("key.txt") as f:
	key = f.read()

def fetch_ratings(show, key):
    response = requests.get("http://www.omdbapi.com/?t=" + show + "&apikey=" + key)
    data = response.json()
    print(data)
    output = {"name": data["Title"], "poster": data["Poster"], "seasons": []}

    if data["Type"] == "series":
        num_series = output["num_series"] = int(data["totalSeasons"])
        for season in range(1, num_series+1):
            season_data = {"season": season, "episodes": []}
            season_req = requests.get("http://www.omdbapi.com/?t=" + show + "&season=" + str(season) + "&apikey=" + key)
            for episode in season_req.json()["Episodes"]:
                link = "https://www.imdb.com/title/" + episode["imdbID"]
                #print("Season " + str(season) + " Episode " + episode["Episode"] + " Rating: " + episode['imdbRating'] + " | Link: " + link)
                season_data["episodes"].append({"episode": episode["Episode"], "rating": episode['imdbRating'], "link":link})
            output["seasons"].append(season_data)

    return output
show = input("Show title: ")

print(fetch_ratings(show, key))
