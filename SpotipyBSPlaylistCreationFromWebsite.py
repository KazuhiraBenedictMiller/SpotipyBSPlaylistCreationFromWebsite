import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

Date = input("To which date would you like to be teleported? (YYYY-MM-DD Format)\n")

BillBoard = "https://www.billboard.com/charts/hot-100/" + Date + "/"

response = requests.get(BillBoard)

soup = BeautifulSoup(response.text, "html.parser")

#print(soup.prettify())

Titles = [x.getText(strip=True) for x in soup.select("li ul li h3")]

#print(Titles)

sp = spotipy.Spotify(
  auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                            redirect_uri="http://localhost:8888/callback",
                            client_id="0fedf79ef5c049fe85c956160b63ed5d",
                            client_secret="34728ffe591f4b7694fa7fa7b5aae5e5",
                            show_dialog=True,
                            cache_path="token.txt"))

user_id = sp.current_user()["id"]

song_uris = []
year = Date.split("-")[0]
for song in Titles:
    Results = sp.search(q=f"track:{song} year:{year}", type="track")
# print(result) #Prints the result
    try:
#   Handling exception where the song cannot be found. It is skipped in this case.
        uri = Results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(f"{song} exist in Spotify. Added.")
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{Date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
