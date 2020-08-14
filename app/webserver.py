import os
import sys
import glob
import logging
from flask import Flask, request, jsonify, render_template, url_for, redirect
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateNotFound


logger = logging.getLogger(__name__)


try:
    from wandbox import wandbox
    from app.config.routes import router
except ImportError as e:
    logger.error(e)
    sys.exit(1)


current_dir = os.path.dirname(__file__)
templates_dir = os.path.join(current_dir, 'templates')
contents_dir = os.path.join(current_dir, 'contents')

app = Flask(__name__)
# テンプレートのloaderをtemplatesディレクトリとcontentsディレクトリに設定
app.jinja_loader = FileSystemLoader(
    [templates_dir, contents_dir]
)


SITE_TITLE = 'Light Coding'
EXTS = {
    'python': 'py',
    'ruby': 'rb'
}

@app.route('/', methods=['GET'])
def index():
    title = 'プログラミングを学ぼう | ' + SITE_TITLE
    return render_template('index.html', title=title)


@app.route('/lesson/<lang>/list', methods=['GET'])
def lesson_list(lang):
    title = str(lang).capitalize() + ' Lesson' + ' - ' + SITE_TITLE
    links = router.children_recursive(url_for('lesson', lang=lang, section='', page=''))
    return render_template('list.html', title=title, lang=str(lang).capitalize(), links=links)


# レッスン
@app.route('/lesson/<lang>/<section>/<page>', methods=['GET'])
def lesson(lang, section, page):
    # Title
    title = str(lang).capitalize() + ' Lesson'

    # 同一セクション内で登録されたURLの数
    section_children = router.children(router.get_path('lesson', lang, section))
    page_count = len(section_children)
    page_index = section_children.index(router.get_tail(router.get_path('lesson', lang, section, page))) + 1

    # Link
    current_path = url_for('lesson', lang=lang, section=section, page=page)
    previous_page, _ = router.previous_path(current_path, depth=1)
    next_page, _ = router.next_path(current_path, depth=1)

    links = router.children_recursive(url_for('lesson', lang=lang, section='', page=''))
    chain = router.get_chain(current_path, 2)

    # Code
    ext = EXTS.get(lang)
    if ext is None:
        raise KeyError('No such language in extensions map: ' + lang)
    filename = '{}.{}'.format(page, ext)
    filepath = os.path.join(contents_dir, lang, section, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError as e:
        logger.error(e)
        code = ''

    # Template
    template_filename = '{}.html'.format(page)
    template_filepath = '/{}/{}/{}'.format(lang, section, template_filename)

    context = {
        'title': title,
        'lang': lang,
        'section': section,
        'page': page,
        'ext': ext,
        'previous_page': previous_page or '',
        'next_page': next_page or '',
        'links': links,
        'chain': chain,
        'page_index': page_index,
        'page_count': page_count,
        'code': code,
        'lesson_template': template_filepath,
    }

    return render_template('lesson.html', **context)


@app.route('/api/compile', methods=['GET'])
def api_compile():
    code = request.args.get('code', '')
    lang = request.args.get('lang', '')
    r = wandbox.compile(code, lang)
    return jsonify(r)


def start_webserver():
    app.debug = True
    app.run(host='', port=8000)
