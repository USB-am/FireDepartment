
class DBException(Exception):
    ''' Based class for data base exceptions '''


class DBPrimaryKeyError(DBException):
    ''' Data base has row with this primary key argument '''
