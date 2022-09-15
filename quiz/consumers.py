import json
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid

USERNAME_SYSTEM = '*system*'
group = 'group_%s' % str(uuid.uuid4())

# QuizConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class QuizConsumer( AsyncWebsocketConsumer ):
    # コンストラクタ
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.strGroupName = group
        self.strRoomName = ''
        self.strUserName = ''
        self.strRoleType = ''

    # WebSocket接続時の処理
    async def connect( self ):
        await self.accept()

    # WebSocket切断時の処理
    async def disconnect( self ):
        # クイズから離脱
        await self.leave_quiz()

    # WebSocketがデータを受信した時の処理
    async def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        # クイズへの参加時の処理
        if( 'join' == text_data_json.get( 'messageType' ) ):
            # ルーム名(UUID)の設定
            self.strRoomName = str(uuid.uuid4())
            # ユーザー名をクラスメンバー変数に設定
            self.strUserName = text_data_json['userName']
            # 役割の取得(管理者もしくは回答者)
            self.strRoleType = text_data_json['roleType']
            # クイズへの参加
            await self.join_quiz()

        # クイズからの離脱時の処理
        elif( 'leave' == text_data_json.get( 'messageType' ) ):
            # クイズからの離脱
            await self.leave_quiz()

        # 各命令やメッセージを全体送信する処理(受け取ったデータをそのまま送信する)
        else:
            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.strGroupName, text_data_json )

    # 拡散データ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def spread_send( self, data ):
        await self.send( text_data=json.dumps( data ) )

    # クイズへの参加
    async def join_quiz( self ):
        # グループに参加
        await self.channel_layer.group_add( self.strGroupName, self.channel_name )

    # クイズからの離脱
    async def leave_quiz( self ):
        # グループから離脱
        await self.channel_layer.group_discard( self.strGroupName, self.channel_name )