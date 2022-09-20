// WebSocketオブジェクト
let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const g_socket = new WebSocket( ws_scheme + "://" + window.location.host + "/ws/quiz/" );

const g_element_textform = document.getElementById("textform");
const g_element_textdisplay = document.getElementById("display");

function socket(){
    g_socket.send( JSON.stringify( { "content": g_element_textform.value } ) );
};

// WebSocketからデータ受信時の処理
g_socket.onmessage = ( event ) =>
{
    console.log(event);
    // テキストデータをJSONデータにデコード
    let data = JSON.parse( event.data );

    g_element_textdisplay.textContent = data["content"];

}