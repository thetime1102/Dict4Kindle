import os
import sqlite3_common as sql
import app_common as app
import ast
from datetime import datetime
import threading


def main():
    type_mapping_file = app.get_type_mapping_file()
    if not os.path.exists(type_mapping_file):
        print("type_mapping.txt not found !")
        return
    else:
        try:
            with open(type_mapping_file, "r", encoding='utf-8') as f:
                type_mapping_dict = ast.literal_eval(f.read())
                f.close()
        except Exception as ex:
            print("error: " + ex)
            return

    database_file = app.get_db_file()
    if not os.path.exists(database_file):
        print("database file not found !")
        return
    else:
        # create a database connection
        conn = sql.create_connection(database_file)

    if conn == "None":
        print("Connect to sql failed")
        return

    list_all_javi = []
    list_all_javi_example = []
    list_all_kanji = []
    with conn:
        # get all kanji
        print("start : {}".format(datetime.now()))
        rs_kanji = sql.select_all_kanji(conn)
        for kanji in rs_kanji:
            list_all_kanji.append(kanji)

        # get all javi
        rs_javi = sql.select_all_javi(conn)
        for javi in rs_javi:
            list_all_javi.append(javi)

        #get all javi example
        rs_javi_example = sql.select_all_javi_example(conn)
        for javi_ex in rs_javi_example:
            list_all_javi_example.append(javi_ex)
        print("end : {}".format(datetime.now()))

    # close sqlite connection
    conn.close()

    start_process = datetime.now()
    # get dict file
    cur_path = app.get_current_path()
    src_file = cur_path + "/db2txt/Ja2VnDict4Kindle - By VinhTQ.txt"

    cur_path = app.get_current_path()
    src_file_log = cur_path + "/db2txt/Ja2VnDict4Kindle_log.txt"

    # remove old file
    if os.path.exists(src_file):
        os.remove(src_file)

    if os.path.exists(src_file_log):
        os.remove(src_file_log)

    with open(src_file, 'w+', encoding='utf-8') as f:
        f.close()

    with open(src_file_log, 'w+', encoding='utf-8') as f:
        f.close()

    threads = []
    total_round = 20
    l_first = int(len(list_all_javi) / total_round)
    for round in range(1, total_round):
        if round == 1:
            l_from = 0
            l_to = l_first
            # print(str(round) + ":" + str(l_from) + " ->" + str(l_to))
            thread = threading.Thread(target=app.build_data_dict, args=(
                list_all_javi, list_all_javi_example, list_all_kanji, type_mapping_dict, l_from, l_to, src_file,))
            threads.append(thread)
            thread.start()
            with open(src_file_log, 'a', encoding='utf-8') as f:
                f.write(str(round) + ":" + str(l_from) + " ->" + str(l_to) + "\n")
                f.close()
        else:
            l_from = l_first * round
            l_to = l_first + l_first * round
            print(str(round) + ":" + str(l_from) + " ->" + str(l_to))
            thread = threading.Thread(target=app.build_data_dict, args=(
            list_all_javi, list_all_javi_example, list_all_kanji, type_mapping_dict, l_from, l_to, src_file,))
            threads.append(thread)
            thread.start()
            with open(src_file_log, 'a', encoding='utf-8') as f:
                f.write(str(round) + ":" + str(l_from) + " ->" + str(l_to) + "\n")
                f.close()

    for thread in threads:
        thread.join()
    print(" end ------------------------------------")
    print("Start process: {}".format(start_process))
    print("End process: {}".format(datetime.now()))

if __name__ == '__main__':
    main()
