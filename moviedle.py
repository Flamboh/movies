import requests
import json
import random
from bs4 import BeautifulSoup
from config import *


def get_movie_id(movie_title: str) -> int:
    '''
    Get movie ID from TMDB API
    '''
    # Remove year from title
    if movie_title[-4:-1].isdigit():
        movie_title = movie_title[:-4]
    # Set URL for movie search
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_access_token}"
    }

    response = requests.get(url, headers=headers)

    # Convert response to dictionary
    search_dict = json.loads(response.text)

    # Get movie ID from search results
    movie_id = search_dict['results'][0]['id']

    return movie_id


def get_movie_info(movie_id: int) -> dict:
    '''
    Load movie info from TMDB API
    '''
    # Set URL for movie
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=credits&language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_access_token}"
    }

    response = requests.get(url, headers=headers)

    # Convert response to dictionary
    info_dict = json.loads(response.text)

    return info_dict


def get_movie_rating(movie_title: int) -> list:
    '''
    Get community rating from letterboxd using html
    '''
    film = movie_title.strip().lower().replace(' ', '-').replace(':', '').replace('.', '').replace('(', '').replace(')', '')
    url = f'https://letterboxd.com/film/{film}/'
    print(url)
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    rating_html = soup.find("meta", attrs={'name':'twitter:data2'})
    rating_num = round(float(rating_html['content'][:4].strip()), 1)

    return rating_num   


def get_movie_list(num_movies) -> list:
    '''
    Get list of popular movies on letterboxd from text file
    '''
    with open('film_list.txt', 'r') as f:
        movie_list = [x.strip().replace('-', ' ').title() for x in f.readlines()[0:num_movies]]
        f.close()
    return movie_list

def play_moviedle():
    '''
    Play the moviedle game
    '''
    movie_list = get_movie_list(500)
    movie_title = random.choice(movie_list)
    rating = get_movie_rating(movie_title)
    # print(movie_title)
    movie_id = get_movie_id(movie_title)
    movie_info = get_movie_info(movie_id)
    movie_title = movie_info['title']
    # print(movie_title)
    # print(movie_info['title'], movie_info['credits']['cast'][0]['name'], rating)
    for crew in movie_info['credits']['crew']:
        if crew['job'] == 'Director':
            director = crew['name']
            break
    # print(director)
    print('Welcome to Moviedle!')
    print('You will be guessing a movie given a few hints about it.')
    print('You will have 8 guesses')
    for i in range(8):
        if i == 0:
            print(f'The movie has a rating of {rating} on Letterboxd')
        elif i == 1:
            print(f'The movie has a runtime of {movie_info["runtime"]} minutes')
        elif i == 2:
            print(f'The movie\'s primary genre is {movie_info["genres"][0]["name"]}')
        elif i == 3:
            print(f'The movie\'s secondary genre is {movie_info["genres"][1]["name"]}')
        elif i == 4:
            print(f'The movie was released in {movie_info["release_date"][:4]}')
        elif i == 5:
            print(f'The movie was directed by {movie_info["credits"]["crew"][0]["name"]}')
        elif i == 6:
            print(f'The movie stars {movie_info["credits"]["cast"][0]["name"]}')
        else:
            print(f'Final guess! The movie\'s tagline is "{movie_info["tagline"]}"')
        guess = input('Guess the movie: ')
        if guess.lower() == movie_title.lower():
            print('Correct!')
            break
        else:
            print('Incorrect')
    print(f'The movie was {movie_title}')

if __name__ == '__main__':
    play_moviedle()
    