import requests
from bs4 import BeautifulSoup
import random
import tmdbsimple as tmdb
from config import *
import json
tmdb.API_KEY = tmdb_key
tmdb.REQUESTS_TIMEOUT = 5
header = tmdb_access_token


def get_rating(movie_title: str) -> float:
    film = movie_title.strip().lower().replace(' ', '-').replace(':', '').replace('.', '').replace('(', '').replace(')', '')
    url = f'https://letterboxd.com/film/{film}/'

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    
    rating_html = soup.find("meta", attrs={'name':'twitter:data2'})
    rating_num = round(float(rating_html['content'][:4].strip()), 1)

    return rating_num   


def print_rules():
    print('Welcome to the rating guesser')
    print('You play by guessing the rating of the randomly selected movie.\nMake guesses to one decimal place (e.g. 4.3)')


def play_guesser():
    movies_list = ['Barbie', 'Wonka', 'Scott Pilgrim vs. the World', 'Hereditary', 'Dune (2021)', 'Spider-Man: Across the Spider-Verse', 'Spider-Man: Into the Spider-Verse', 'The Lighthouse (2019)', 'Smile (2022)', 'The Croods', 'Beau Is Afraid', 'Barbarian (2022)', 'Cocaine Bear', 'Fantastic Mr. Fox', 'Despicable Me', 'Joker', 'Avengers: Endgame']
    
    print_rules()
    
    while True:
        # movie = random.choice(movies_list)
        movie = 'Wonka'
        search = tmdb.Search()
        response = search.movie(query=movie)
        movie_id = search.results[0]['id']
        print(movie_id)
        # movie_tmdb = tmdb.Movies(int(movie_id))
        # response = movie_tmdb.info()
        print(type(movie_id))
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {tmdb_access_token}"
        }

        response = requests.get(url, headers=headers)
        
        # print(response.text)
        d = json.loads(response.text)
        # print(d['cast'][0]['name'])

        print(f'The movie you will be guessing this round is: {movie}')
        rating = get_rating(movie)
        points = 0

        while True:
            guess = input('Guess the rating: ').strip()
            if not guess.replace('.', '').isdigit() or len(guess) != 3 or '.' not in guess:
                print('Please input a valid guess')
            else:
                guess = float(guess)
                break
        difference = round(abs(guess - rating), 1)
        print(f'{movie} has an average rating of {rating}')
        if difference > 0.3:
            print('A bit off, no points this movie')
        elif difference == 0:
            print('Right on! two points for this movie')
            points += 2
        else:
            print('Close, one point for this movie')
            points += 1
        print(f'You have {points} point(s)')
        if input('Would you like to keep playing? (Y or N): ')[0].lower() == 'n':
            break
    print(f'You got {points} point(s).\nThanks for playing!')


def main():
    play_guesser()

if __name__ == '__main__':
    main()