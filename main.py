
import os
import requests
from dotenv import load_dotenv


# ==========================================
# 1. Load Environment Variables
# ==========================================

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")
API_URL = "https://www.omdbapi.com/"


# ==========================================
# 2. Movie Class
# ==========================================

class Movie:
    """A class to store and organize movie information."""

    def __init__(self, data):
        self.title = data.get("Title", "N/A")
        self.year = data.get("Year", "N/A")
        self.genre = data.get("Genre", "N/A")
        self.director = data.get("Director", "N/A")
        self.actors = data.get("Actors", "N/A")
        self.rating = data.get("imdbRating", "N/A")
        self.runtime = data.get("Runtime", "N/A")
        self.language = data.get("Language", "N/A")
        self.country = data.get("Country", "N/A")
        self.plot = data.get("Plot", "N/A")

    def display(self):
        """Display movie information in a formatted summary."""

        print("\n" + "=" * 65)
        print("                     MOVIE INFORMATION")
        print("=" * 65)

        print(f"Title       : {self.title}")
        print(f"Year        : {self.year}")
        print(f"Genre       : {self.genre}")
        print(f"Director    : {self.director}")
        print(f"Actors      : {self.actors}")
        print(f"IMDb Rating : {self.rating}")
        print(f"Runtime     : {self.runtime}")
        print(f"Language    : {self.language}")
        print(f"Country     : {self.country}")

        print("-" * 65)
        print("Plot:")
        print(self.plot)

        print("=" * 65)


# ==========================================
# 3. API Integration
# ==========================================

def get_movie(movie_title):
    """Retrieve movie information from the OMDb API."""

    params = {
        "apikey": API_KEY,
        "t": movie_title,
        "plot": "full",
        "r": "json"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15
    )

    # Check HTTP status code
    response.raise_for_status()

    # Parse JSON response
    data = response.json()

    # Check API response
    if data.get("Response") == "False":
        raise ValueError(data.get("Error", "Movie not found."))

    return data


# ==========================================
# 4. Main Program
# ==========================================

def main():

    print("=" * 65)
    print("                  WELCOME TO MOVIE FINDER")
    print("=" * 65)

    # Check API key
    if not API_KEY:
        print("\nError: API key not found!")
        print("Please configure your .env file.")
        return

    while True:

        print("\n1. Search for a movie")
        print("2. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            movie_title = input("\nEnter movie title: ").strip()

            if not movie_title:
                print("\nPlease enter a valid movie title.")
                continue

            try:
                print("\nSearching for movie...")

                # Get movie data from API
                movie_data = get_movie(movie_title)

                # Create Movie object
                movie = Movie(movie_data)

                # Display movie information
                movie.display()

            except ValueError as error:
                print(f"\nError: {error}")

            except requests.exceptions.Timeout:
                print("\nError: Request timed out.")

            except requests.exceptions.RequestException as error:
                print(f"\nNetwork error: {error}")

            except requests.exceptions.JSONDecodeError:
                print("\nError: Unable to parse JSON response.")

        elif choice == "2":
            print("\nThank you for using Movie Finder!")
            break

        else:
            print("\nInvalid choice. Please select 1 or 2.")


# ==========================================
# 5. Program Entry Point
# ==========================================

if __name__ == "__main__":
    main()
