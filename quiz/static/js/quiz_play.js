/* 変数定義 */
const roomName = window.sessionStorage.getItem('uuid');
const nickname = window.sessionStorage.getItem('nickname');

const quizSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/quiz/?userid=' + roomName + '&nickname=' + nickname
);

let quizId; // 出題される問題のID、quizOpenを受信したときに代入
let checkedValue; // 回答者が選択している選択肢

let sentenceParagraph = document.getElementById('sentence-paragraph');
let choiceA = document.getElementById('A');
let choiceB = document.getElementById('B');
let choiceC = document.getElementById('C');
let choiceD = document.getElementById('D');
let choiceALabel = document.getElementById('A-label');
let choiceBLabel = document.getElementById('B-label');
let choiceCLabel = document.getElementById('C-label');
let choiceDLabel = document.getElementById('D-label');
let messageParagraph = document.getElementById('message-paragraph');

/* メッセージ到着時の動作*/
quizSocket.onmessage = function(e) {
    let datatmp;
    if (JSON.parse(e.data).message === undefined) {
        datatmp = JSON.parse(e.data);
    } else {
        datatmp = JSON.parse(e.data).message;
    }
    const data = datatmp;
    const messageType = data.messageType;
    /* ページに待機中の画面が表示されている場合、回答画面に切り替える */
    document.getElementById('waiting').style.visibility = 'hidden';
    
    /* messageTypeで場合分け */
    if (messageType === 'quizOpen') {
        /* 問題のIdを記録 */
        quizId = data.quizId;

        /* HTML上に問題文を表示 */
        document.getElementById('sentence-paragraph').innerText = data.sentence
        /* 回答欄挿入 */
        choiceALabel.textContent = data.choices[0];
        choiceBLabel.textContent = data.choices[1];
        choiceCLabel.textContent = data.choices[2];
        choiceDLabel.textContent = data.choices[3];

        /* 回答欄をenable */
        choiceA.disabled = false;
        choiceB.disabled = false;
        choiceC.disabled = false;
        choiceD.disabled = false;
    } else if (messageType === 'quizClose') {
        /* メッセージ欄を書き換える */
        messageParagraph.innerText = '回答を締め切りました';

        /* 回答欄をdisable */
        choiceA.disabled = true;
        choiceB.disabled = true;
        choiceC.disabled = true;
        choiceD.disabled = true;       

    } else if (messageType === 'announce') {
        /* メッセージ欄を書き換える */
        messageParagraph.innerText = data.textMessage;

    } else if (messageType === 'answerSentRequest') {
        /* 回答を取得 checkedValueは参加者の回答 choicesは選択肢すべてのelement*/
        let choices = document.getElementsByName('answer');
        for (let i=0; i<4; i++) {
            if (choices.item(i).checked){
                checkedValue = choices.item(i).value;
            }
        }

        /* 送信 */
        quizSocket.send(JSON.stringify({
            'messageType': 'answerSent',
            'userId': window.sessionStorage.getItem('uuid'),
            'quizId': quizId,
            'choice': checkedValue,
        })
        )
    } else if (messageType === 'scoringResult') {
        /* サーバから送られた正答 */
        let correctChoice = data.correctChoice;
        console.log(correctChoice);
        console.log(checkedValue);

        /* ユーザの回答が正しかったかどうかで表示する画面を切り替える */
        if (correctChoice === checkedValue) {
            /* 正解画面のメッセージを書き換え */
            document.getElementById('correctMessage').innerText = correctChoice;
            /* 正解画面を表示 */
            document.getElementById('correct').style.visibility = 'visible';

        } else {
            /* 不正解画面のメッセージを書き換え */
            document.getElementById('incorrectMessage').innerText = correctChoice;
            /* 不正解画面を表示 */
            document.getElementById('incorrect').style.visibility = 'visible';
        }

        /* ユーザの回答を無回答に変更 */
        checkedValue = "NOT_ANSWERED";

    } else if (messageType === 'userIdSentRequest') {
        /* ネームカードのIDを送信します */
        quizSocket.send(JSON.stringify({
            'userId': window.sessionStorage.getItem('uuid')
        })
        ) 

    } else if (messageType === 'rankDisplay') {
        /* 送られてきたスコアと順位に書き換えます */
        let score = data.score;
        let rank = data.rank;
        document.getElementById('rank').innerText = String(rank);
        document.getElementById('score').innerText = String(score);
        
        /* 最終発表の場合の表示 */
        if (data.isFin) {
            document.getElementById('ranking-back-to-toppage').style.visibility = 'visible';
            document.getElementById('ranking-head').innerText = '最終発表';
        } 
        /* 中間発表の場合 */
        else {
            let rankingClose = document.getElementById('ranking-close')
            rankingClose.style.visibility = 'visible';
            rankingClose.onclick = function () {
                document.getElementById('ranking').style.visibility = 'visible'; 
            }
        }    

        /* ランキングを表示 */
        document.getElementById('ranking').style.visibility = 'visible';

    }
    /* messageTypeで場合分け 終 */

    /* WebSocket 切断時の動作 */
    quizSocket.onclose = function (e) {
        alert('クイズから切断されました。ページをリロードしてください。');
        console.error('quizSocket closed unexpectedly.');
    }
}
