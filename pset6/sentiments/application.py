from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    screen_name = screen_name.lstrip("@")

    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if tweets == None:
        return redirect(url_for("index"))

    # sys.path[0] is the directory containing the script that was used to invoke the Python interpreter
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # initialize analyzer like in analyzer.py
    analyzer = Analyzer(positives, negatives)

    # get tweets
    tweets = helpers.get_user_timeline(screen_name, 100)

    if tweets == None or tweets == RuntimeError:
        sys.exit("Error: unable to retrieve tweets")

    # initialize positive, negative, neutral variables
    positive, negative, neutral = 0.0, 0.0, 0.0

    # analyze each tweet
    for tweet in tweets:
        score = analyzer.analyze(tweet)

        if score > 0.0:
            positive += 1
        elif score < 0.0:
            negative += 1
        else:
            neutral += 1

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
