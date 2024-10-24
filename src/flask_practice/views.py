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
from flask_practice.models.models import Item, ItemCategory

STRINGFIELD_ITEM_NAME = "item_name"
STRINGFIELD_PLACE = "place"
INTEGERFIELD_PPRICE = "price"
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
    """Show ranking list page"""
    item_categories = ItemCategory.query.all()
    print(item_categories)
    return render_template(
        "ranking_list.html",
        item_categories=item_categories,
        ranking_url=ranking.__name__,
    )


@app.route("/rankings/<int:item_category_id>")
def ranking(item_category_id):
    """Show ranking page"""
    item_category = ItemCategory.query.get(item_category_id)
    items = item_category.items
    print(item_category.item_category_name)
    print(items)
    return render_template(
        "ranking.html",
        item_category=item_category,
        items=items,
        ranking_list_url=url_for(ranking_list.__name__),
        ranking_history_url=url_for(
            ranking_history.__name__, item_category_id=item_category.id
        ),
    )


@app.route("/ranking-history/<int:item_category_id>")
def ranking_history(item_category_id):
    """Show ranking history in the game"""
    item_category = ItemCategory.query.get(item_category_id)
    items = Item.query.filter(
        Item.item_category_id == item_category.id, Item.is_opened
    ).order_by(Item.place)
    return render_template(
        "ranking_history.html",
        items=items,
        ranking_url=url_for(ranking.__name__, item_category_id=item_category.id),
    )


@app.route("/edit_ranking/<int:item_category_id>", methods=["POST", "GET"])
def edit_ranking(item_category_id):
    """Edit ranking page"""
    item_category = ItemCategory.query.get(item_category_id)
    items = Item.query.filter(Item.item_category_id == item_category.id)
    ranking_form = RankingForm(
        items=items,
        edit_cancel_url=url_for(
            edit_ranking.__name__, item_category_id=item_category.id
        ),
    )
    print("validate_on_submit before")
    print(ranking_form.data)

    if ranking_form.data[RANKINGFORM_ADDLINE]:
        ranking_form.update_self()

    if ranking_form.data[RANKINGFORM_SUBMIT] and RankingForm().validate_on_submit():
        print("validate_on_submit after")
        # Clear DB
        Item.query.filter(Item.item_category_id == item_category.id).delete()

        # update DB with entered values in ranking form
        for item in ranking_form.data[RANKINGFORM_ITEMS]:
            ranking = Item(
                item_name=item.get(STRINGFIELD_ITEM_NAME),
                price=item.get(INTEGERFIELD_PPRICE),
                place=item.get(STRINGFIELD_PLACE),
                item_category_id=item_category.id,
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
            item = Item.query.get(item_id_to_open)
            item.is_opened = True
            db.session.commit()
            message = "update_is_open_ajax completed"
        except Exception as e:
            print(e)
            message = "update_is_open_ajax failed"
    return message
