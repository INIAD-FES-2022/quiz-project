/* 変数定義 */
const roomName = window.sessionStorage.getItem('uuid');

cosnt quizSocket = new WebSocket(
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
    const quizId; // 出題される問題のID、quizOpenを受信したときに代入
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
    }
}
