"""Flask views.

storing flask views
"""

from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, StringField, SubmitField
from wtforms.validators import InputRequired

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

    item_name = StringField(STRINGFIELD_ITEM_NAME, validators=[InputRequired()])
    place = StringField(STRINGFIELD_PLACE, validators=[InputRequired()])
    ranking_category = StringField(STRINGFIELD_RANKING_CATEGORY)
    item_image = StringField(STRINGFIELD_ITEM_IMAGE)
    is_deleted = BooleanField(BOOLEANFIELD_IS_DELETED, default="")


class RankingForm(FlaskForm):
    """ranking list form for edit"""

    items = FieldList(FormField(ItemForm, "Item"))
    submit = SubmitField("送信")
    addline = SubmitField("Add new line")

    def update_self(self):
        """Function for adding new row"""
        # read the data in the form
        read_form_data = self.data

        # updated_list to be seen after reloading
        updated_list = read_form_data["items"]

        # add row if addline buttton clicked
        if read_form_data["addline"]:
            updated_list.append({})

        # update item list removing deleted rows
        if read_form_data["submit"]:
            updated_list_delete_row = updated_list
            updated_list = []
            for item in updated_list_delete_row:
                if not item.get(BOOLEANFIELD_IS_DELETED):
                    updated_list.append(item)

        # reload the form from the modified data
        read_form_data["items"] = updated_list
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
    """Show ranking page"""
    items = Ranking.query.all()
    return render_template("ranking_list.html", rankings=items)


@app.route("/edit_ranking", methods=["POST", "GET"])
def ranking_edit():
    """Edit ranking page"""
    items = Ranking.query.all()
    ranking_form = RankingForm(items=items)

    if RankingForm().validate_on_submit():
        # This reloads the form with the editted values/added rows/deleted rows
        ranking_form.update_self()

        # Clear DB
        db.session.query(Ranking).delete()

        # update DB with entered values in ranking form
        print(ranking_form.data)
        for item in ranking_form.data["items"]:
            ranking = Ranking(
                item_name=item.get(STRINGFIELD_ITEM_NAME),
                place=item.get(STRINGFIELD_PLACE),
                ranking_category=item.get(STRINGFIELD_RANKING_CATEGORY),
                item_image=item.get(STRINGFIELD_ITEM_IMAGE),
            )
            db.session.add(ranking)
        db.session.commit()

    return render_template("edit-ranking.html", ranking_form=ranking_form)
