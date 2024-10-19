"""Flask views.

storing flask views
"""

from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, StringField, SubmitField

from flask_practice import app, db
from flask_practice.models.ranking import Ranking

STRINGFIELD_ITEM_NAME = "item_name"
STRINGFIELD_PLACE = "place"
STRINGFIELD_RANKING_CATEGORY = "ranking_category"
STRINGFIELD_ITEM_IMAGE = "item_image"
BOOLEANFIELD_IS_DELETED = "is_deleted"


class ItemForm(FlaskForm):
    """ranking row for edit"""

    class Meta:
        """Disabling csrf"""

        csrf = False

    item_name = StringField(STRINGFIELD_ITEM_NAME)
    place = StringField(STRINGFIELD_PLACE)
    ranking_category = StringField(STRINGFIELD_RANKING_CATEGORY)
    item_image = StringField(STRINGFIELD_ITEM_IMAGE)
    is_deleted = BooleanField(BOOLEANFIELD_IS_DELETED, default="")


class RankingForm(FlaskForm):
    """ranking list form for edit"""

    items = FieldList(FormField(ItemForm, "Item"))
    """
    FieldlistとFormFieldを用いて子フォーム複製
    """
    submit = SubmitField("送信")
    addline = SubmitField("Add new line")

    def update_self(self):
        """Function for adding new row"""
        # read the data in the form
        read_form_data = self.data
        print(read_form_data)
        # modify the data as you see fit:
        updated_list = read_form_data["items"]

        if read_form_data["addline"]:
            updated_list.append({})

        if read_form_data["submit"]:
            updated_list_delete_row = updated_list
            updated_list = []
            for item in updated_list_delete_row:
                if not item.get(BOOLEANFIELD_IS_DELETED):
                    updated_list.append(item)

        read_form_data["items"] = updated_list
        # reload the form from the modified data
        self.__init__(formdata=None, **read_form_data)
        self.validate()


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
        form_item_name = request.form.get(STRINGFIELD_ITEM_NAME)  # str
        form_place = request.form.get(STRINGFIELD_PLACE)  # str
        form_ranking_category = request.form.get(
            STRINGFIELD_RANKING_CATEGORY, default="kurasuhi"
        )  # str
        form_item_image = request.form.get(STRINGFIELD_ITEM_IMAGE, default="")  # str
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
    items = Ranking.query.all()
    ranking_form = RankingForm(items=items)

    if RankingForm().validate_on_submit():
        ranking_form.update_self()  # This reloads the form with the processed data
        for item in ranking_form.items:
            print(item.data)
            print(item.data[BOOLEANFIELD_IS_DELETED])
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
