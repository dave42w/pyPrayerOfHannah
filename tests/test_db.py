#from src.pyPrayerOfHannah.db import DB
#mport pathlib as pl

print("hello test")

def delete_database_test() -> None:
    raise AssertionError(f"Database File hasn't been deleted: {str(path)}")
    '''
    db = DB()
    path: pl.Path = pl.Path(db.DATABASE_FILE)
    if pl.Path(path).resolve().is_file():
        raise AssertionError(f"Database File hasn't been deleted: {str(path)}")
    else:
        raise AssertionError(f"BOGUS Database File hasn't been deleted: {str(path)}")
    '''