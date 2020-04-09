import os
import sys
import logging
from flask import Flask, request, jsonify, render_template, url_for
from jinja2 import FileSystemLoader


logger = logging.getLogger(__name__)


try:
    from wandbox import wandbox
    from app.config.lang_extension_map import extensions
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


@app.route('/', methods=['GET'])
def index():
    title = 'index'
    return render_template('index.html', title=title)


@app.route('/<lang>/list', methods=['GET'])
def lesson_list(lang):
    title = lang + ' List'
    lessons = router.get_path(lang, 'list')
    return render_template('list.html', title=title)


@app.route('/<lang>/<section>/<int:page>', methods=['GET'])
def lesson(lang, section, page):
    # Title
    title = lang + ' Lesson'

    # Pagination
    current_path = router.get_path(lang, section, str(page))
    previous_page = router.previous_path(current_path)
    next_page = router.next_path(current_path)

    # Code
    ext = extensions.get(lang)
    if not ext:
        raise KeyError('No such language in extensions map: ' + lang)
    filename = '{}_{}.{}'.format(section, page, ext)
    filepath = os.path.join(contents_dir, lang, section, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError as e:
        logger.error(e)
        code = ''

    # Template
    template_filename = '{}_{}.html'.format(section, page)
    template_filepath = '/' + \
        os.path.join(lang, section, template_filename).replace(
            os.path.sep, '/')

    context = {
        'title': title,
        'language': lang,
        'section': section,
        'page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'code': code,
        'lesson': template_filepath,
    }

    return render_template('lesson.html', **context)


@app.route('/api/compile', methods=['GET'])
def api_compile():
    code = request.args.get('code', '')
    print(code, type(code))
    r = wandbox.compile(code)
    return jsonify(r)


def start_webserver():
    app.debug = True
    app.run(host='', port=8000)
