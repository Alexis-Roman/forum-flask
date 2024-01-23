from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)



class Topic(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(unique=True)
    topicID: Mapped[str]

with app.app_context():
    db.create_all()

@app.route("/" , methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Add a new Topic
        topic = Topic(
            title=request.form["title"],
            description=request.form["description"],
        )
        db.session.add(topic)
        db.session.commit()
    topics = db.session.execute(db.select(Topic)).scalars()
    # for topic in topics:
    #     print(topic.title, topic.description, topic.id)
    return render_template("index.html", topics=topics)

@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        # Add a new Comment to the topic
        comment = Comment(
            text=request.form["comment"],
            topicID=id
        )
        db.session.add(comment)
        db.session.commit()

        #Pull topic and comments
    topic = db.get_or_404(Topic, id)
    comments = Comment.query.filter_by(topicID=id).all()
    # print(comments)
    # for comment in comments:
    #     print(comments)
    return render_template("Forum-Clicked.html", topic=topic, comments=comments)
    



app.run(debug=True, port=5001)