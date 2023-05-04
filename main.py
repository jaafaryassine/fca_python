from flask import Flask, jsonify
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import joblib
import sklearn
import html5lib
import numpy as np
from functions import *

app = Flask(__name__)

@app.route('/api/predict-score/<teamA>/<teamB>', methods=['GET'])
def perdictScore(teamA,teamB):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://understat.com/league/EPL")
        html = driver.page_source
        data = pd.read_html(html)
        df = pd.DataFrame(data[0])
        driver.quit()
        df.xG = df.xG.apply(lambda xG: correctValue(xG))
        df.xGA = df.xGA.apply(lambda xGA: correctValue(xGA))
        df.xG = df.xG.astype(float)
        df.xGA = df.xGA.astype(float)
        df["xG"] = df["xG"] / df["M"]
        df["xGA"] = df["xGA"] / df["M"]
        df = df[['Team', 'xG', 'xGA']]
        hxG = df[df["Team"] == teamA]["xG"].iloc[0]
        hxGA = df[df["Team"] == teamA]["xGA"].iloc[0]
        axG = df[df["Team"] == teamB]["xG"].iloc[0]
        axGA = df[df["Team"] == teamB]["xGA"].iloc[0]

        infos = np.array([hxG, hxGA, axG, axGA])
        infos = infos.reshape(1, -1)
        model = joblib.load("predict_score_model.joblib")
        score = model.predict(infos)[0]
        switcher = {
            0: "Draw",
            1: "Home",
            2: "Away",
        }
        return jsonify({"result": switcher[score]})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/stats-league/<league>', methods=['GET'])
def getStats(league):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://understat.com/league/" + league)
        html = driver.page_source
        data = pd.read_html(html)
        df = pd.DataFrame(data[0])
        driver.quit()
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": "Sorry ! The website where we scrap data is not available now ! Come back soon"})



# start the app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8005)
