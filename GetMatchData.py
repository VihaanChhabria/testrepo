import json
import csv
import requests

BASE_URL = "https://www.thebluealliance.com/api/v3"

def main(event_key, api_key):
    """
    Downloads matches for the given event key and TBA API key, and saves to a json and csv file.

    :param event_key: The event key to download matches for
    :param api_key: The TBA API key to use
    :return: None
    """
    # Get the matches from TBA
    allMatches = getEventMatches(event_key, api_key)

    # Rearrange the matches to be in a more useful format
    qualMatches =  [match for match in matches if match["comp_level"] == "qm"]
    
    matchesRearranged = []
    
    # Iterate through the list of qualifying matches
    for match in qualMatches:
        # Get the red and blue teams for the current match
        red_teams, blue_teams = getMatchTeams(match)

        # Add the match to the list of rearranged matches with the match number and the red and blue alliances
        matchesRearranged.append({
            "matchNum": match["match_number"],
            "redAlliance": red_teams,
            "blueAlliance": blue_teams
        })

    # Save the rearranged matches to a json file
    with open("../data/EventMatches.json", "w") as file:
        json.dump({"matches": matchesRearranged}, file)

def getEventMatches(event_key, api_key):
    """
    Fetches and converts the matches for the given event key using the given TBA API key.
    
    :param event_key: The event key to download matches for
    :param api_key: The TBA API key to use
    :return: The matches for the given event
    """
    # Construct the URL to query the TBA API
    url = f"{BASE_URL}/event/{event_key}/matches/"
    
    # Fetch the matches from the TBA API
    body = fetchTBA(url, api_key)
    
    # Parse the matches from the JSON response
    matches = json.loads(body)
    
    return matches

def fetchTBA(url: str, api_key: str) -> str:
    """
    Fetches a response from the TBA API using the given URL and API key.

    :param url: The URL to query the TBA API
    :param api_key: The TBA API key to use
    :return: The response from the TBA API
    """
    # Set the headers for the request
    headers = {
        "X-TBA-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Make the request to the TBA API
    response = requests.get(url, headers=headers)
    
    # Return the response from the TBA API
    return response.text

def getMatchTeams(match):
    """
    Extracts the teams from the given match.
    
    :param match: The match to extract the teams from
    :return: The teams in the red and blue alliances
    """
    alliances = match["alliances"]
    
    # Extract the red alliance
    red_alliance = alliances["red"]
    # Extract the teams from the red alliance
    red_teams = red_alliance["team_keys"]
    
    # Extract the blue alliance
    blue_alliance = alliances["blue"]
    # Extract the teams from the blue alliance
    blue_teams = blue_alliance["team_keys"]

    return red_teams, blue_teams

if __name__ == "__main__":
    main(input("Enter event key (ex: 2024mrcmp): "), input("Enter TBA API key: "))