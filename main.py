import os
import sqlite3_common as sql
import app_common as app
import ast
import sys
from datetime import datetime
from tab2opf import tab2opf

VERSION = "1.0"


def show_help():
    print("***********************************************************************************************************")
    print("**  Create Dictionary Search Tool")
    print("**  Version: %s" % VERSION)
    print("**  Copyright (C) 2018 - Tran Quang Vinh")
    print("***********************************************************************************************************")
    print("Usage tool: python  [option]  [use_for_option]")
    print("    option:")
    print("         mazii    |==> from mazii db (JP-VN dict) (*.db) file generate to dictionary resource (*.txt)     |")
    print("         to_opf   |==> from dictionary resource (*.txt) convert tab delimited dictionary into *.opf file  |")
    print("         to_mobi  |==> from *.opf file convert to dictionary (*.mobi) use for Kindle                      |")
    print("***********************************************************************************************************")
    sys.exit(1)


def generate_mazzi_dict(db_file):
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

    database_file = app.get_db_file(db_file)
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
        print("start get kanji: {}".format(datetime.now()))
        rs_kanji = sql.select_all_kanji(conn)
        for kanji in rs_kanji:
            list_all_kanji.append(kanji)
        print("end get kanji: {}".format(datetime.now()))

        # get all javi
        print("start get javi: {}".format(datetime.now()))
        rs_javi = sql.select_all_javi(conn)
        for javi in rs_javi:
            list_all_javi.append(javi)
        print("end get javi: {}".format(datetime.now()))

        # get all javi example
        print("start get javi example: {}".format(datetime.now()))
        rs_javi_example = sql.select_all_javi_example(conn)
        for javi_ex in rs_javi_example:
            list_all_javi_example.append(javi_ex)
        print("end get javi example: {}".format(datetime.now()))

    # close sqlite connection
    conn.close()

    # get dict file
    cur_path = app.get_current_path()
    src_file = cur_path + "/db2txt/Dict4Kindle.txt"

    # remove old file
    if os.path.exists(src_file):
        os.remove(src_file)

    # with open(src_file, 'w+', encoding='utf-8') as f:
    #     f.close()

    start_get_javi_dict_items = datetime.now()
    javi_dict_items = []
    for javi in list_all_javi:
        javi_mean = ""
        javi_mean += app.to_string(javi["phonetic"])

        kanji_detail = ""
        for i in range(0, len(app.to_string(javi["word"]))):
            # kanji = sql.select_kanji_by_word(conn, app.to_string(javi["word"])[i])
            if i == 0:
                javi_mean += " 「 "

            found_kanji = app.find_kanji_by_word(list_all_kanji, app.to_string(javi["word"])[i])
            if found_kanji == "":
                pass
            else:
                javi_mean += app.rem_after_comma(app.to_string(found_kanji["mean"])) + " "
                kanji_detail += " ● " + app.to_string(found_kanji["kanji"])
                kanji_detail += " (" + app.to_string(found_kanji["mean"]) + "): "
                kanji_detail += "<br/>  ➞ Âm on (音): " + app.to_string(found_kanji["on"])
                kanji_detail += "<br/>  ➞ Âm kun (訓): " + app.to_string(found_kanji["kun"])
                kanji_detail += "<br/>  ➞ Số nét: " + app.to_string(found_kanji["stroke_count"])
                kanji_detail += "<br/>  ➞ JLPT(level): " + app.to_string(found_kanji["level"])

                compDetail = found_kanji["compDetail"]
                if compDetail == None:
                    pass
                else:
                    try:
                        kanji_detail += "<br/>  ➞ Bộ thành phần: "
                        for comp in ast.literal_eval(compDetail):
                            kanji_detail += "『" + app.to_string(comp["w"]) + ": " + app.to_string(comp["h"]) + "』"
                    except:
                        pass

                examples = app.to_string(found_kanji["examples"])
                kanji_example = ""
                if examples == None:
                    pass
                else:
                    try:
                        for ex in ast.literal_eval(examples):
                            kanji_example += "  ➞➞ " + app.to_string(ex["w"]) \
                                             + "「" + app.rem_after_comma(app.to_string(ex["h"])) + "」" \
                                             + "(" + app.to_string(ex["p"]) + "): " \
                                             + app.to_string(ex["m"]) + "<br/>"
                    except:
                        pass

                if not kanji_example.__eq__(""):
                    kanji_detail += "<br/>  ➞ Ví dụ: <br/> " + kanji_example

        if i + 1 == (len(app.to_string(javi["word"]))):
            javi_mean += "」 <br/>"

        mean_literal = ast.literal_eval(app.to_string(javi["mean"]))
        for ml in mean_literal:
            # print(ml)
            for key, val in ml.items():
                if key == "examples":
                    for ex_id in val:
                        # rs_example = sql.select_javi_example(conn, ex_id)

                        # print("start search javi example: {}".format(datetime.now()))
                        example = ""
                        for javi_example in list_all_javi_example:
                            if javi_example["id"] == ex_id:
                                example = javi_example
                                break
                        if not example == "":
                            javi_mean += "※ <i>" + app.to_string(example["content"]) \
                                         + "(" + app.to_string(example["trans"]) \
                                         + "): " + app.to_string(example["trans"]) + "</i> <br/>"
                        # print("end search javi example: {}".format(datetime.now()))

                        # for example in rs_example:
                        #     javi_mean += "※ <i>" + app.to_string(example["content"]) + \
                        #                  "(" + app.to_string(example["trans"]) + "): " + app.to_string(
                        #         example["trans"]) + "</i> <br/>"
                elif key == "kind":
                    javi_mean += "☆ Thể loại: " + app.type_mapping(type_mapping_dict, app.to_string(val)) + " <br/>"
                else:
                    javi_mean += "◆ " + app.to_string(val) + " <br/>"
        if kanji_detail == "":
            pass
        else:
            javi_mean += "*** Phân tích chi tiết hán tự ***<br/>"
            javi_mean += kanji_detail

        # write to dict file
        dict_item = app.to_string(javi["word"]) + "\t" + javi_mean
        print(dict_item)
        javi_dict_items.append(dict_item)

    print("start_get_javi_dict_items: {}".format(start_get_javi_dict_items))
    print("end_get_javi_dict_items: {}".format(datetime.now()))

    start_write_file = datetime.now()
    # create new file
    with open(src_file, 'w+', encoding='utf-8') as f:
        for item in javi_dict_items:
            f.write(item + "\n")
        # end write file
        f.close()

    print("start_write_file: {}".format(start_write_file))
    print("end_write_file: {}".format(datetime.now()))

    # get list javi
    # conn.row_factory = lambda cursor, row: row[0]
    # rs_javi = sql.select_javi(conn)
    # app.build_data_dict(conn, rs_javi, 0, len(rs_javi), src_file)

    # total_round = 50
    # l_first = int(len(rs_javi) / total_round)
    # for round in range(1, total_round):
    #     if round == 1:
    #         l_from = 0
    #         l_to = l_first
    #     else:
    #         l_from = l_first * round
    #         l_to = l_first + l_first * round
    #
    #     try:
    #         _thread.start_new_thread(app.build_data_dict(conn, rs_javi, l_from, l_to, src_file))
    #     except:
    #         print("Error: unable to start thread")
    #     #
    #     # while 1:
    #     #     pass
    #     print("round {0}: from={1}, to={2}".format(round, l_from, l_to))
    #     print("-------------- end round -------------------")

    # for k, v in l_javi[100].items():
    #     print(k)
    #     if k == "mean":
    #         mean_literal = ast.literal_eval(v)
    #         for ml in mean_literal:
    #             for km, vm in ml.items():
    #                print(vm)

    print("-----------------------------done----------------------------------")


def main():
    print("main")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        opt = sys.argv[1]
        if opt in app.general_cmd:
            if opt.__eq__(app.build_mazzi_dict):
                if len(sys.argv) >= 2:
                    db_file = sys.argv[2]
                    if os.path.isfile(db_file):
                        generate_mazzi_dict(db_file)
                    else:
                        show_help()

            if opt.__eq__(app.build_opf):
                if len(sys.argv) >= 2:
                    utf_index = False
                    if sys.argv[2] == '-utf':
                        utf_index = True
                        resource_file_path = sys.argv[3]
                    else:
                        resource_file_path = sys.argv[2]

                    if not os.path.isfile(resource_file_path) or os.path.splitext(resource_file_path)[1].__ne__(".txt"):
                        print("Usage tool: python  to_opf  resource_file_path.txt")
                    else:
                        tab2opf(resource_file_path, utf_index)

            if opt.__eq__(app.build_mobi):
                if len(sys.argv) >= 2:
                    mobigen_path = os.path.join(os.getcwd(), "tool", "mobigen.exe")
                    opf_file_path = sys.argv[2]
                    if not os.path.isfile(opf_file_path) or os.path.splitext(opf_file_path)[1].__ne__(".opf"):
                        print("Usage tool: python  to_mobi  opf_file_path.opf")
                    else:
                        if not os.path.exists(mobigen_path):
                            print("Not found: {0}".format(mobigen_path))
                        else:
                            try:
                                build_mobi_cmd = "{0} {1}".format(mobigen_path, opf_file_path)
                                build_mobi_status = os.system(build_mobi_cmd)
                                if build_mobi_status == 0:
                                    mobi_out_dir = os.path.split(os.path.abspath(opf_file_path))[0]
                                    mobi_name = "{0}.mobi".format(os.path.splitext(os.path.basename(opf_file_path))[0])
                                    mobi_file_path = os.path.join(mobi_out_dir, mobi_name)
                                    if os.path.isfile(mobi_file_path):
                                        print("-----------------------------------------------------------------------")
                                        print("Created file: {0}".format(mobi_file_path))
                                        print("-----------------------------------------------------------------------")
                                    else:
                                        print("Can not build {0} file to".format(opf_file_path))
                                else:
                                    print("Can not build {0} file to".format(opf_file_path))
                            except Exception as ex:
                                print(ex)
        else:
            show_help()
    else:
        show_help()
