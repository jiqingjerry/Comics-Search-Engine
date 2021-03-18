from flask import Flask, render_template, request
from pymongo import MongoClient
import os
import json

app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://CS242jzhu:CS242jzhu0305@cluster0.2gehc.mongodb.net/test?retryWrites=true&w=majority')
db = client['images']
collection = db['test_collection']


@app.route('/', methods=['GET', 'POST'])
def index():
    if len(request.form) > 0:
        img_data = []
        print(request.form['search method'])
        if request.form['search method'] == "amazon":
            searchQuery = "curl -XGET -u \"bent:CS242bt123$\" \"https://search-cs242-demo-sex65drkn7zjhbwdqtpbkk6zum.us" \
                          "-west-1.es.amazonaws.com/images/_search?q="
            searchQuery += request.form["query"].replace(" ", "%20")
            searchQuery += "&pretty=true\""
            print(searchQuery)

            results = os.popen(searchQuery).read()

            x = json.loads(results)
            s = x["hits"]["hits"]

            # This list will contain an ordered list of image IDs to be returned
            image_titles = []

            for i in s:
                image_titles.append(i["_source"]["title"])
            print(image_titles)
            for i in image_titles:
                print(i)
                cur_result = collection.find_one({"title": i})
                if cur_result:
                    img_data.append(cur_result)
        else:
            # img_data = list(collection.find({"title": {"$in": list(request.form["query"].split(' '))}}).limit(10))
            query_words = list(request.form["query"].split(' '))
            new_query = ".*".join(query_words)
            img_data = list(collection.find({"title": {"$regex": new_query}}).limit(10))
            for i in img_data:
                print(i['title'])
        return render_template('index.html', query=request.form["query"], results=img_data, index=request.form['search method'])
    return render_template('index.html', name="no results found")

app.run('127.0.0.1', debug=True)
