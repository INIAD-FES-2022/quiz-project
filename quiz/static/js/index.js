/* 変数定義 */
let params;
let uuid = '';
let nickname = '';

/* URLのクエリパラメータからUUIDとニックネームの取得を試みる */
try {
    params = location.search;
    uuid = params.get('uuid');
    nickname = params.get('nickname');
} catch(e) {
    console.error("Error:",e.message);
}
    
/* フォームにニックネームを挿入 */
let nameForm = document.getElementById("nickname");
nameForm.value = nickname;

/* sessionStorageにUUIDを保持 */
window.sessionStorage("UUID", uuid);


