from easygui import *
import http.client
import json


while True:
    # Connect to the API server
    conn = http.client.HTTPSConnection("movie-database-imdb-alternative.p.rapidapi.com")
    # Define API Key and Host. Replace EXAMPLEKEY123 with your API key
    headers = {
        'x-rapidapi-key': "EXAMPLEKEY123",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
        }
    # Define text to display to the left of the input field
    fieldNames = ['Name or ID: ']
    # Define multenterbox parameters. Each word is added separately to a list
    search = multenterbox(msg='IMDB Database search by name or ID', title='Enter', fields=fieldNames)
    # If first item in search list is blank then display blank error message
    try:
        if search[0] == "":
            print(textbox("Search field was blank. Please try again.", "No results"))
            continue
    except:
        break
    # Join items in input list together with a space as a string
    try:
        search = ' '.join(search)
    except:
        break
    # Replace spaces with %20 (I tried to do this simultaneously but was having issues)
    search = search.replace(" ", "%20")
    # If input is an IMDB ID (if it begins with "tt") use the ID parameters for the connection request
    if search.startswith("tt"):
        conn.request("GET", "/?i=" + search + "&r=json", headers=headers)
    # Otherwise use the keyword parameters for the connection request
    else:
        conn.request("GET", "/?s=" + search + "&page=1&r=json", headers=headers)
    # Get the response and format it to json
    res = conn.getresponse()
    data = res.read()
    parsed = json.loads(data)
    # Create empty list for the results
    results = []
    # If input is an IMDB ID (if it begins with "tt")
    if search.startswith("tt"):
        # Append the following to the results list
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
        if parsed['Type'] == "series": # If the result is a series type then also include the following
            results.append("[TOTAL SEASONS] " + parsed['totalSeasons'] + "\n")
        else:
            results.append("[BOX OFFICE] " + parsed['BoxOffice'] + "\n")
    # Otherwise we assume it is a keyword search
    else:
        try:    
            results.append("\n\n\nTOTAL RESULTS: " + parsed['totalResults'] + "\n") # Try to append the results key
        except:
            print(textbox("Apologies, no results found.", "No results")) # If it fails, assume there are no results and display textbox
            break
        for response, search in parsed.items():
            for movie in search:
                if type(movie) is dict:
                    # Append the desired keys to the results
                    results.append("[TITLE] " + movie["Title"] + "\n")
                    results.append("[YEAR] " + movie["Year"] + "\n")
                    results.append("[IMDB ID] " + movie["imdbID"] + "\n")
                    results.append("[TYPE] " + movie["Type"].capitalize() + "\n")
                    results.append("---------------------------------------\n")
    # Display results in the textbox popup
    print(textbox("Results:", "Results", results))
