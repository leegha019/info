from db_connection import connection_handler


@connection_handler
def add_login(cursor, user_data):
    query = ''' INSERT INTO logins (email,pass,date)
                VALUES (%(email)s,%(pass)s,%(date)s)    '''
    cursor.execute(query,user_data)



@connection_handler
def is_in_session(cursor, email):
    query = ''' SELECT COUNT(email) as session FROM logins
                WHERE email=%(email)s   '''
    params = {'email':email}
    cursor.execute(query,params)
    return cursor.fetchone()['session'] == 1