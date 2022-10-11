// WebSocketオブジェクト
const g_socket = new WebSocket( "ws://" + window.location.host + "/ws/quiz/" );

// WebSocketに命令を送信する処理
function SendOperate(obj){
    var opType = obj.value;
    // 待機中切り替え
    if(opType == "スタート"){
        let context = {}
        context["messageType"] = "roomActivate";
        g_socket.send( JSON.stringify( context ) );
    }
    // 問題の公開
    else if(opType == "公開"){
        let context = {};
        let context_raw = q_obj();
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
        let context = {}
        let text = document.getElementById("messageText").value;
        context["messageType"] = "announce";
        context["textMessage"] = text;
        g_socket.send( JSON.stringify( context ) );
    }
    // 問題を締め切る
    else if(opType == "非公開"){
        let context = {}
        context["messageType"] = "quizClose";
        g_socket.send( JSON.stringify( context ) );
    }
    // 採点（回答の集計）
    else if(opType == "採点"){
        let context = {}
        context["messageType"] = "answerSentRequest";
        g_socket.send( JSON.stringify( context ) );
    }
    // 中間発表（ユーザーIDの集計）
    else if(opType == "中間発表"){
        let context = {}
        context["messageType"] = "userIdSentRequest";
        g_socket.send( JSON.stringify( context ) );
    }
    else{
        console.log("無効なアクセスです。");
    }
};