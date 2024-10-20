"""ranking model"""

from datetime import datetime

from flask_practice import db


class Ranking(db.Model):
    """storing ranking records regardless of ranking category"""

    __tablename__ = "ranking"
    id = db.Column(db.Integer, primary_key=True)  # system use
    item_name = db.Column(db.String(255))  # product name
    place = db.Column(db.Integer)  # place in the ranking category
    price = db.Column(db.Integer)
    ranking_category = db.Column(db.String(255))  # ranking category ex. mcdonalds
    item_image = db.Column(db.String(2048))  # item image
    is_opened = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )  # 作成日時
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )  # 更新日時
