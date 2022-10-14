/* 変数定義 */
let params;
let uuid = '';
let nickname = '';

/* UUID生成 */
function createUuid(){

  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(a) {
      let r = (new Date().getTime() + Math.random() * 16)%16 | 0, v = a == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
   });

}


/* URLのクエリパラメータからUUIDとニックネームの取得を試みる */
try {
    params = location.search;
    uuid = params.get('uuid');
    nickname = params.get('nickname');
} catch(e) {
    uuid = createUuid();
}
    
/* フォームにニックネームを挿入 */
document.getElementById("nickname").value = nickname;

/* sessionStorageにUUIDを保持 */
window.sessionStorage.setItem("uuid", uuid);

/* 参加ボタンを押した時の動作 */
let nameFormButton = document.getElementById("join-button");
nameFormButton.addEventListener('click', function () {
    let nameForm = document.getElementById("nickname");
    window.sessionStorage.setItem("nickname", nameForm.value);
    window.location.href = 'quiz_play';
})
