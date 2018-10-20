begin_html = """<?xml version="1.0" encoding="utf-8"?>
                <html xmlns:idx="www.mobipocket.com" xmlns:mbp="www.mobipocket.com" xmlns:xlink="http://www.w3.org/1999/xlink">
                  <body>
                    <mbp:pagebreak/>
                    <mbp:frameset>
                      <mbp:slave-frame display="bottom" device="all" breadth="auto" leftmargin="0" rightmargin="0" bottommargin="0" topmargin="0">
                        <div align="center" bgcolor="yellow"/>
                        <a onclick="index_search()">Dictionary Search (make by VinhTQ)</a>
                        </div>
                      </mbp:slave-frame>
                      <mbp:pagebreak/>
            """


def html_content(yomi, key_word, key_num, orth_alter_tag, key_word_translate):
    content = """      <idx:entry name="word" scriptable="yes">
                            <h2>
                              <idx:orth value="%s">%s</idx:orth><idx:key key="%s">
                              %s
                              </idx:key>
                            </h2>
                            %s
                        </idx:entry>
                        <mbp:pagebreak/>
               """ % (yomi, key_word, key_num, orth_alter_tag, key_word_translate)
    return content


end_html = """
        </mbp:frameset>
      </body>
    </html>
    """


def begin_opf(dict_name):
    begin = """<?xml version="1.0"?><!DOCTYPE package SYSTEM "oeb1.ent">
    
                    <!-- the command line instruction 'prcgen dictionary.opf' will produce the dictionary.prc file in the same folder-->
                    <!-- the command line instruction 'mobigen dictionary.opf' will produce the dictionary.mobi file in the same folder-->
                    
                    <package unique-identifier="uid" xmlns:dc="Dublin Core">
                    
                        <metadata>
                            <dc-metadata>
                                <dc:Identifier id="uid">%s</dc:Identifier>
                                <!-- Title of the document -->
                                <dc:Title><h2>%s</h2></dc:Title>
                                <dc:Language>EN</dc:Language>
                            </dc-metadata>
                            <x-metadata>
                """ % (dict_name, dict_name)
    return begin


opf_temp_head_no_utf = """		<output encoding="UTF-8" flatten-dynamic-dir="yes"/>"""

opf_temp_head_2 = """
            <DictionaryInLanguage>en-us</DictionaryInLanguage>
            <DictionaryOutLanguage>ja-jp</DictionaryOutLanguage>
        </x-metadata>
    </metadata>

<!-- list of all the files needed to produce the .prc file -->
<manifest>
"""


def opf_temp_line(dict_no, dict_name):
    temp_line = """ <item id="dictionary%d" href="%s%d.html" media-type="text/x-oeb1-document"/>
                """ % (dict_no, dict_name, dict_no)
    return temp_line


opf_temp_mid = """</manifest>


<!-- list of the html files in the correct order  -->
<spine>
"""


def opf_temp_line_ref(dict_no):
    temp_line_ref = """	<itemref idref="dictionary%d"/>
    """ % dict_no
    return temp_line_ref


def opf_temp_end():
    temp_end = """</spine>
    
    <tours/>
    <guide> <reference type="search" title="Dictionary Search (make by VinhTQ)" onclick= "index_search()"/> </guide>
    </package>
    """
    return temp_end
