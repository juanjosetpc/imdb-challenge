import requests
import questionary
from questionary import Choice
import os

API_URL = os.getenv("API_URL", "http://localhost:8080/api")

def format_professions(profession_str):
    professions = [p.strip() for p in profession_str.split(",") if p.strip()]
    if not professions:
        return "unknown profession"
    if len(professions) == 1:
        return professions[0]
    elif len(professions) == 2:
        return f"{professions[0]} and {professions[1]}"
    else:
        return ", ".join(professions[:-1]) + f" and {professions[-1]}"

def search_person():
    name = questionary.text("Which person do you want to search for?").ask()
    if not name or not name.strip():
        print("Please enter a valid name.")
        return

    try:
        response = requests.get(f"{API_URL}/people/search", params={"name": name})
        if response.status_code == 200:
            people = response.json()
            if people:
                for p in people:
                    birth_year = p.get('birthYear', 'unknown year')
                    professions = p.get('profession')
                    professions_text = format_professions(professions)
                    print(f"{p.get('name')} was born in {birth_year} and was {professions_text}.")
        elif response.status_code == 204:
            print("No people found with that name. (204 No Content)")
        elif response.status_code == 400:
            print("Invalid or missing parameter.")
        else:
            print(f"Query error: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {e}")

def search_film():
    title = questionary.text("Which movie do you want to search for?").ask()
    if not title or not title.strip():
        print("Please enter a valid title.")
        return

    try:
        response = requests.get(f"{API_URL}/films/search", params={"title": title})
        if response.status_code == 200:
            films = response.json()
            if films:
                for f in films:
                    original_title = f.get('originalTitle') or f.get('title') or 'Unknown'
                    title_type = f.get('type', 'unknown type')
                    print(f"{original_title}, originally titled '{f.get('originalTitle', original_title)}', is a {title_type}.")
        elif response.status_code == 204:
            print("No movie found with that name. (204 No Content)")
        elif response.status_code == 400:
            print("Invalid or missing parameter.")
        else:
            print(f"Query error: {response.status_code}")
    except Exception as e:
        print(f"Connection error: {e}")

def main():
    while True:
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                Choice("Search person by name", "person"),
                Choice("Search movie by title", "film"),
                Choice("Exit", "exit"),
            ],
        ).ask()

        if choice == "person":
            search_person()
        elif choice == "film":
            search_film()
        elif choice == "exit":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
