// WebSocketオブジェクト
const g_socket = new WebSocket( "ws://" + window.location.host + "/ws/quiz/" );

// WebSocketに命令を送信する処理
function SendOperate(obj){
    var opType = obj.value;
    let context = {};
        // 待機中切り替え
    if(opType == "スタート"){
        context["messageType"] = "roomActivate";
        g_socket.send( JSON.stringify( context ) );
    }
    // 問題の公開
    else if(opType == "公開"){
        let context_raw = q_obj();
        console.log(context_raw);
        context["messageType"] = "quizOpen";
        context["sentence"] = context_raw["sentence"];
        context["choices"] = [
            context_raw["choiceA"],
            context_raw["choiceB"],
            context_raw["choiceC"],
            context_raw["choiceD"]
        ]
        g_socket.send( JSON.stringify( context ) );
    }
    // 任意のメッセージ
    else if(opType == "送信"){
        let text = document.getElementById("messageText").value;
        context["messageType"] = "announce";
        context["textMessage"] = text;
        g_socket.send( JSON.stringify( context ) );
    }
    // 問題を締め切る
    else if(opType == "非公開"){
        context["messageType"] = "quizClose";
        g_socket.send( JSON.stringify( context ) );
    }
    // 採点（回答の集計）
    else if(opType == "回収"){
        context["messageType"] = "answerSentRequest";
        g_socket.send( JSON.stringify( context ) );
    }
    else if (opType == "採点") {
        context["messageType"] = "scoring";
        context["quizId"] = document.getElementById("select_q").value;
        g_socket.send(JSON.stringify(context));
    }
    // 中間発表（ユーザーIDの集計）
    else if(opType == "中間発表"){
        context["messageType"] = "rankDisplayRequest";
        context["isFin"] = false;
        g_socket.send( JSON.stringify( context ) );
    }
    else if(opType == "最終発表"){
        context["messageType"] = "rankDisplayRequest";
        context["isFin"] = true;
        g_socket.send( JSON.stringify( context ) );
    }
    else{
        console.log("無効なアクセスです。");
    }
};

// WebSocketからデータ受信時の処理
g_socket.onmessage = ( event ) =>
{
    // テキストデータをJSONデータにデコード
    let data = JSON.parse( event.data );
    console.log(data);
}