from flask import Flask, request, redirect
from Article import Article
import sqlite3

def add_article(title, message, cur, conn):
    id = "0"
    cur.execute("SELECT id FROM Articles")
    records = cur.fetchall()
    records = sorted(records)
    for row in records:
        id = row[0]
    id = str(int(id) + 1)
    cur.execute("INSERT INTO Articles(id, title, message) VALUES('" + id + "', '" + title + "', '" + message + "')")
    conn.commit()

def show_articles(conn, cur):
    cur.execute("SELECT * FROM Articles")
    records = cur.fetchall()
    out = ""
    file = open("./Articles/template_header.html", 'r')
    for string in file:
        out += string
    file.close()
    articles = []
    for record in records:
        id = record[0]
        message = record[2]
        name = record[1]
        articles.append({"message":message, "name":name, "id":id})
    cur.close()
    file = open("./Articles/template_news.html", 'r')
    template = ""
    for string in file:
        template += string
    file.close()
    for article in articles:
        tmp = template.replace("###name###", article["name"])
        tmp = tmp.replace("###message###", article["message"])
        tmp = tmp.replace("###id###", article["id"])
        out += tmp
    file = open("./Articles/template_form.html", "r")
    for string in file:
        out += string
    file.close()
    return out

def save_file(id, title, message, cur, conn):
    cur.execute("UPDATE Articles SET message = '" + message + "', title = '" + title + "' WHERE id = '" + id + "'")
    conn.commit()

def delete_file(id, cur, conn):
    cur.execute("DELETE FROM Articles WHERE id = '" + id + "'")
    conn.commit()

####################################################
def clear_file():
    file = open("registration.db", 'w')
    file.write("")
    file.close()
####################################################
app = Flask(__name__)
articles = [Article("Привет", "Первое сообщение"),
            Article("Погода", "Сегодня холодно")]

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('registration.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Articles(
        id TEXT,
        title TEXT,
        message TEXT);
    """)
    conn.commit()
    if request.method == "POST":
        if request.form["act"] == "save":
            save_file(request.form["id"], request.form["name"], request.form["message"], cur, conn)
        elif request.form["act"] == "delete":
            delete_file(request.form["id"], cur, conn)
        elif request.form["act"] == "add" and request.form["name"].strip() != "" and request.form["message"].strip() != "":
            add_article(request.form["name"], request.form["message"], cur, conn)
    #return "Hello, world!"
    return show_articles(conn, cur)


@app.route("/add_comment/<int:id>", methods=["POST"])
def add_comment(id):
    for article in articles:
        if article.get_id() == id:
            article.add_comment(request.form['title'],
                                request.form['content'])
            break
    return redirect('/')
#clear_file()
app.run(port=5000)