document.addEventListener('DOMContentLoaded',function() {
    const submitRow = document.querySelector ('.submit-row');
    if (submitRow) {
        // プレビューボタンの作成
        const previewBtn = document.createElement ('input');
        previewBtn.type = 'button';
        previewBtn.value ="プレビュー（保存前）";
        previewBtn.className = 'button';
        previewBtn.style.background = '#79aec8';
        previewBtn.style.marginLeft = "5px";

        submitRow.appendChild(previewBtn);

        previewBtn.addEventListener('click', function() {
        const form = document.getElementById('sermon_article_form'); //フォームIDはモデル名により変わります
        const originalaction = form.action;
        const originalTarget = form.target;
        // 一時的に送信先をプレビューURLに変更
        form.action = "preview/";
        form.target ="_blank"; //別タブで開く
        form.submit ();
        // 元の設定に戻す

        form.action = originalaction;
        form.target = originalTarget;
    });
    }
});