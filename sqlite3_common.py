import sqlite3
from sqlite3 import Error
import app_common as app
import ast


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
        print(conn)
        return conn
    except Error as e:
        print(e)

    return "None"


def select_all_javi(conn):
    """
    Query all rows in the javi table
    :param conn: the Connection object
    :return:
    """
    # query = "SELECT jv.word as word, jv.phonetic as phonetic, jv.mean as mean FROM javi jv \
    #           UNION \
    #          SELECT jvc.c1word as word, jvc.c2phonetic as phonetic, jvc.c3mean as mean FROM javi_content jvc"
    query = "SELECT jv.word as word, jv.phonetic as phonetic, jv.mean as mean FROM javi jv"
    cur = conn.cursor()
    cur.execute(query)
    # rows = cur.fetchall()
    # print(len(rows))
    # for row in rows:
    #     for k, v in row.items():
    #         print(k)

    return cur.execute(query)


def select_javi(conn):
    """
    Query all rows in the javi table
    :param conn: the Connection object
    :return: list of javi
    """
    # query = "SELECT jv.word as word, jv.phonetic as phonetic, jv.mean as mean FROM javi jv WHERE word='人生'"
    query = "SELECT jv.word as word, jv.phonetic as phonetic, jv.mean as mean FROM javi jv"
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def select_all_kanji(conn):
    """
    Query all rows in the kanji  table
    :param conn: the Connection object
    :return:
    """
    query = "SELECT kanji.kanji, " \
                    "kanji.mean, " \
                    "kanji.level, " \
                    "kanji.'on', " \
                    "kanji.kun, " \
                    "kanji.detail, " \
                    "kanji.stroke_count, " \
                    "kanji.compDetail, " \
                    "kanji.examples " \
                    "" \
            "FROM kanji "
    cur = conn.cursor()
    return cur.execute(query)


def select_kanji_by_word(conn, word):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    query = "SELECT kanji.kanji, " \
                    "kanji.mean, " \
                    "kanji.level, " \
                    "kanji.'on', " \
                    "kanji.kun, " \
                    "kanji.stroke_count, " \
                    "kanji.detail " \
            "FROM kanji " \
            "WHERE kanji='" + word + "'"
    cur = conn.cursor()
    return cur.execute(query)


def select_all_javi_example(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    query = "SELECT ex.id, ex.content, ex.trans, ex.mean FROM example ex"
    cur = conn.cursor()
    return cur.execute(query)


def select_javi_example(conn, ex_id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    query = "SELECT ex.content, ex.trans, ex.mean FROM example AS ex WHERE ex.id=" + ex_id + ""
    cur = conn.cursor()
    return cur.execute(query)


def select_javi_kanji(conn, javi_word):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    query = sql_select_javi_kanji(javi_word)
    cur = conn.cursor()
    # cur.execute(query)
    # rows = cur.fetchall()
    # for row in rows:
    #     print(row)
    return cur.execute(query)


def sql_select_javi_kanji(javi_word):
    """
    Query all rows in the tasks table
    :param javi_word: the Connection object
    :return:
    """
    query = "SELECT kanji.kanji, kanji.mean, kanji.level, kanji.'on', kanji.kun, kanji.stroke_count FROM kanji " \
            + "JOIN (SELECT javi.word FROM javi WHERE  javi.word = '" + javi_word + "') AS javi1 " \
            + " ON javi1.word LIKE ('%' || kanji.kanji || '%')"
    return query


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
