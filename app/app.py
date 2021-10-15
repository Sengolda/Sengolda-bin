from flask import Flask, render_template, request, abort
from flask.helpers import url_for
import pymongo
import random
import config

app = Flask(__name__)
mongo_cluster = pymongo.MongoClient(config.mongo_db_url)
db = mongo_cluster['projects']
col = db['pastes']

@app.route("/", methods=["GET", "POST"])
def hello():
    rand_num = random.randrange(1, 10000)
    to_paste = request.form.get("code")
    col.update_one(
        {"_id": rand_num},
        {"$set": {"content": to_paste}},
        upsert=True,
    )

    return render_template("index.html", paste_url=url_for("paste", id=rand_num))

@app.route("/paste/<int:id>")
def paste(id):
    val = col.find({"_id": id})
    if not val:
        abort(404)
    

    v = val[0]
    return str(v.get("content"))


def run():
    app.run(debug=True)
