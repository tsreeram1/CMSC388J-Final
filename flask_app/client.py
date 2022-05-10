import requests


class Movie(object):
    def __init__(self, omdb_json, detailed=False):
        if detailed:
            self.genres = omdb_json["Genre"]
            self.director = omdb_json["Director"]
            self.actors = omdb_json["Actors"]
            self.plot = omdb_json["Plot"]
            self.awards = omdb_json["Awards"]

        self.title = omdb_json["Title"]
        self.year = omdb_json["Year"]
        self.imdb_id = omdb_json["imdbID"]
        self.type = "Movie"
        self.poster_url = omdb_json["Poster"]

    def __repr__(self):
        return self.title


class MovieClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        self.base_url = f"http://www.omdbapi.com/?apikey={api_key}&r=json&type=movie&"

    def search(self, search_string):
        """
        Searches the API for the supplied search_string, and returns
        a list of Media objects if the search was successful, or the error response
        if the search failed.

        Only use this method if the user is using the search bar on the website.
        """
        search_string = "+".join(search_string.split())
        page = 1

        search_url = f"s={search_string}&page={page}"

        resp = self.sess.get(self.base_url + search_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')

        search_results_json = data["Search"]
        remaining_results = int(data["totalResults"])

        result = []

        ## We may have more results than are first displayed
        while remaining_results != 0:
            for item_json in search_results_json:
                result.append(Movie(item_json))
                remaining_results -= len(search_results_json)
            page += 1
            search_url = f"s={search_string}&page={page}"
            resp = self.sess.get(self.base_url + search_url)
            if resp.status_code != 200 or resp.json()["Response"] == "False":
                break
            search_results_json = resp.json()["Search"]

        return result

    def retrieve_movie_by_id(self, imdb_id):
        """
        Use to obtain a Movie object representing the movie identified by
        the supplied imdb_id
        """
        movie_url = self.base_url + f"i={imdb_id}&plot=full"

        resp = self.sess.get(movie_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        if data["Response"] == "False":
            raise ValueError(f'Error retrieving results: \'{data["Error"]}\' ')

        movie = Movie(data, detailed=True)

        return movie


class Coin(object):
    def __init__(self, coin_json, detailed=False):
        if detailed:
            self.marketCapRank = coin_json["market_cap_rank"]
            self.description = coin_json["description"]['en']
            self.price = coin_json['market_data']['current_price']['usd']

        self.id = coin_json['id']
        self.symbol = coin_json['symbol']
        self.name = coin_json['name']
        if detailed:
            self.icon = coin_json['image']['large']
        else: 
            self.icon = coin_json['image']
        

    def __repr__(self):
        return self.id


class CoinClient():
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = 'https://api.coingecko.com/api/v3/'

    
    # We can offer to reduce the number of coins being shown - as the search field!
    def displayAllCoins(self, search_val):
        """
        Displays all the coins that are available
        """
        searchVal = str(search_val)
        search_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={searchVal}&page=1&sparkline=false"

        resp = self.sess.get(search_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()
        result = []
        for item_json in data:
            result.append(Coin(item_json))

        return result

    def getCoin(self, coin_id):
        searchVal = str(coin_id)
        search_url = f'https://api.coingecko.com/api/v3/coins/{searchVal}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'
        
        resp = self.sess.get(search_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()
        result = Coin(data, True)
        return result

## -- Example usage -- ###
if __name__ == "__main__":
    import os

    client = MovieClient(os.environ.get("OMDB_API_KEY"))

    movies = client.search("guardians")

    for movie in movies:
        print(movie)

    print(len(movies))

