"""Load a csv file into database."""

import sys
from pathlib import Path

import pandas as pd

from flask_practice import app, db, views
from flask_practice.models.ranking import Ranking


def import_csv(input):
    """Load a csv file into database."""
    input_csv = Path(input).absolute()
    if input_csv.is_file() and input_csv.suffix == ".csv":
        df = pd.read_csv(input_csv, encoding="utf8", sep=",", dtype=str)

        # Clear DB
        db.session.query(Ranking).delete()

        for index, row in df.iterrows():
            ranking = Ranking(
                item_name=row[views.STRINGFIELD_ITEM_NAME],
                price=row[views.INTEGERFIELD_PPRICE],
                place=row[views.STRINGFIELD_PLACE],
                item_image=row[views.STRINGFIELD_ITEM_IMAGE],
            )
            db.session.add(ranking)
        db.session.commit()


if __name__ == "__main__":
    args = sys.argv
    file_name = str(args[1])
    with app.app_context():
        import_csv(file_name)
