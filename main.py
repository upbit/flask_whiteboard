#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request

import jieba
import jieba.analyse as analyse
import jieba.posseg as pseg
jieba.initialize()

import mmseg
import mmseg.search

app = Flask(__name__)

EXAMPLE_WORDS = '研究生在研究院研究生命科学'
CUT_MOD_NAMES = {
    's': '搜索引擎模式',
    'f': '全模式',
    'd': '精确模式',
    '': '分词测试',
    'mm': 'mmseg',
    'mms': 'mmseg-search',
}

def add_red(document, key_words):
    result = document
    for word in [ word.encode('utf-8') for word in key_words ]:
        result = result.replace(word, "<span class=red>%s</span>" % word)
    return result

@app.route('/')
def index():
    return redirect(url_for('cut_words'))

@app.route('/cut', methods=['GET', 'POST'])
@app.route('/cut/<word>')
@app.route('/cut/<word>/<mode>')
def cut_words(word=None, mode=None):
    if not word:
        word = request.form['word'] if request.method == 'POST' else request.args.get('word')
    if not mode:
        mode = request.form['mode'] if request.method == 'POST' else request.args.get('mode')

    if word:
        word = word.encode('utf-8')
        if not mode in CUT_MOD_NAMES.keys():
            mode = 'mms'    # 默认值
        # 调用jieba切词
        if mode == 's':
            segments = jieba.cut_for_search(word)
        elif mode == 'f':
            segments = jieba.cut(word, cut_all=True)
        elif mode == 'd':
            segments = jieba.cut(word)
        elif mode == 'mm':
            segments = mmseg.seg_txt(word)
        elif mode == 'mms':
            segments = mmseg.search.seg_txt_search(word)
        else:
            raise Exception("Unknown mode(%s)" % mode)
        result = ", ".join(segments)
        try:
            # try encode to utf-8 if ascii
            result = result.encode('utf-8')
        except:
            pass

        content = result
        if mode in ['d','f','s']:
            content += "<br/>" + "关键词: " + add_red(word, analyse.extract_tags(word, topK=2))
    else:
        # 没有输入要分词的内容
        word = ''
        mode = ''
        content  = '请在地址栏后或输入框中，输入要分词的内容<br/>例如: <a href="%s">%s</a><br/><br/>' % (url_for('cut_words', word=EXAMPLE_WORDS).encode('utf8'), '/cut/'+EXAMPLE_WORDS)
        content += '支持的模式: <br>' \
                   '&nbsp; jieba: <span class=tips>/d</span> 精确模式; <span class=tips>/a</span> 全模式; <span class=tips>/s</span> 搜索引擎模式<br>' \
                   '&nbsp; mmseg: <span class=tips>/mm</span> mmseg模式; <span class=tips>/mms</span> mmseg.search模式'
                
    return render_template('whiteboard.html', word=word, mode=mode, mode_names=CUT_MOD_NAMES, content=content, title='Jieba切词测试')

@app.route('/pseg', methods=['GET', 'POST'])
@app.route('/pseg/<word>')
def posseg(word=None):
    if not word:
        word = request.form['word'] if request.method == 'POST' else request.args.get('word')

    if word:
        word = word.encode('utf-8')
        segments = [ "%s/%s" % (w, f) for w, f in pseg.cut(word) ]
        content = ", ".join(segments).encode('utf-8')
    else:
        # 没有输入要分词的内容
        word = ''
        mode = ''
        content = '请在地址栏后或输入框中，输入要进行词性标注的内容<br/>例如: <a href="%s">%s</a>' % (url_for('posseg', word=EXAMPLE_WORDS).encode('utf8'), '/pseg/'+EXAMPLE_WORDS)
    return render_template('whiteboard.html', word=word, content=content, title='Jieba词性标注测试')

if __name__ == '__main__':
    app.run()
