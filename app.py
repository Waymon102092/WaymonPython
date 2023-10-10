from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from waymon import res

# post request.form.get("")
# get  request.args.get("")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/test"
# 追踪数据库 一般不开启
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


migrate = Migrate(app=app, db=db)


@app.route("/info", methods=["GET"])
def info():
    id = request.args.get("id")
    task = Todo.query.filter(Todo.id == id).first()
    return res(task, "ok", 0)


@app.route("/list", methods=['GET'])
def list():
    page = request.args.get("page")
    print(page)
    size = request.args.get("size")
    print(size)
    tasks = Todo.query.order_by(Todo.pub_date).all()
    return res(tasks, "ok", 0)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        task_content = request.form.get("content")
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return res(None, "ok", 0)
        except:
            return res(None, "err", 1)
    else:
        task_content = request.args.get("content")
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return res(None, "ok", 0)
        except:
            return res(None, "err", 1)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["task"]
        try:
            db.session.commit()
            return res(None, "ok", 0)
        except:
            return res(None, "ok", 1)
    else:
        return res(None, "不支持GET", 2)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return res(data=None, msg="ok", status=0)
    except:
        return res(None, "err", 1)


if __name__ == '__main__':
    app.run(port=5001)
