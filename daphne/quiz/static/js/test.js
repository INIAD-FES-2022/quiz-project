// WebSocketオブジェクト
let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
// デバッグ用パラメータ付きのリンク、実際はここのパラメータをSessionStorageからいじる。
const g_socket = new WebSocket( ws_scheme + "://" + window.location.host + "/ws/quiz/?userid=0a20a99f-4f55-4901-939b-b45859b74f46&nickname=INYAA" ); 

const g_element_textform = document.getElementById("textform");
const g_element_textdisplay = document.getElementById("display");

function socket(){
    console.log(g_element_textform.value);
    g_socket.send( g_element_textform.value );

    //g_socket.send( JSON.parse( g_element_textform.value ) );
};

// WebSocketからデータ受信時の処理
g_socket.onmessage = ( event ) =>
{
    // テキストデータをJSONデータにデコード
    let data = JSON.parse( event.data );
    console.log(data);

    g_element_textdisplay.textContent = JSON.stringify(data);

}