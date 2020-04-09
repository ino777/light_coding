/* ----------------------------テキストエリア----------------------- */
// 行を取得
function getRow(str, pos) {
    var text = str.substring(0, pos);
    return (text.match(/\n/g) || []).length + 1;
}

// 列を取得
// 最大200列まで
function getCol(str, pos) {
    var text = str.substring(0, pos);
    var char = '';
    var line = '';

    if (text.match(/\n/g) === null) {
        // カーソル位置が一行目のとき
        line = text;
    } else {
        for (i = 1; i < 200; i++) {
            if (pos - i < 0) { break; }
            char = text.charAt(pos - i);
            if (char === '\n') {
                line = text.slice(pos - i + 1, pos);
                break;
            }
        }
    }
    return line.length;
}


// 一行の文字列を取得
function getLineText(str, row) {
    var lines = str.split(/\n/g);
    return lines[row - 1]
}

// 行の最初の空白の数を取得
function getIndent(str, pos) {
    var row = getRow(str, pos);
    var line = getLineText(str, row);
    var count = 0;
    var i = 0;
    const limit = 100;
    while (line[i] === ' ') {
        if (i >= limit) { break; }
        count++;
        i++;
    }
    return count;
}

// インデントされているか
function isIndented(str, pos) {
    return getIndent(str, pos) !== 0;
}

// 文字列の挿入
function insertString(inStr, str, start, end) {
    return str.substring(0, start) + inStr + str.substring(end, str.length);
}

// 直前の空白改行でない文字を取得
function getPreChar(str, pos) {
    var char = '';
    for (i = 1; i < str.length; i++) {
        char = str.charAt(pos - i);
        if ((char !== ' ') && (char !== '\n')) { break; }
    }
    return char;
}




/*------------------------------ キー制御 ----------------------------------------*/

// オプション
var TABSPACE = 4;


// Tabキー制御
// Tabを打つとスペース4つを入力する
// <textarea>はTabが入力できないため、Tabを入力できるようにこれを使う
function tabInput(event) {
    if (event.keyCode !== 9) { return false; }
    // デフォルト動作停止
    event.preventDefault();
    var textarea = event.target;
    // 選択状態でないとき入力できる
    if (textarea.selectionStart === textarea.selectionEnd) {
        var sentence = textarea.value;
        var len = sentence.length;
        var pos = textarea.selectionStart;
        sentence = insertString(' '.repeat(TABSPACE), sentence, textarea.selectionStart, textarea.selectionEnd);
        textarea.value = sentence;
        textarea.setSelectionRange(pos + TABSPACE, pos + TABSPACE);
    }
    // テキストエリアにchangeのイベントを発火
    $(textarea).change();
    // デフォルト動作の再設定
    event.onkeydown = true;
    return false;
}

// Shift + Tabキー制御
// カーソル位置の直前の4の倍数の列まで空白で埋まっていた場合、それらの空白を消す
function shiftTabInput(event) {
    if (event.shiftKey && (event.keyCode === 9)) {
        // デフォルト動作停止
        event.preventDefault();

        var textarea = event.target;

        // 選択状態でないとき入力できる
        if (textarea.selectionStart === textarea.selectionEnd) {
            var pos = textarea.selectionStart;
            var sentence = textarea.value;
            var col = getCol(sentence, pos);
            var len;
            if (col % TABSPACE === 0) { len = TABSPACE; }
            else { len = col % TABSPACE };

            if (sentence.substring(pos - len, pos) === ' '.repeat(len)) {
                sentence = insertString('', sentence, pos - len, pos);
                textarea.value = sentence;
                textarea.setSelectionRange(pos - len, pos - len);
            }
        }
        // テキストエリアにchangeのイベントを発火
        $(textarea).change();
        // デフォルト動作の再設定
        event.onkeydown = true;
    }
    return false;
}

// BackSpaceキー制御
// カーソル位置の列が4の倍数かつ直前に空白が4つあるとき、BackSpaceキーを打つと空白4つを消す
function backspaceInput(event) {
    if (event.keyCode !== 8) { return false; }

    var textarea = event.target;
    // 複数文字を選択のときは通常通り消す
    if (textarea.selectionStart !== textarea.selectionEnd) { return false; }

    var pos = textarea.selectionStart;
    var sentence = textarea.value;
    var col = getCol(sentence, pos);

    // 条件を満たせば空白4つを消す
    if ((col % TABSPACE === 0) && (sentence.substring(pos - TABSPACE, pos) === ' '.repeat(TABSPACE))) {
        sentence = insertString('', sentence, pos - TABSPACE + 1, pos);
        textarea.value = sentence;
        textarea.setSelectionRange(pos - TABSPACE + 1, pos - TABSPACE + 1);
    }
    // テキストエリアにchangeのイベントを発火
    $(textarea).change();
    return false;
}


// Enterキー制御
// ( ':', '{', '(' )の直後に改行すると、次の行はTABSPACE分インデントされる
function enterInput(event) {
    if (event.keyCode !== 13) { return false; }
    // デフォルト動作停止
    event.preventDefault();

    var textarea = event.target;
    var pos = textarea.selectionStart;
    var sentence = textarea.value;

    // 直前の文字を取得
    var char = sentence.charAt(pos - 1);
    // 改行後のインデントを求める
    var newSpaceCount = (isIndented(sentence, pos)) ? getIndent(sentence, pos) : 0;
    var insertStr = '\n' + ' '.repeat(newSpaceCount);

    switch (char) {
        case ':':
            insertStr += ' '.repeat(TABSPACE);
            newSpaceCount += TABSPACE;
            break;
        case '{':
            insertStr += ' '.repeat(TABSPACE);
            newSpaceCount += TABSPACE;
            if (sentence.charAt(pos) === '}') { insertStr += '\n' + ' '.repeat(getIndent(sentence, pos)); }
            break;
        case '(':
            insertStr += ' '.repeat(TABSPACE);
            newSpaceCount += TABSPACE;
            if (sentence.charAt(pos) === ')') { insertStr += '\n' + ' '.repeat(getIndent(sentence, pos)); }
            break;
        default:
            break;
    }
    sentence = insertString(insertStr, sentence, textarea.selectionStart, textarea.selectionEnd);
    textarea.value = sentence;
    textarea.setSelectionRange(pos + newSpaceCount + 1, pos + newSpaceCount + 1);
    // テキストエリアにchangeのイベントを発火
    $(textarea).change();
    // デフォルト動作の再設定
    event.onkeydown = true;
    return false;
}

// コード内でのキー制御
$('.code').on('keydown', function (e) {
    console.log("KEYDOWN");
    // BackSpace
    if (e.keyCode === 8) { backspaceInput(e); }
    // Tab
    if (e.keyCode === 9) {
        if (!e.shiftKey) { tabInput(e); }
        else { shiftTabInput(e); }
    }
    // Enter
    if (e.keyCode === 13) { enterInput(e); }
});