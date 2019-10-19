import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def post_fact():

    url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    text = get_fact()
    payload = {'input_text': text}
    resp = requests.post(url, data=payload, allow_redirects=False)
    if resp.status_code == 302:
        try:
            return resp.headers['Location']
        except KeyError as e:
            raise NameError
    else:
        return ''

@app.route('/')
def home():
    try:
        url = post_fact()
    except NameError:
        url = "Not found"
    return url


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

