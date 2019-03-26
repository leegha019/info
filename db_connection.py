import os
import psycopg2, psycopg2.extras
import urllib



# -------------------------------------FOR REMOTE USE----------------------------------
# def open_database():
#     try:
#         urllib.parse.uses_netloc.append('postgres')
#         url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
#         connection = psycopg2.connect(
#             database=url.path[1:],
#             user=url.username,
#             password=url.password,
#             host=url.hostname,
#             port=url.port
#         )
#         connection.autocommit = True
#     except psycopg2.DatabaseError as exception:
#         print('Database connection problem')
#         raise exception
#     return connection
#
#
#
# def connection_handler(function):
#     def wrapper(*args, **kwargs):
#         connection = open_database()
#         dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#         ret_value = function(dict_cur, *args, **kwargs)
#         dict_cur.close()
#         connection.close()
#         return ret_value
#     return wrapper




# --------------------------------FOR LOCAL USE--------------------------------------
def get_connection_string():
    user_name = os.environ.get('PSQL_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB')
    env_variables_defined = user_name and password and host and database_name
    if env_variables_defined:
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')



def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection



def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper