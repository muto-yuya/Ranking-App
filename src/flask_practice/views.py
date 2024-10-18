"""Flask views.

storing flask views
"""

from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SubmitField

from flask_practice import app, db
from flask_practice.models.ranking import Ranking

STRINGFIELD_ITEM_NAME = "item_name"
STRINGFIELD_PLACE = "place"
STRINGFIELD_RANKING_CATEGORY = "ranking_category"
STRINGFIELD_ITEM_IMAGE = "item_image"


class ItemForm(FlaskForm):
    """ranking row for edit"""

    def __init__(self, *args, **kwargs):
        kwargs["csrf_enabled"] = (
            False  # 子フォームではCSRFトークンが生成されないように設定
        )
        super(ItemForm, self).__init__(*args, **kwargs)

    item_name = StringField(STRINGFIELD_ITEM_NAME)
    place = StringField(STRINGFIELD_PLACE)
    ranking_category = StringField(STRINGFIELD_RANKING_CATEGORY)
    item_image = StringField(STRINGFIELD_ITEM_IMAGE)
    delete = SubmitField(label="Delete")


class RankingForm(FlaskForm):
    """ranking list form for edit"""

    items = FieldList(FormField(ItemForm, "Item"))
    """
    FieldlistとFormFieldを用いて子フォーム複製
    """
    submit = SubmitField("送信")


@app.route("/")
def index():
    """Index page"""
    return render_template("index.html")


@app.route("/test")
def other1():
    """TEST page"""
    return "テストページです！"


@app.route("/add_ranking", methods=["GET", "POST"])
def add_ranking():
    """Add ranking page for test"""
    if request.method == "GET":
        return render_template("add_ranking.html")
    if request.method == "POST":
        form_item_name = request.form.get("item_name")  # str
        form_place = request.form.get("place")  # str
        form_ranking_category = request.form.get(
            "ranking_category", default="kurasuhi"
        )  # str
        form_item_image = request.form.get("item_image", default="")  # str
        ranking = Ranking(
            item_name=form_item_name,
            place=form_place,
            ranking_category=form_ranking_category,
            item_image=form_item_image,
        )
        db.session.add(ranking)
        db.session.commit()
        return redirect(url_for("index"))


@app.route("/rankings")
def ranking_list():
    """Show ranking page for test"""
    items = Ranking.query.all()
    return render_template("ranking_list.html", rankings=items)


@app.route("/edit_ranking", methods=["POST", "GET"])
def ranking_edit():
    """Edit ranking page for test"""
    ranking_form = RankingForm()

    if request.method == "GET":
        for item in Ranking.query.all():
            item_form = ItemForm()
            item_form.item_name = item.item_name  # These fields don't use 'data'
            item_form.place = item.place
            item_form.ranking_category = item.ranking_category
            item_form.item_image = item.item_image
            ranking_form.items.append_entry(item_form)
        return render_template("edit-ranking.html", ranking_form=ranking_form)
    if request.method == "POST":
        db.session.query(Ranking).delete()
        for item in ranking_form.data["items"]:
            ranking = Ranking(
                item_name=item[STRINGFIELD_ITEM_NAME],
                place=item[STRINGFIELD_PLACE],
                ranking_category=item[STRINGFIELD_RANKING_CATEGORY],
                item_image=item[STRINGFIELD_ITEM_IMAGE],
            )
            db.session.add(ranking)
        db.session.commit()
        return render_template("edit-ranking.html", ranking_form=ranking_form)
