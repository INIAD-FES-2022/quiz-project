import json
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid

from quiz.models import UserAnswers
from quiz.quiz_functions import *

# QuizConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class QuizConsumer( AsyncWebsocketConsumer ):
    groups = []
    static_group = ['INIAD_FES_06_quiz_group']

    # WebSocket接続時の処理
    async def connect( self ):
        self.room_group_name = 'INIAD_FES_06_quiz_group'
        # useridが無い場合はuuidを生成する
        try:
            self.uuid_str = self.scope["url_route"]["kwargs"]["userid"]
            self.nickname = self.scope["url_route"]["kwargs"]["nickname"]
        except:
            print("Error: Incorrect parameter")

        QuizConsumer.groups.append(self.uuid_str)

        # 全体送信用グループ
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # 個別送信用グループ
        await self.channel_layer.group_add(
            self.uuid_str,
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
        await self.channel_layer.group_discard(
            self.uuid_str,
            self.channel_name
        )
        QuizConsumer.groups.remove(self.uuid_str)

    # WebSocketがデータを受信した時の処理
    async def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )
        user = self.scope['user']

        # 管理者がデータを送信した場合の処理
        if(user.is_authenticated):
            # 中間、最終発表の際にランキングを更新する。
            if(text_data_json.get("messageType") == "userIdSentRequest"):
                eId = text_data_json["eventId"]
                update_ranking(eId)

            # 受信処理関数の追加
            text_data_json["type"]="spread_send"
            await self.channel_layer.group_send( self.room_group_name, text_data_json )

        # 参加者がデータを送信した場合の処理
        else:
            if(text_data_json.get("messageType") == "answerSent"):
                # 回答の保存
                uId = text_data_json["userId"]
                qId = text_data_json["quizId"]
                cId = text_data_json["choice"]
                usr_obj, _ = UserData.objects.get_or_create(id=uId, defaults={"nickname": self.nickname})
                obj = UserAnswers(user=usr_obj, quiz=qId, choice=cId)
                obj.save()

                await self.send( text_data = json.dumps({"RequestStatus": "Success"}))

            elif(text_data_json.get("messageType") == "userIdSent"):
                eId = text_data_json["eventId"]
                uId = text_data_json["userId"]
                isFin = text_data_json["isFin"]
                uScore = get_users_score(eId, uId)
                data = {
                    "messageType": "rankDisplay",
                    "rank": uScore.temp_rank,
                    "score": uScore.score,
                    "isFin": isFin,
                }
                self.send( text_data = json.dumps( data ) )

            else:
                # 受信処理関数の追加
                text_data_json["type"]="spread_send"
                await self.channel_layer.group_send( self.room_group_name, text_data_json )

    # 拡散データ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def spread_send( self, data ):
        await self.send( text_data=json.dumps( data ) )