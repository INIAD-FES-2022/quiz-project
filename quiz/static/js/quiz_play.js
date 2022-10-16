/* 変数定義 */
const roomName = window.sessionStorage.getItem('uuid');

const quizSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/quiz/' + roomName + '/'
);

let sentenceParagraph = document.getElementById('sentence-paragraph');
let choiceA = document.getElementById('A');
let choiceB = document.getElementById('B');
let choiceC = document.getElementById('C');
let choiceD = document.getElementById('D');
let messageParagraph = document.getElementById('message-paragraph');

/* メッセージ到着時の動作*/
quizSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageType = data.messageType;
    let quizId; // 出題される問題のID、quizOpenを受信したときに代入
    /* ページに待機中の画面が表示されている場合、回答画面に切り替える */
    document.getElementById('waiting').style.visibility = 'hidden';
    
    /* messageTypeで場合分け */
    if (messageType === 'quizOpen') {
        /* 問題のIdを記録 */
        quizId = data.quizId;

        /* HTML上に問題文を表示 */
        document.getElementById('sentence-paragraph').innerText = data.sentence
        /* 回答欄挿入 */
        choiceA.innerText = data.choices[0];
        choiceB.innerText = data.choices[1];
        choiceC.innerText = data.choices[2];
        choiceD.innerText = data.choices[3];

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
        let checkedValue;
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

        /* ユーザの回答が正しかったかどうかで表示する画面を切り替える */
        let isCorrect = data.correctChoice;
        if (isCorrect) {
            /* 正解画面のメッセージを書き換え */
            document.getElementById('correctMessage').innerText = correctChoice;
            /* 正解画面を表示 */
            document.getElementById('correct').style.visibility = 'hidden';

        } else {
            /* 不正解画面のメッセージを書き換え */
            document.getElementById('incorrectMessage').innerText = correctChoice;
            /* 不正解画面を表示 */
            document.getElementById('incorrect').style.visibility = 'hidden';
        }

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
        document.getElementById('rank').innerText = String(score);
        docuemnt.getElementById('score').innerText = String(rank);
        
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
                document.getElementById('ranking').style.visibility = 'hidden'; 
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
