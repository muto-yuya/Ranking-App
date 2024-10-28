"""Flask views.

storing flask views
"""

from flask import redirect, render_template, request, url_for
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
from flask_practice.models.models import Game, GameItem, Item, ItemCategory

INTEGERFIELD_ID = "id"
STRINGFIELD_ITEM_NAME = "item_name"
STRINGFIELD_PLACE = "place"
INTEGERFIELD_PPRICE = "price"
STRINGFIELD_ITEM_IMAGE = "item_image"
BOOLEANFIELD_IS_OPENED = "is_opened"
BOOLEANFIELD_IS_DELETED = "is_deleted"
RANKINGFORM_ITEMS = "items"
RANKINGFORM_ADDLINE = "addline"
RANKINGFORM_SUBMIT = "submitform"
STRINGFIELD_ITEM_CATEGORY_NAME = "item_category_name"


class ItemForm(FlaskForm):
    """編集用"""

    class Meta:
        """Disabling csrf"""

        csrf = False

    id = IntegerField(INTEGERFIELD_ID)
    item_name = StringField(STRINGFIELD_ITEM_NAME, validators=[InputRequired()])
    place = StringField(STRINGFIELD_PLACE, validators=[InputRequired()])
    price = IntegerField(INTEGERFIELD_PPRICE)
    item_image = StringField(STRINGFIELD_ITEM_IMAGE)
    is_deleted = BooleanField(BOOLEANFIELD_IS_DELETED)


class ItemEditForm(FlaskForm):
    """編集用"""

    items = FieldList(FormField(ItemForm, "Item"))
    submitform = SubmitField("保存")
    addline = SubmitField("行追加")

    def self_addline(self):
        """Function for adding new row"""
        # read the data in the form
        read_form_data = self.data

        # updated_list to be seen after reloading
        updated_list = read_form_data.get(RANKINGFORM_ITEMS)

        # add row if addline buttton clicked
        if read_form_data.get(RANKINGFORM_ADDLINE):
            updated_list.append({})

        # reload the form from the modified data
        read_form_data[RANKINGFORM_ITEMS] = updated_list
        self.__init__(formdata=None, **read_form_data)
        self.validate()


@app.route("/")
def category_list():
    """Show ranking list page"""
    item_categories = ItemCategory.query.all()
    return render_template(
        "category_list.html",
        item_categories=item_categories,
        game_create_url="game_create",
    )


@app.route("/game_create/<int:item_category_id>")
def game_create(item_category_id):
    """Create a game and redirect to the created game"""
    # Game作成
    item_category = ItemCategory.query.get(item_category_id)
    game = Game(item_category_id=item_category.id)
    db.session.add(game)
    db.session.commit()

    # GameItem作成
    items = Item.query.filter(
        Item.item_category_id == game.item_category_id,
        Item.is_deleted == False,
    )
    for item in items:
        game_item = GameItem(
            game_id=game.id,
            item_id=item.id,
            is_opened=False,
        )
        db.session.add(game_item)
    db.session.commit()
    return redirect(url_for(game_show.__name__, game_id=game.id))


@app.route("/games/<int:game_id>")
def game_show(game_id):
    """Show items in the game"""
    game = Game.query.get(game_id)
    game_items = game.game_items

    return render_template(
        "game.html",
        item_category=game.item_category,
        game_items=game_items,
        category_list_url=url_for(category_list.__name__),
        game_history_url=url_for(game_history.__name__, game_id=game.id),
    )


@app.route("/games/game_history/<int:game_id>")
def game_history(game_id):
    """Show ranking history in the game"""
    game = Game.query.get(game_id)
    opened_game_items = [
        game_item for game_item in game.game_items if game_item.is_opened
    ]
    return render_template(
        "history.html",
        game_items=opened_game_items,
        game_url=url_for(game_show.__name__, game_id=game.id),
    )


@app.route("/update_is_open_ajax", methods=["POST"])
def update_is_open_ajax():
    """Update is open status through Ajax"""
    print(request.form)
    message = ""
    if request.method == "POST":
        try:
            game_item_id_to_open = request.form["item_id_to_open"]
            game_item = GameItem.query.get(game_item_id_to_open)
            game_item.is_opened = True
            db.session.commit()
            message = "update_is_open_ajax completed"
        except Exception as e:
            print(e)
            message = "update_is_open_ajax failed"
    return message


@app.route("/edit_items/<int:item_category_id>", methods=["POST", "GET"])
def edit_items(item_category_id):
    """Edit items in a category page"""
    item_category = ItemCategory.query.get(item_category_id)
    items_db = Item.query.filter(
        Item.item_category_id == item_category.id,
        Item.is_deleted == False,
    )

    ranking_form = ItemEditForm(
        items=items_db,
        edit_cancel_url=url_for(edit_items.__name__, item_category_id=item_category.id),
    )

    # 行追加ボタンが押された時
    if ranking_form.data.get(RANKINGFORM_ADDLINE):
        ranking_form.self_addline()

    # 保存ボタンが押された時
    if (
        ranking_form.data.get(RANKINGFORM_SUBMIT)
        and ItemEditForm().validate_on_submit()
    ):
        items_form = ranking_form.data.get(RANKINGFORM_ITEMS)
        item_ids_db = [item_db.id for item_db in items_db]
        item_ids_form = [item_form.get(INTEGERFIELD_ID) for item_form in items_form]

        # 既存更新または新規追加のループ
        for item_form in items_form:
            # フォームからの情報取得
            item_id_form = item_form.get(INTEGERFIELD_ID)
            item_name_form = item_form.get(STRINGFIELD_ITEM_NAME)
            price_form = item_form.get(INTEGERFIELD_PPRICE)
            place_form = item_form.get(STRINGFIELD_PLACE)
            item_image_form = item_form.get(STRINGFIELD_ITEM_IMAGE)

            if item_id_form is None:
                # 新規で追加されている場合は、Item作成する
                item_new = Item(
                    item_name=item_name_form,
                    price=price_form,
                    place=place_form,
                    item_category_id=item_category.id,
                    item_image=item_image_form,
                )
                db.session.add(item_new)
            else:
                # 既存のアイテムが更新されている場合→Item更新する
                item_db = Item.query.filter(Item.id == item_id_form).first()
                item_db.item_name = item_name_form
                item_db.price = price_form
                item_db.place = place_form
                item_db.item_image = item_image_form

        # 既存削除のループ
        for item_id_db in item_ids_db:
            if item_id_db not in item_ids_form:
                item_db = Item.query.filter(Item.id == item_id_db).first()
                item_db.is_deleted = True

        db.session.commit()
    return render_template("edit_items.html", ranking_form=ranking_form)
