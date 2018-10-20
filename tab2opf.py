#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------------------------------------------------------------------------------
# - Remake of tab2opf dictionary builder for kindle
# - Script to convert tab delimited dictionary files into opf file to run
# - with kindlegen into a translation lookup dictionary for kindle.
# - Based on the generally available tab2opf.py by Klokan Petr Přidal (www.klokan.cz) from 2007
# - Convert from python version 2.7 to python version 3.6 by VinhTQ (thetime1102)
# - Worked with Japanese character (^_^)
# --------------------------------------------------------------------------------------------------------
#
# Script for conversion of Stardict tabfile (<header>\t<definition>
# per line) into the OPF file for MobiPocket Dictionary
#
# For usage of dictionary convert it by:
# (wine) mobigen.exe DICTIONARY.opf
#
# MobiPocket Reader at: www.mobipocket.com for platforms:
#   PalmOs, Windows Mobile, Symbian (Series 60, Series 80, 90, UIQ), Psion,
#   Blackberry, Franklin, iLiad (by iRex), BenQ-Siemens, Pepper Pad..
#   http://www.mobipocket.com/en/DownloadSoft/DownloadManualInstall.asp
# mobigen.exe available at:
#   http://www.mobipocket.com/soft/prcgen/mobigen.zip
#
# Copyright (C) 2007 - Klokan Petr Přidal (www.klokan.cz)
# Copyright (C) 2018 - Tran Quang Vinh (https://github.com/thetime1102)
#
#
# Version history:
# 0.1 (19.7.2007) Initial version
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

# VERSION
from numpy import unicode
import codecs
import sys
import os
from unicodedata import normalize, decomposition, combining
import string
import tab2opf_setting as tab2opf_set

VERSION = "2.0"

# Hand-made table from PloneTool.py
mapping_custom_1 = {
    138: 's', 142: 'z', 154: 's', 158: 'z', 159: 'Y'}

# UnicodeData.txt does not contain normalization of Greek letters.
mapping_greek = {
    912: 'i', 913: 'A', 914: 'B', 915: 'G', 916: 'D', 917: 'E', 918: 'Z',
    919: 'I', 920: 'TH', 921: 'I', 922: 'K', 923: 'L', 924: 'M', 925: 'N',
    926: 'KS', 927: 'O', 928: 'P', 929: 'R', 931: 'S', 932: 'T', 933: 'Y',
    934: 'F', 936: 'PS', 937: 'O', 938: 'I', 939: 'Y', 940: 'a', 941: 'e',
    943: 'i', 944: 'y', 945: 'a', 946: 'b', 947: 'g', 948: 'd', 949: 'e',
    950: 'z', 951: 'i', 952: 'th', 953: 'i', 954: 'k', 955: 'l', 956: 'm',
    957: 'n', 958: 'ks', 959: 'o', 960: 'p', 961: 'r', 962: 's', 963: 's',
    964: 't', 965: 'y', 966: 'f', 968: 'ps', 969: 'o', 970: 'i', 971: 'y',
    972: 'o', 973: 'y'}

# This may be specific to German...
mapping_two_chars = {
    140: 'O', 156: 'o', 196: 'A', 246: 'o', 252: 'u', 214: 'O',
    228: 'a', 220: 'U', 223: 's', 230: 'e', 198: 'E'}

mapping_latin_chars = {
    192: 'A', 193: 'A', 194: 'A', 195: 'a', 197: 'A', 199: 'C', 200: 'E',
    201: 'E', 202: 'E', 203: 'E', 204: 'I', 205: 'I', 206: 'I', 207: 'I',
    208: 'D', 209: 'N', 210: 'O', 211: 'O', 212: 'O', 213: 'O', 215: 'x',
    216: 'O', 217: 'U', 218: 'U', 219: 'U', 221: 'Y', 224: 'a', 225: 'a',
    226: 'a', 227: 'a', 229: 'a', 231: 'c', 232: 'e', 233: 'e', 234: 'e',
    235: 'e', 236: 'i', 237: 'i', 238: 'i', 239: 'i', 240: 'd', 241: 'n',
    242: 'o', 243: 'o', 244: 'o', 245: 'o', 248: 'o', 249: 'u', 250: 'u',
    251: 'u', 253: 'y', 255: 'y'}

# Feel free to add new user-defined mapping. Don't forget to update mapping dict
# with your dict.

mapping = {}
mapping.update(mapping_custom_1)
mapping.update(mapping_greek)
mapping.update(mapping_two_chars)
mapping.update(mapping_latin_chars)

# On OpenBSD string.whitespace has a non-standard implementation
# See http://plone.org/collector/4704 for details
whitespace = ''.join([c for c in string.whitespace if ord(c) < 128])
allowed = string.ascii_letters + string.digits + string.punctuation + whitespace


def normalize_unicode(text, encoding='humanascii'):
    """
    This method is used for normalization of unicode characters to the base ASCII
    letters. Output is ASCII encoded string (or char) with only ASCII letters,
    digits, punctuation and whitespace characters. Case is preserved.
    """
    unicodeinput = True
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8')
        unicodeinput = False

    res = ''
    global allowed
    if encoding == 'humanascii':
        enc = 'ascii'
    else:
        enc = encoding
    for ch in text:
        if (encoding == 'humanascii') and (ch in allowed):
            # ASCII chars, digits etc. stay untouched
            res += ch
            continue
        else:
            try:
                ch.encode(enc, 'strict')
                res += ch
            except UnicodeEncodeError:
                ordinal = ord(ch)
                if mapping.get(ordinal, None) is not None:
                    # try to apply custom mappings
                    res += mapping.get(ordinal)
                elif decomposition(ch) or len(normalize('NFKD', ch)) > 1:
                    normalized = filter(lambda i: not combining(i), normalize('NFKD', ch))
                    # normalized string may contain non-letter chars too. Remove them
                    # normalized string may result to  more than one char
                    res += ''.join([c for c in normalized if c in allowed])
                else:
                    # hex string instead of unknown char
                    res += "%x" % ordinal
    if unicodeinput:
        return res
    else:
        return res.encode('utf-8')


def html_write(html_file, html_content):
    with codecs.open(html_file, mode='w', encoding='utf-8') as use_for_opf:
        use_for_opf.write(html_content)
        use_for_opf.close()


def tab2opf(file_path, utf_index):
    cur_dir = os.getcwd()
    print("input file: {0}".format(file_path))
    fr = codecs.open(file_path, 'rb', encoding='utf-8')
    name = os.path.splitext(os.path.basename(file_path))[0]
    tab2opf_path = os.path.join(cur_dir, "tab2opf_converted")
    if not os.path.exists(tab2opf_path):
        os.mkdir(tab2opf_path)

    i = 0
    to = False
    # len_line = len(fr.readlines())
    for r in fr.readlines():

        print("i % 10000 = {0}".format(i % 10000))
        if i % 10000 == 0:
            if to:
                to.write("""
                    </mbp:frameset>
                  </body>
                </html>
                """)
                to.close()
            html_file = os.path.join(tab2opf_path, "%s%d.html" % (name, i / 10000))
            print("ceate file: {0}".format(html_file))
            to = codecs.open(html_file, mode='w', encoding='utf-8')
            to.write(tab2opf_set.begin_html)

        # processing keyword and translate
        dt, dd = r.split('\t', 1)
        if not utf_index:
            dt = normalize_unicode(dt, 'utf-8')
            dd = normalize_unicode(dd, 'utf-8')
        dtstrip = normalize_unicode(dt)
        dd = dd.replace("\\\\", "\\").replace("\\n", "<br/>\n")
        # print("processing keyword and translate: dt={0} - dd={1}".format(dt, dd))

        orth_alter = []
        # adding kanji entries as inflections
        try:
            yomi, kanji = dt.split(u',')

            # duplicate items according to kanji, excluding suffix
            if u'―' not in kanji:
                for k in kanji[1:-1].split(u'・'):
                    orth_alter.append(u'%s【%s】' % (k, yomi))
        except Exception as e:
            yomi = dt
            kanji = u''
        print("adding kanji entries as inflections: yomi={0} - kanji={1}".format(yomi, kanji))

        orth_alter_tag = ''
        if orth_alter:
            orth_alter_tag = u''.join(
                [u'<idx:orth value="%s"></idx:orth>' % k for k in orth_alter]
            )
        print("orth_alter_tag: {0}".format(orth_alter_tag))

        dt = dt.replace(u',', u'')
        to.write(tab2opf_set.html_content(yomi, dt, dtstrip, orth_alter_tag, dd))
        i += 1
        print("{0} - Keyword: {1}".format(i, dt))

    to.write(tab2opf_set.end_html)
    to.close()
    fr.close()

    # create opf file
    opf_file_path = os.path.join(tab2opf_path, "{0}.opf".format(name))
    lineno = i - 1
    # opf_file_path = "%s.opf" % name
    with open(opf_file_path, mode='w') as opf_to:
        opf_to.write(tab2opf_set.begin_opf(name))

        if not utf_index:
            opf_to.write(tab2opf_set.opf_temp_head_no_utf)
        opf_to.write(tab2opf_set.opf_temp_head_2)

        lineno_count = int(lineno / 10000)
        for i in range(0, lineno_count + 1):
            opf_to.write(tab2opf_set.opf_temp_line(i, name))
        opf_to.write(tab2opf_set.opf_temp_mid)

        for i in range(0, lineno_count + 1):
            opf_to.write(tab2opf_set.opf_temp_line_ref(i))
        opf_to.write(tab2opf_set.opf_temp_end())

        opf_to.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        utf_index = False
        if sys.argv[1] == '-utf':
            utf_index = True
            file_path = sys.argv[2]
        else:
            file_path = sys.argv[1]

        tab2opf(file_path, utf_index)
    else:
        print("tab2opf (Stardict->MobiPocket)")
        print("------------------------------")
        print("Version: %s" % VERSION)
        print("Copyright (C) 2018 - Tran Quang Vinh")
        print("Usage: python tab2opf.py [-utf] DICTIONARY.tab")
        print("ERROR: You have to specify a .tab file")
        sys.exit(1)
