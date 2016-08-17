#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for, request

import jieba
import jieba.analyse as analyse
import jieba.posseg as pseg
jieba.initialize()

app = Flask(__name__)

EXAMPLE_WORDS = '刘德华演过的经典电影'
CUT_MOD_NAMES = {
    's': '搜索引擎模式',
    'f': '全模式',
    'd': '精确模式',
    '': '分词测试',
}

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
            mode = 's'
        # 调用jieba切词
        if mode == 's':
            segments = jieba.cut_for_search(word)
        elif mode == 'f':
            segments = jieba.cut(word, cut_all=True)
        else:
            segments = jieba.cut(word)
        content = ", ".join(segments).encode('utf-8')
        content += "<br/><br/>关键词: " + " ".join(analyse.extract_tags(word, topK=3)).encode('utf-8')
    else:
        # 没有输入要分词的内容
        word = ''
        mode = ''
        content = '请在地址栏后或输入框中，输入要分词的内容<br/>例如: <a href="%s">%s</a><br/><br/>支持的模式: <b>/d</b> 精确模式; <b>/a</b> 全模式; <b>/s</b> 搜索引擎模式' % (url_for('cut_words', word=EXAMPLE_WORDS, mode='s').encode('utf8'), '/cut/'+EXAMPLE_WORDS)
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
