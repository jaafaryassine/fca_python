from flask import Flask, jsonify
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import html5lib

app = Flask(__name__)


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
    app.run(debug=True, host='127.0.0.1', port=8003)
