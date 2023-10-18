/* 変数定義 */
let params;
let uuid = '';
let nickname = '';
const apiUrl = 'http://' + window.location.host + '/api/';
/* UUID生成 */
function createUuid(){

  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(a) {
      let r = (new Date().getTime() + Math.random() * 16)%16 | 0, v = a == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
   });

}


/* URLのクエリパラメータからUUIDとニックネームの取得を試みる */
params = new URLSearchParams(location.search);
uuid = params.get('uuid');
nickname = params.get('nickname');

/* UUIDがパラメータに渡されていない場合、sessionStorageから持ってくるか、新しく生成する */
if (uuid === null) {
    if (sessionStorage.getItem('uuid') === null) {
        uuid = createUuid();
    } else {
	uuid = sessionStorage.getItem('uuid');
    }
}


    
/* フォームにニックネームを挿入 */
if (nickname !== null) {
    document.getElementById("nickname").value = nickname;
}

/* sessionStorageにUUIDを保持 */
window.sessionStorage.setItem("uuid", uuid);

/* 参加ボタンを押した時の動作 */
let nameFormButton = document.getElementById("join-button");
nameFormButton.addEventListener('click', function () {
    let nameForm = document.getElementById("nickname");
    if (nameForm.value === '') {
	alert('ニックネームを入力してください。');
    } else {
        window.sessionStorage.setItem("nickname", nameForm.value);
    	window.location.href = "quiz_play";
    }
})


/* プルダウンメニューの値を取得し代入する */
document.addEventListener("DOMContentLoaded", function() {
    const selectMenu = document.getElementById("selectMenu");

    fetch(apiUrl+'events/')
	    .then(response => {
                if (!response.ok) {
		    throw new Error('Failed to get quiz events.');
		}

		return response.json();
	    })
	    .then(data => {
		let child;
		let i=0;
		for (i=0; i<data.length; i++) {
		    child = document.createElement("option");
		    child.value = data[i].id;
		    child.textContent = data[i].name;
		    selectMenu.append(child);
		}
	    })
});

/* プルダウンメニューの値に合わせてランキング表を書き換える */
document.addEventListener("DOMContentLoaded", function() {
    const selectMenu = document.getElementById("selectMenu");
    const rankingTable = document.getElementById("rankingTable");
    const rankingTableBody = document.getElementById("rankingTableBody");

    selectMenu.addEventListener("change", function() {
	const selectValue = selectMenu.value;
	rankingTableBody.innerHTML = '';

	fetch(apiUrl+'ranking/?eventid='+selectValue)
	    .then(response => {
                if (!response.ok) {
		    throw new Error('Failed to get ranking.');
		}
		return response.json();
	    })
	    .then(data => {
		let tableRow;
		let tableRankCell;
		let tableNameCell;
		let tableScoreCell;
		let i=0;
		let max=50;
		if (data.length === 0) {
			let errorMsg = document.createElement("p");
			errorMsg.textContent = "まだ開催されていません。";
			rankingTableBody.append(errorMsg);
		} else if (data.length < max) {
	            max=data.length 
		    for (i=0; i<max; i++) {
			    tableRow = document.createElement("tr");
			    tableRankCell = document.createElement("td");
			    tableRankCell.textContent = data[i].temp_rank;
			    tableNameCell = document.createElement("td");
			    tableNameCell.textContent = data[i].nickname;
			    tableScoreCell = document.createElement("td");
			    tableScoreCell.textContent = data[i].score;
			    tableRow.append(tableRankCell);
			    tableRow.append(tableNameCell);
			    tableRow.append(tableScoreCell);
			    rankingTableBody.append(tableRow);
		    }
		}
	    });
    });
});

/* 順位を表示する */
function showRank() {
	const selectMenu = document.getElementById("selectMenu");

	if (selectMenu.value === '選択してください') {
		alert('開催回を選択してください。');
	} else {
		const params = {
			"eventid": selectMenu.value,
			"userid": uuid
		}
		const queryParams = new URLSearchParams(params);
		
		fetch(apiUrl+'ranking/?'+queryParams)
			.then(response => {
				if (!response.ok) {
					throw new Error('Failed to get ranking');
					alert('取得に失敗しました。もう一度お試しください。');
				}
				return response.json();
			})
			.then (data => {
				if (data.length === 0) {
					alert(selectMenu[selectMenu.selectedIndex].textContent+'には参加していないようです。他の開催を選んでもう一度お試しください。');
				} else {
					alert(data[0].nickname+'さんの'+selectMenu[selectMenu.selectedIndex].textContent+'のスコアは以下のとおりです。\n順位: '+data[0].temp_rank+' スコア: '+data[0].score);
				}
			});
	}
}