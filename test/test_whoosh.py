# -*- coding: utf-8 -*-

import os, sys, shutil, sqlite3, time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
    
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NGRAM
from whoosh.analysis import StemmingAnalyzer, NgramWordAnalyzer
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir 

os.chdir(os.path.dirname(__file__))
ix_dir = os.path.join(os.getcwd(), 'dir_indices')

b_indexing = False
if b_indexing:
    if os.path.isdir(ix_dir):
        shutil.rmtree(ix_dir)
    os.mkdir(ix_dir)
    schema = Schema(code=ID(stored=True),
                    name=TEXT(analyzer=StemmingAnalyzer(), stored=True),
                    note=TEXT(analyzer=StemmingAnalyzer(), stored=True),
                    iid=ID(stored=True))

    ix = create_in(ix_dir, schema)
    writer = ix.writer()

    cn = sqlite3.connect('mycis.db')
    cr = cn.cursor()

    print('creating indices ...')
    start_time = time.time()
    for r in cr.execute('select * from diag').fetchall():
        iid, code, name, name_zh = r
        # remove . in icd10
        writer.add_document(code=code.replace('.', ''), name=unicode(name), note=unicode(name_zh), iid=u'diag_%s' % iid)
    print('creating diag indices: use %f seconds.' % (time.time() - start_time,))

    start_time = time.time()
    for r in cr.execute('select * from ord').fetchall():
        iid, code, name, name_en, note = r
        writer.add_document(code=code, name=unicode(name), 
                            note=unicode(name_en + ' ' + note), iid=u'ord_%s' % iid)    
    print('creating ord indices: use %f seconds.' % (time.time() - start_time,))

    start_time = time.time()
    for r in cr.execute('select id, code, name, name_zh, content_name, class_group from med').fetchall():
        iid, code, name, name_zh, content_name, class_group = r
        writer.add_document(code=code, name=unicode(name), note=unicode(content_name + ' ' + class_group), iid=u'med_%s' % iid)
    print('creating med indices: use %f seconds.' % (time.time() - start_time,))

    writer.commit()

class browser(QWebView):

    def __init__(self, par=None):
        super(browser, self).__init__(par)

    def set_htm(self, h='', ref='/home/cytu/sample.html', b_raw=True):
        self.setHtml(h if b_raw else htm(h), 
                     QUrl.fromLocalFile(ref if ref else __file__))

class mycis_js(QObject):
    '''Simple class with one slot and one read-only property.'''

    @pyqtSlot(str)
    def showMessage(self, msg):
        '''Open a message box and display the specified message.'''
        QMessageBox.information(None, 'Info', msg)

    def _pyVersion(self):
        '''Return the Python version.'''
        return sys.version

    '''Python interpreter version property.'''
    pyVersion = pyqtProperty(str, fget=_pyVersion)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('test_whoosh')
    
    m = mycis_js()
    w = browser()
    w.page().mainFrame().addToJavaScriptWindowObject('mycis', m)
    
    ix = open_dir(ix_dir)
    with ix.searcher() as searcher:
        query = QueryParser('note', ix.schema).parse(u'檢查')
        results = searcher.search(query, limit=None)
        html = '<html><body>'
        for i in results[1:50]:
            html += """<p><a href='""" + i['code'] + """' onClick="mycis.showMessage('""" + i['iid'] + """')">""" + i['code'] + """</a><br /><span class="name">""" + i['name'] + """</span><br />""" + i['note'] + """</p>"""        
        html += '</body></html>'
        w.set_htm(html)

    w.show()
    app.exec_()
