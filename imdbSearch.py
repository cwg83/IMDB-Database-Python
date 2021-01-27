from easygui import *
import http.client
import json


while True:

    conn = http.client.HTTPSConnection("movie-database-imdb-alternative.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "EXAMPLEKEY123",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
        }

    fieldNames = ['Name or ID: ']
    search = multenterbox(msg='IMDB Database search by name or ID', title='Enter', fields=fieldNames)

    try:
        if search[0] == "":
            print(textbox("Search field was blank. Please try again.", "No results"))
            continue
    except:
        break

    try:
        search = ' '.join(search)
    except:
        break

    search = search.replace(" ", "%20")

    if search.startswith("tt"):
        conn.request("GET", "/?i=" + search + "&r=json", headers=headers)
    else:
        conn.request("GET", "/?s=" + search + "&page=1&r=json", headers=headers)

    res = conn.getresponse()
    data = res.read()
    parsed = json.loads(data)

    results = []

    if search.startswith("tt"):

        results.append("[TITLE] " + parsed["Title"] + "\n")
        results.append("[ACTORS] " + parsed['Actors'] + "\n")
        results.append("[AWARDS] " + parsed['Awards'] + "\n")
        results.append("[DIRECTOR] " + parsed['Director'] + "\n")
        results.append("[GENRE] " + parsed['Genre'] + "\n")
        results.append("[METASCORE] " + parsed['Metascore'] + "\n")
        results.append("[PLOT] " + parsed['Plot'] + "\n")
        results.append("[RATED] " + parsed['Rated'] + "\n")
        results.append("[TYPE] " + parsed['Type'] + "\n")
        results.append("[RELEASE DATE] " + parsed['Released'] + "\n")
        results.append("[RUNTIME] " + parsed['Runtime'] + "\n")
        results.append("[YEAR] " + parsed['Year'] + "\n")
        results.append("[LANGUAGES] " + parsed['Language'] + "\n")
        results.append("[IMDB RATING] " + parsed['imdbRating'] + "\n")
        results.append("[IMDB ID] " + parsed['imdbID'] + "\n")
        if parsed['Type'] == "series":
            results.append("[TOTAL SEASONS] " + parsed['totalSeasons'] + "\n")
        else:
            results.append("[BOX OFFICE] " + parsed['BoxOffice'] + "\n")

    else:
        try:
            results.append("\n\n\nTOTAL RESULTS: " + parsed['totalResults'] + "\n")
        except:
            print(textbox("Apologies, no results found.", "No results"))
            break
        for response, search in parsed.items():
            for movie in search:
                if type(movie) is dict:

                    results.append("[TITLE] " + movie["Title"] + "\n")
                    results.append("[YEAR] " + movie["Year"] + "\n")
                    results.append("[IMDB ID] " + movie["imdbID"] + "\n")
                    results.append("[TYPE] " + movie["Type"].capitalize() + "\n")
                    results.append("---------------------------------------\n")

    print(textbox("Results:", "Results", results))
