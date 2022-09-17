import json
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid

# QuizConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class QuizConsumer( AsyncWebsocketConsumer ):
    # WebSocket接続時の処理
    async def connect( self ):
        self.room_group_name = 'INIAD_FES_06_quiz_group'
        ch_name = self.scope["url_route"]["kwargs"]["userid"]
        # useridがNoneの場合はuuidを生成する
        if ch_name:
            self.channel_name = ch_name
        else:
            self.channel_name = str(uuid.uuid4())

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # WebSocket切断時の処理
    async def disconnect( self, close_code ):
        # クイズから離脱
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # WebSocketがデータを受信した時の処理
    async def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        # 管理者がデータを送信した場合の処理
        if(text_data_json.get( 'isStaff' )):
            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.room_group_name, text_data_json )

        # 参加者がデータを送信した場合の処理
        else:
            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.room_group_name, text_data_json )

    # 拡散データ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def spread_send( self, data ):
        await self.send( text_data=json.dumps( data ) )