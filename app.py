# app.py
from flask import Flask, request, jsonify
import cfscrape
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def Seturl(url, retry=False):
    client = cfscrape.create_scraper(delay=10)
    DOMAIN = "https://set.seturl.in/"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://paisa-king.com/"
    h_get = {"referer": ref}
    h_post = {
        "x-requested-with": "XMLHttpRequest",
        "referer": final_url,
        "content-type": "application/x-www-form-urlencoded"
    }

    try:
        resp = client.get(final_url, headers=h_get)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs if input.get("name")}

        if not data:
            return "No form data found. The page structure might have changed."

        time.sleep(7)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h_post)
        return str(r.json()["url"])
    except BaseException as e:
        if not retry:
            print(f"Error occurred: {e}. Retrying...")
            return Seturl(url, retry=True)
        else:
            return "Something went wrong, Please Wait For Few Seconds and try again..."

@app.route('/seturl', methods=['POST'])
def seturl_endpoint():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400
    url = data['url']
    result = Seturl(url)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
