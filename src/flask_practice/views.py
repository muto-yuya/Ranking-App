"""Flask views.

storing flask views
"""

from flask import render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FieldList,
    FormField,
    IntegerField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired

from flask_practice import app, db
from flask_practice.models.ranking import Ranking

STRINGFIELD_ITEM_NAME = "item_name"
STRINGFIELD_PLACE = "place"
INTEGERFIELD_PPRICE = "price"
STRINGFIELD_RANKING_CATEGORY = "ranking_category"
STRINGFIELD_ITEM_IMAGE = "item_image"
BOOLEANFIELD_IS_OPENED = "is_opened"
BOOLEANFIELD_IS_DELETED = "is_deleted"
RANKINGFORM_ITEMS = "items"
RANKINGFORM_ADDLINE = "addline"
RANKINGFORM_SUBMIT = "submitform"


class ItemForm(FlaskForm):
    """ranking row for edit"""

    class Meta:
        """Disabling csrf"""

        csrf = False

    item_name = StringField(STRINGFIELD_ITEM_NAME, validators=[InputRequired()])
    place = StringField(STRINGFIELD_PLACE, validators=[InputRequired()])
    price = IntegerField(INTEGERFIELD_PPRICE)
    ranking_category = StringField(STRINGFIELD_RANKING_CATEGORY)
    item_image = StringField(STRINGFIELD_ITEM_IMAGE)
    is_opened = BooleanField(BOOLEANFIELD_IS_OPENED)


class RankingForm(FlaskForm):
    """ranking list form for edit"""

    items = FieldList(FormField(ItemForm, "Item"))
    submitform = SubmitField("保存")
    addline = SubmitField("行追加")

    def update_self(self):
        """Function for adding new row"""
        # read the data in the form
        read_form_data = self.data

        # updated_list to be seen after reloading
        updated_list = read_form_data[RANKINGFORM_ITEMS]

        # add row if addline buttton clicked
        if read_form_data[RANKINGFORM_ADDLINE]:
            updated_list.append({})

        # reload the form from the modified data
        read_form_data[RANKINGFORM_ITEMS] = updated_list
        self.__init__(formdata=None, **read_form_data)
        self.validate()


@app.route("/rankings")
def ranking_list():
    """Show ranking page"""
    items = Ranking.query.all()
    print(items)
    print(items[0].is_opened)
    return render_template(
        "ranking_list.html",
        items=items,
        ranking_history_url=url_for(ranking_history.__name__),
    )


@app.route("/ranking-history")
def ranking_history():
    """Show ranking history in the game"""
    items = Ranking.query.all()
    items = db.session.query(Ranking).filter(Ranking.is_opened).order_by(Ranking.place)
    print(items)
    return render_template(
        "ranking_history.html",
        items=items,
        ranking_list_url=url_for(ranking_list.__name__),
    )


@app.route("/edit_ranking", methods=["POST", "GET"])
def edit_ranking():
    """Edit ranking page"""
    items = Ranking.query.all()
    ranking_form = RankingForm(
        items=items, edit_cancel_url=url_for(edit_ranking.__name__)
    )
    print("validate_on_submit before")
    print(ranking_form.data)

    if ranking_form.data[RANKINGFORM_ADDLINE]:
        ranking_form.update_self()

    if ranking_form.data[RANKINGFORM_SUBMIT] and RankingForm().validate_on_submit():
        print("validate_on_submit after")
        # Clear DB
        db.session.query(Ranking).delete()

        # update DB with entered values in ranking form
        for item in ranking_form.data[RANKINGFORM_ITEMS]:
            ranking = Ranking(
                item_name=item.get(STRINGFIELD_ITEM_NAME),
                price=item.get(INTEGERFIELD_PPRICE),
                place=item.get(STRINGFIELD_PLACE),
                ranking_category=item.get(STRINGFIELD_RANKING_CATEGORY),
                item_image=item.get(STRINGFIELD_ITEM_IMAGE),
                is_opened=item.get(BOOLEANFIELD_IS_OPENED),
            )
            db.session.add(ranking)
        db.session.commit()
    return render_template("edit-ranking.html", ranking_form=ranking_form)


@app.route("/update_is_open_ajax", methods=["POST"])
def update_is_open_ajax():
    """Update is open status through Ajax"""
    message = ""
    if request.method == "POST":
        try:
            item_id_to_open = request.form["item_id_to_open"]
            item = Ranking.query.get(item_id_to_open)
            item.is_opened = True
            db.session.commit()
            message = "update_is_open_ajax completed"
        except Exception as e:
            print(e)
            message = "update_is_open_ajax failed"
    return message
