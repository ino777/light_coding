// オプション

var options = {
    code: {
        defaultText: '',
        language: code_lang
    }
}


function initOpts() {
    options['code']['defaultText'] = $('#editor').val();
    options['code']['language'] = code_lang;
}


/* ----------------------------------- API　----------------------------------*/
// コードをapiに送信
function compileCode(code, lang, target) {
    $(target).html('Now connecting...');

    $.ajax({
        url: '/api/compile',
        method: 'GET',
        data: {
            'code': code,
            'lang': lang
        }
    })
        .done((result) => {
            console.log(result);
            if (result.program_message) {
                message = result.program_message.replace(/</gm, '&lt').replace(/>/gm, '&gt').replace(/\r\n|\r|\n/gm, '<br>');
            } else {
                message = '';
            }
            message += '<br>'.repeat(3)
            $(target).html(message);
        })
        .fail((result) => {
            $(target).html('No response');
        })
}

/* ---------------------------------描画制御 --------------------------------*/
// ボトムを画面下部に固定
function stickBottom(target) {
    var offsetTop = window.innerHeight - target.height();
    target.offset({ top: offsetTop });
}


// CodeMirrorを描画
function RenderCodeMirror(l, id) {
    var cm;
    var target = document.getElementById(id)
    switch (l) {
        case 'python':
            cm = CodeMirror.fromTextArea(target, {
                mode: 'python',
                lineNumbers: true,
                smartIndent: true,
                indentUnit: 4,
                Theme: 'abcdef',
            });
            cm.save();
            break;
        default:
            break;
    }
    return cm;
}


/*  読み込み時に実行　*/
$(function () {
    // 初期化
    initOpts();

    // divの最下部を画面最下部に固定させる
    var lsnNavDiv = $('#lesson-nav');
    var outputDiv = $('#program-output');
    // $(window).on("load scroll resize", function () {
    //     // stickBottom(lsnNavDiv);
    //     stickBottom(outputDiv);
    // });
    // outputDiv.on('scroll', function () {
    //     stickBottom(outputDiv);
    // });


    // CodeMirror
    // See here. https://codemirror.net/index.html
    var cm = RenderCodeMirror(options['code']['language'], 'editor');
    cm.on('change', function () {
        cm.save();
    });

    cm.setOption("extraKeys", {
        'Ctrl-Enter': function () {
            var code = $('#editor').val();
            compileCode(code, options['code']['language'], '#program-output-text');
        }
    });

    // Reset処理
    $('#reset').on('click', function () {
        $('#editor').val(options['code']['defaultText']).change();
        cm.setValue($('#editor').val());
    });

    // Compile処理
    $('#compile-run').on('click', function () {
        var code = $('#editor').val();
        compileCode(code, options['code']['language'], '#program-output-text');
    });

    console.log(cm.defaultTextHeight());
});