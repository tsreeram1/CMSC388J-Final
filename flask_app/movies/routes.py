from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client, coin_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time

movies = Blueprint("movies", __name__)

@movies.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        try:
            results = coin_client.displayAllCoins(form.search_query.data)
            return render_template("query.html", results=results)
        except ValueError as e: 
            flash(str(e))
    return render_template("index.html", form=form)


@movies.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = movie_client.search(query)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("movies.index"))

    return render_template("query.html", results=results)


@movies.route("/movies/<movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = coin_client.getCoin(movie_id)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    return render_template("movie_detail.html", coin=result)


@movies.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)