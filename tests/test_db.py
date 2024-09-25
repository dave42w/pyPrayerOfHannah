from py_prayer_of_hannah.db import DB
import pathlib as pl


def delete_database_test() -> None:
    db = DB()
    path: pl.Path = pl.Path(db.DATABASE_FILE)
    if pl.Path(path).resolve().is_file():
        raise AssertionError(f"Database File hasn't been deleted: {str(path)}")
    else:
        raise AssertionError(f"BOGUS Database File hasn't been deleted: {str(path)}")