document.addEventListener('DOMContentLoaded', function() {
    const submitRow = document.querySelector('.submit-row');
    if (submitRow) {
        // プレビューボタンの作成
        const previewBtn = document.createElement('input');
        previewBtn.type = 'button';
        previewBtn.value = "プレビュー（保存前）";
        previewBtn.className = 'button';
        previewBtn.style.background = '#79aec8';
        previewBtn.style.marginLeft = "5px";

        submitRow.appendChild(previewBtn);

        previewBtn.addEventListener('click', function() {
            // 【修正1】フォームのIDを修正（sermon_article_form -> sermonarticle_form）
            // 念のため、IDで見つからない場合はページ内の最初のform要素を取得する処理も追加
            let form = document.getElementById('sermonarticle_form');
            if (!form) {
                form = document.querySelector('form');
            }

            // それでも見つからない場合は処理を中断
            if (!form) {
                alert('エラー: フォームが見つかりませんでした。');
                return;
            }

            const originalAction = form.action;
            const originalTarget = form.target;

            // 一時的に送信先をプレビューURLに変更
            // URLの末尾がスラッシュで終わっているか確認し、適切にパスを結合
            const currentPath = window.location.pathname;
            const separator = currentPath.endsWith('/') ? '' : '/';
            form.action = currentPath + separator + "preview/";
            
            form.target = "_blank"; // 別タブで開く
            
            form.submit();

            // 【修正2】送信処理が確実にブラウザに認識されてから元に戻すため、少し時間を置く
            setTimeout(function() {
                form.action = originalAction;
                form.target = originalTarget;
            }, 500); // 0.5秒後に戻す
        });
    }
});