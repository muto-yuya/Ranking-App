"""Item model"""

from datetime import datetime

from flask_practice import db


class Item(db.Model):
    """storing ranking records regardless of ranking category"""

    __tablename__ = "Item"
    id = db.Column(db.Integer, primary_key=True)  # system use
    item_name = db.Column(db.String(255))  # 商品名
    place = db.Column(db.Integer, nullable=False, default="NA")  # 商品の順位
    price = db.Column(db.Integer, nullable=False, default="NA")  # 商品の価格
    item_category_id = db.Column(
        db.Integer, db.ForeignKey("ItemCategory.id"), nullable=False
    )  # アイテムカテゴリのID
    item_image = db.Column(db.String(2048), nullable=True)  # 商品の画像
    is_opened = db.Column(
        db.Boolean, default=False, nullable=False
    )  # 順位確認済みフラグ
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )  # 作成日時
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )  # 更新日時


class ItemCategory(db.Model):
    """Item category such as kurasushi or mcdonalds"""

    __tablename__ = "ItemCategory"
    id = db.Column(db.Integer, primary_key=True)  # system use
    item_category_name = db.Column(db.String(255))  # カテゴリ名
    items = db.relationship("Item", backref="item_category")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )  # 作成日時
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )  # 更新日時
