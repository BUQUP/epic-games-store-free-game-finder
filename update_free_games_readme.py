import requests
from datetime import datetime, timezone

"""
Update README.md file with game name and URL.
"""
def clear_readme(game_name, game_url):
    with open("README.md", "w") as readme:  # Open README.md file in write mode
        readme.write(f"<p align=\"center\">\n")
        readme.write(f"    <b><a href=\"{game_url}\">{game_name}</a></b>\n")
        readme.write(f"</p>\n\n")

"""
Parse date string into datetime object and convert it to UTC timezone.
"""
def parse_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    date_obj_utc = date_obj.replace(tzinfo=timezone.utc)
    return date_obj_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

"""
Check for free games and update README.md file with relevant information.
"""
def check_free_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=GB&allowCountries=GB"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for any HTTP error response
        
        data = response.json()
        
        if "data" in data:
            game_name = data["data"]["Catalog"]["searchStore"]["elements"][0]["title"]
            game_url = f"https://store.epicgames.com/en-US/p/{data['data']['Catalog']['searchStore']['elements'][0]['productSlug']}"
            clear_readme(game_name, game_url)
            
            free_games = []  # List to store information about free games
            
            # Iterating over each game element in the response
            for game in data["data"]["Catalog"]["searchStore"]["elements"]:
                title = game["title"]
                is_free = game["price"]["totalPrice"]["discountPrice"] == 0  # Check if the game is free
                
                if is_free:  # If the game is free
                    url = f"https://store.epicgames.com/en-US/p/{game['productSlug']}"
                    image_url = game["keyImages"][0]["url"]
                    
                    start_date = None
                    end_date = None
                    
                    if "promotions" in game:  # Check if promotions key exists in the game
                        if "promotionalOffers" in game["promotions"]:
                            if game["promotions"]["promotionalOffers"]:
                                promotion = game["promotions"]["promotionalOffers"][0]
                                
                                if "promotionalOffers" in promotion:
                                    if promotion["promotionalOffers"]:
                                        start_date = parse_date(promotion["promotionalOffers"][0].get("startDate"))
                                        end_date = parse_date(promotion["promotionalOffers"][0].get("endDate"))
                                        
                    free_games.append((title, url, image_url, start_date, end_date))
            
            if free_games:  # If there are free games available
                with open("README.md", "a") as readme:  # Open README.md file in append mode
                    readme.write(f"<table align=\"center\">\n")
                    readme.write(f"  <tr>\n")
                    readme.write(f"    <td align=\"center\"><b>Start Date</b></td>\n")
                    readme.write(f"    <td align=\"center\"><b>End Date</b></td>\n")
                    readme.write(f"  </tr>\n")
                    
                    # Iterating over each free game and writing its start and end date
                    for _, _, _, start_date, end_date in free_games:
                        readme.write(f"  <tr>\n")
                        readme.write(f"    <td align=\"center\">{start_date}</td>\n")
                        readme.write(f"    <td align=\"center\">{end_date}</td>\n")
                        readme.write(f"  </tr>\n")
                    
                    readme.write(f"  <tr>\n")
                    readme.write(f'    <td colspan="2" align="center"><img src="{free_games[0][2]}" width="400"></td>\n')
                    readme.write(f"  </tr>\n")
                    
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
                    readme.write(f"<p align=\"center\">\n")
                    readme.write(f"<em>Last Updated: {current_time}</em>\n")
                print("Successfully updated README.md with free games.")
            else:
                print("No free games found.")
        else:
            print("No data found in the response.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    check_free_games()
