"""Load a csv file into database."""

import sys
from pathlib import Path

import pandas as pd

from flask_practice import app, db, views
from flask_practice.models.models import Item, ItemCategory


def import_csv(input):
    """Load a csv file into database."""
    input_csv = Path(input).absolute()
    if input_csv.is_file() and input_csv.suffix == ".csv":
        df = pd.read_csv(input_csv, encoding="utf8", sep=",", dtype=str)

        item_category_name = df.iloc[0][views.STRINGFIELD_ITEM_CATEGORY_NAME]
        item_category = ItemCategory.query.filter(
            ItemCategory.item_category_name == item_category_name
        )

        if item_category is not None:
            # アイテムカテゴリ名が既存のものと一致すれば、アイテムカテゴリを洗替更新
            item_category = item_category.first()
            Item.query.filter(Item.item_category_id == item_category.id).delete()
            db.session.commit()
        else:
            # アイテムカテゴリ名が既存のものと一致しなければ、アイテムカテゴリを新規作成
            item_category = ItemCategory(item_category_name=item_category_name)
            db.session.add(item_category)
            db.session.commit()

        for index, row in df.iterrows():
            item = Item(
                item_name=row[views.STRINGFIELD_ITEM_NAME],
                price=row[views.INTEGERFIELD_PPRICE],
                place=row[views.STRINGFIELD_PLACE],
                item_category_id=item_category.id,
                item_image=row[views.STRINGFIELD_ITEM_IMAGE],
            )
            db.session.add(item)
        db.session.commit()


if __name__ == "__main__":
    args = sys.argv
    file_name = str(args[1])
    with app.app_context():
        import_csv(file_name)
