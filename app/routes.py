import datetime as dt
from flask import render_template, request, redirect, url_for
from app import app
from app.models import Todo
from app.forms import AddForm
from app import db


@app.route('/')
def index():
    todos = Todo.query.filter_by(completed=False).all()
    current_time = dt.datetime.utcnow()
    todo_timediff = []
    for todo in todos:
        if isinstance(todo.deadline, dt.datetime):
            x = todo.deadline - current_time
            todo_timediff.append((todo, x.total_seconds()))
        else:
            todo_timediff.append((todo, 3600))
    count = len(todo_timediff)
    return render_template(
        "index.html",
        todos=todo_timediff,
        count=count,
        title="Todos Overview"
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        utc_diff = form.time_offset.data

        if form.deadline.data is not None:
            utc_time = form.deadline.data + dt.timedelta(minutes=int(utc_diff))
        else:
            utc_time = None

        task = Todo(
            title=form.title.data,
            desc=form.desc.data,
            deadline=utc_time,
            utc_offset=utc_diff,
        )
        db.session.add(task)
        db.session.commit()

        return redirect(url_for("todo_detail",
                                id=task.id))
    return render_template("add.html",
                           title="Add todo",
                           form=form)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_todo(id):
    form = AddForm()
    todo = Todo.query.get(id)
    if form.validate_on_submit():
        utc_diff = form.time_offset.data
        if form.deadline.data is not None:
            utc_time = form.deadline.data + dt.timedelta(minutes=int(utc_diff))
        else:
            utc_time = None
        todo.title = form.title.data
        todo.desc = form.desc.data
        if utc_time is not None:
            todo.deadline = utc_time
        else:
            todo.deadline = None
        db.session.commit()
        return redirect(url_for("todo_detail",
                                id=todo.id))
    elif request.method == "GET":
        form.title.data = todo.title
        form.desc.data = todo.desc
        if todo.deadline is not None:
            time_limit = todo.deadline - dt.timedelta(minutes=todo.utc_offset)
            time_limit.strftime(format="%d.%m.%Y %H:%M")
            form.deadline.data = time_limit
    return render_template("edit.html",
                           title="Edit todo",
                           form=form,
                           todo=todo)


@app.route("/todo/<id>", methods=["GET"])
def todo_detail(id):
    todo = Todo.query.get(id)
    return render_template("todo.html",
                           title=todo.title,
                           todo=todo)


@app.route("/completed/<id>", methods=["GET", "POST"])
def todo_finished(id):
    todo = Todo.query.get(id)
    todo.completed_todo()
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/completed", methods=["GET", "POST"])
def completed_todo():
    todos = Todo.query.filter_by(completed=True)
    for todo in todos:
        print(todo.completed_time)
    count = todos.count()
    return render_template(
        "completed.html",
        count=count,
        todos=todos,
        title="Finished todo"
    )


@app.route("/uncomplited/<id>", methods=["GET", "POST"])
def todo_uncompleted(id):
    todo = Todo.query.get(id)
    todo.no_complited_todo()
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("todo_detail", id=todo.id))


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


"""

@bp.route("/unfinished/<id>", methods=["GET", "POST"])
@login_required
def task_unfinished(id):
    task = Task.query.get(id)
    if task is None or task.author != current_user:
        flash("There is no such task.")
        return redirect(url_for("main.index"))
    task.mark_unfinished()
    db.session.add(task)
    db.session.commit()
    flash("Task marked as unfinished")
    return redirect(url_for("main.task_detail", id=task.id))


"""
