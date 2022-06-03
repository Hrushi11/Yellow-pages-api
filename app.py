from yellow_pages_api_call import Scrape
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/yellow-pages-api")
def api():
    scrape = Scrape("https://www.yellowpages.com/las-vegas-nv/restaurants")
    arr = scrape.scrape_web()

    return jsonify([arr][0])

if __name__ == "__main__":
    app.run()
