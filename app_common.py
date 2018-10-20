import os
import ast
import sqlite3_common as sql

general_cmd = ["mazii", "to_opf", "to_mobi"]

build_mazzi_dict = "mazii"
build_opf = "to_opf"
build_mobi = "to_mobi"


def get_current_path():
    """
    get current path
    :return: current path
    """
    return r'%s' % os.getcwd().replace('\\', '/')


def to_string(text):
    """
    convert to string and replace \r \n
    :param input string
    :return: converted string
    """
    if str(text) == "None":
        txt = ""
    else:
        txt = str(text).replace('\r\n', ', ').replace('\n', ', ')
    return txt


def get_db_file(db_file):
    """
    get directory of database file
    :return: database file path
    """
    cur_path = get_current_path()
    file_path = cur_path + "/db_mazii/{0}".format(db_file)
    return file_path


def get_type_mapping_file():
    """
    get directory of type mapping file
    :return: type mapping file path
    """
    cur_path = get_current_path()
    file_path = cur_path + "/db_mazii/type_mapping.txt"
    return file_path


def rem_after_comma(text):
    """
    remove text after character ,
    :param string
    :return: rem after comma string
    """
    where_comma = text.find(',')
    if where_comma == -1:
        return text
    return text[:where_comma + 0]


def type_mapping(type_mapping_dict, kinds):
    """
    detect type of word
    :param type_mapping_dict:
    :param kinds:
    :return:
    """
    type = ""
    for key, value in type_mapping_dict.items():
        for kind in kinds.split(","):
            if str(kind).strip() == key:
                type += value + ", "
    return type[:-2]


# def convert_kind(kind):
#     r_kind = ""
#     if kind == "n":
#         r_kind = "danh từ"
#     elif kind == "n, vs":
#         r_kind = "danh từ hoặc giới từ làm trợ từ cho động từ suru"
#     elif kind == "adj-na, n":
#         r_kind = "ính từ đuôi な, danh từ"
#     elif kind == "adv":
#         r_kind = "trạng từ"
#     elif kind == "v1":
#         r_kind = "động từ nhóm 2"
#     elif kind == "v1, vt":
#         r_kind = "động từ nhóm 2, tha động từ"
#     elif kind == "exp, adj-i":
#         r_kind = "động từ nhóm 2, tự động từ"
#     elif kind == "v5s, vt":
#         r_kind = "động từ nhóm 1 -su, tha động từ"
#     elif kind == "exp, v5r":
#         r_kind = "cụm từ, Động từ nhóm 1 -ru"
#     elif kind == "exp":
#         r_kind = "cụm từ"
#     elif kind == "exp, v5k":
#         r_kind = "cụm từ, adj-i"
#     elif kind == "exp, v5k":
#         r_kind = "cụm từ, động từ nhóm 1 -ku"
#     elif kind == "v5r":
#         r_kind = "động từ nhóm 1 -ru"
#     elif kind == "v5m, vt":
#         r_kind = "động từ nhóm 1 -mu, tha động từ"
#     elif kind == "v5r, vi":
#         r_kind = "động từ nhóm 1 -ru, tự động từ"
#     elif kind == "v5r, vt":
#         r_kind = "động từ nhóm 1 -ru, tha động từ"
#     elif kind == "n, adj-no":
#         r_kind = "danh từ, danh từ sở hữu cách thêm の"
#     elif kind == "int, n":
#         r_kind = "thán từ, danh từ"
#     elif kind == "adj-na":
#         r_kind = "tính từ đuôi な"
#     elif kind == "adj-na, n, adj-no":
#         r_kind = "tính từ đuôi な, danh từ, danh từ sở hữu cách thêm の"
#     else:
#         r_kind = kind
#
#     return r_kind


def find_kanji_by_word(list_all_kanji, word):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    kanji_detail = ""
    for kanji in list_all_kanji:
        if to_string(kanji["kanji"]).__eq__(str(word)):
            kanji_detail = kanji
            break
    return kanji_detail


def get_all_kanji(conn):
    list_all_kanji = []
    rs_kanji = sql.select_all_kanji(conn)
    for kanji in rs_kanji:
        list_all_kanji.append(kanji)
    return list_all_kanji


def get_all_javi(conn):
    list_all_javi = []
    rs_javi = sql.select_all_javi(conn)
    for javi in rs_javi:
        list_all_javi.append(javi)
    return list_all_javi


def get_all_javi_example(conn):
    list_all_javi_example = []
    rs_javi_example = sql.select_all_javi_example(conn)
    for javi_ex in rs_javi_example:
        list_all_javi_example.append(javi_ex)
    return list_all_javi_example


def build_data_dict(list_all_javi, list_all_javi_example, list_all_kanji, type_mapping_dict, l_from, l_to, src_file):
    cur_path = get_current_path()
    dict_items = ""

    javi_dict_items = []
    for i in range(l_from, l_to):
        javi_mean = ""
        javi_mean += to_string(list_all_javi[i]["phonetic"])

        kanji_detail = ""
        for j in range(0, len(to_string(list_all_javi[i]["word"]))):
            # kanji = sql.select_kanji_by_word(conn, app.to_string(javi["word"])[i])
            if j == 0:
                javi_mean += " 「 "

            found_kanji = find_kanji_by_word(list_all_kanji, to_string(list_all_javi[i]["word"])[j])
            if found_kanji == "":
                pass
            else:
                javi_mean += rem_after_comma(to_string(found_kanji["mean"])) + " "
                kanji_detail += " ● " + to_string(found_kanji["kanji"])
                kanji_detail += " (" + to_string(found_kanji["mean"]) + "): "
                kanji_detail += "<br/>  ➞ Âm on (音): " + to_string(found_kanji["on"])
                kanji_detail += "<br/>  ➞ Âm kun (訓): " + to_string(found_kanji["kun"])
                kanji_detail += "<br/>  ➞ Số nét: " + to_string(found_kanji["stroke_count"])
                kanji_detail += "<br/>  ➞ JLPT(level): " + to_string(found_kanji["level"])

                compDetail = found_kanji["compDetail"]
                if compDetail == None:
                    pass
                else:
                    try:
                        kanji_detail += "<br/>  ➞ Bộ thành phần: "
                        for comp in ast.literal_eval(compDetail):
                            kanji_detail += "『" + to_string(comp["w"]) + ": " + to_string(comp["h"]) + "』"
                    except:
                        pass

                examples = to_string(found_kanji["examples"])
                kanji_example = ""
                if examples == None:
                    pass
                else:
                    try:
                        for ex in ast.literal_eval(examples):
                            kanji_example += "  ➞➞ " + to_string(ex["w"]) \
                                             + "「" + rem_after_comma(to_string(ex["h"])) + "」" \
                                             + "(" + to_string(ex["p"]) + "): " \
                                             + to_string(ex["m"]) + "<br/>"
                    except:
                        pass

                if not kanji_example.__eq__(""):
                    kanji_detail += "<br/>  ➞ Ví dụ: <br/> " + kanji_example

        if i + 1 == (len(to_string(list_all_javi[i]["word"]))):
            javi_mean += "」 <br/>"

        mean_literal = ast.literal_eval(to_string(list_all_javi[i]["mean"]))
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
                            javi_mean += "※ <i>" + to_string(example["content"]) \
                                         + "(" + to_string(example["trans"]) \
                                         + "): " + to_string(example["trans"]) + "</i> <br/>"
                        # print("end search javi example: {}".format(datetime.now()))

                        # for example in rs_example:
                        #     javi_mean += "※ <i>" + app.to_string(example["content"]) + \
                        #                  "(" + app.to_string(example["trans"]) + "): " + app.to_string(
                        #         example["trans"]) + "</i> <br/>"
                elif key == "kind":
                    javi_mean += "☆ Thể loại: " + type_mapping(type_mapping_dict, to_string(val)) + " <br/>"
                else:
                    javi_mean += "◆ " + to_string(val) + " <br/>"
        if kanji_detail == "":
            pass
        else:
            javi_mean += "*** Phân tích chi tiết hán tự ***<br/>"
            javi_mean += kanji_detail

        # write to dict file
        dict_item = to_string(list_all_javi[i]["word"]) + "\t" + javi_mean
        print(dict_item)
        javi_dict_items.append(dict_item)

    with open(src_file, 'a', encoding='utf-8') as f:
        for item in javi_dict_items:
            f.write(item + "\n")
        # end write file
        f.close()
