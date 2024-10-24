"""Refresh DB"""

from flask_practice import app, db
from flask_practice.models.models import Item, ItemCategory

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        item_category1 = ItemCategory(item_category_name="くら寿司")
        item_category2 = ItemCategory(item_category_name="マクドナルド")
        db.session.add(item_category1)
        db.session.add(item_category2)
        db.session.commit()

        item1 = Item(
            item_name="爆盛ねぎまぐろにぎり",
            price="100",
            place="5",
            item_category_id=item_category1.id,
            item_image="https://www.kurasushi.co.jp/menu/upload/bf4c8baeb6e3f4cefe7a076204ae6a663f4ea93f.jpg",
        )

        item2 = Item(
            item_name="ビッくらポン！ 軍艦セット",
            price="690",
            place="10",
            item_category_id=item_category1.id,
            item_image="https://www.kurasushi.co.jp/menu/upload/730f88c0bd3972e0cf978fb4f3ebcd23bcf2c921.jpg",
        )

        item3 = Item(
            item_name="ダブルチーズバーガー",
            price="430",
            place="圏外",
            item_category_id=item_category2.id,
            item_image="https://www.mcdonalds.co.jp/product_images/11/1360-Double-Cheese-Burger.m.webp?20240902092837",
        )
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.commit()
