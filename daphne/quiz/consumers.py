import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import traceback
from urllib.parse import parse_qs
from django.utils import timezone
from datetime import datetime

from quiz.quiz_functions import *

# QuizConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class QuizConsumer( AsyncWebsocketConsumer ):
    static_group = ['INIAD_FES_06_quiz_group']

    # WebSocket接続時の処理
    async def connect( self ):
        self.room_group_name = 'INIAD_FES_06_quiz_group'

        if self.scope["user"].is_superuser:
            print("Connected admin user")
            self.uuid_str = "NOT_USE"
            self.nickname = "NOT_USE"

            # 全体送信用グループ
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            try:
                query_params = parse_qs(self.scope["query_string"].decode())
                print(query_params)
                self.uuid_str = query_params["userid"][0]
                self.nickname = query_params["nickname"][0]
                # 個別送信用グループ
                await self.channel_layer.group_add(
                    self.uuid_str,
                    self.channel_name
                )
                # 全体送信用グループ
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()

                await database_sync_to_async(event_joined_middle)(self.uuid_str)
                
            except Exception as err:
                print("ERROR: ", *traceback.format_exception_only(type(err), err))
                self.uuid_str = "NOT_USE"
                await self.close()


    # WebSocket切断時の処理
    async def disconnect( self, close_code ):
        # クイズから離脱
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.uuid_str,
            self.channel_name
        )

    # WebSocketがデータを受信した時の処理
    async def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        print("[{}] Received WebSocket:".format(datetime.strftime(timezone.now(), '%m-%d %H:%M:%S:%f')), text_data_json)

        # 管理者がデータを送信した場合の処理
        if(self.scope['user'].is_superuser):
            if (text_data_json.get("messageType") == "quizOpen"):  # 出題
                quiz_uuid = text_data_json.get("quizId")
                err = await database_sync_to_async(sequence_quiz_open)(quiz_uuid)
                await self.send(text_data=json.dumps( {"RequestSuccessed": err >= 0} ))

            elif (text_data_json.get("messageType") == "quizClose"):  # 回答締め切り
                quiz_uuid = text_data_json.get("quizId")
                err = await database_sync_to_async(sequence_quiz_close)(quiz_uuid)
                await self.send(text_data=json.dumps( {"RequestSuccessed": err >= 0} ))

            elif (text_data_json.get("messageType") == "answerSentRequest"):
                quiz_uuid = text_data_json.get("quizId")
                err = await database_sync_to_async(sequence_answer_sent_request)(quiz_uuid)
                await self.send(text_data=json.dumps( {"RequestSuccessed": err >= 0} ))

            elif (text_data_json.get("messageType") == "scoring"):  # 採点
                quiz_uuid = text_data_json.get("quizId")
                err = await database_sync_to_async(sequence_scoring)(quiz_uuid, 10)
                await self.send(text_data=json.dumps( {"RequestSuccessed": err >= 0} ))

            elif (text_data_json.get("messageType") == "rankDisplayRequest"):  # 中間、最終発表
                event_id = text_data_json.get("eventId")
                is_fin = text_data_json.get("isFin")
                err = await database_sync_to_async(sequence_rank_display)(event_id, is_fin)
                await self.send(text_data=json.dumps( {"RequestSuccessed": err >= 0} ))

            elif (text_data_json.get("messageType") == "roomActive"):  # イベント開始
                event_id = text_data_json.get("eventId")
                err = await database_sync_to_async(sequence_room_active)(event_id)
                await self.send(text_data=json.dumps( {"RequestSuccessed": err >= 0} ))

            elif (text_data_json.get("messageType") == "roomInactive"):  # イベント終了
                event_id  = text_data_json.get("eventId")
                err = await database_sync_to_async(sequence_room_inactive)(event_id)
                await self.send(text_data=json.dumps( {"RequestSuccessed": err >= 0} ))
                
            else:  # announce
                # 受信処理関数の追加
                context = {
                    "type": "spread_send",
                    "message": text_data_json
                }
                await self.channel_layer.group_send( self.room_group_name, context )

        # 参加者がデータを送信した場合の処理
        else:
            if(text_data_json.get("messageType") == "answerSent"):
                # 回答の保存
                quiz_uuid = text_data_json.get("quizId")
                choice = text_data_json.get("choice")

                user_uuid = self.uuid_str
                user_nickname = self.nickname

                err = await database_sync_to_async(sequence_save_user_answer)(quiz_uuid, user_uuid, user_nickname, choice)

                await self.send( text_data = json.dumps({"RequestSuccessed": err >= 0}))
            else:
                # 受信処理関数の追加
                await self.send(text_data=json.dumps({"RequestSuccessed": False}))

    # 拡散データ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    # キー「"type"」でのこの関数への値の指定が必要なため、純粋に送りたいメッセージは、キー「"message"」に格納。
    async def spread_send( self, data ):
        await self.send( text_data=json.dumps( data["message"] ) )