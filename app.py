from flask import Flask, render_template, request, jsonify

from news_api import get_news, get_droplist, get_filtered_articles

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("NewsAPI.html")

@app.route("/search", methods=["POST"])
def search():
    selected_date = request.form["date"]
    selected_category = request.form["categories"]
    selected_sources = request.form["sources"]
    input_keywords = request.form["keywords"]

    article_search = get_news(selected_date, selected_category, selected_sources, input_keywords)

    print("Input Date:",selected_date)
    print("Input Category:",selected_category)
    print("Selected Source:",selected_sources)
    print("Listed Keywords:",input_keywords)


    return article_search.to_json(orient="records")



@app.route("/keyword-filter", methods=["POST"])
def keyword_exclusion():

    input_keyword_add = request.form["keyword-add"]
    input_keyword_drop = request.form["keyword-drop"]

    keyword_exclusion_list = get_droplist(input_keyword_add, input_keyword_drop)

    print("Keyword Add Input:",input_keyword_add)
    print("Keyword Drop Input:",input_keyword_drop)

    filtered_articles = get_filtered_articles()

    filtered_articles = filtered_articles.astype(object).where(
        filtered_articles.notna(),
        None
    )

    print("Keyword Exclusion List:")
    print(keyword_exclusion_list)

    print("Filtered Articles:")
    print(filtered_articles)

    
    return jsonify({
        "keyword_exclusion_list": keyword_exclusion_list,
        "articles": filtered_articles.to_dict(orient="records")
    })
   



@app.route("/keyword-remove", methods=["POST"])
def keyword_remove():

    print("KEYWORD REMOVE FUNCTION CALLED")

    keyword = request.form["keyword"]

    print("Keyword Received:",keyword)

    keyword_exclusion_list = get_droplist("", keyword)

    filtered_articles = get_filtered_articles()


    return jsonify({
           "keyword_exclusion_list": keyword_exclusion_list,
           "articles": filtered_articles.to_dict(orient="records")
       })






if __name__ == "__main__":
    app.run(debug=True)