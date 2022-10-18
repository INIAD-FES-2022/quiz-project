from quiz.models import Questions, UserAnswers, Quizzes, UserData, QuizEvents, UserScores
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import traceback


# クイズに対しての採点結果を取得する。
# target_quiz_uuid: 採点したいクイズのUUID。
# 戻り値: 辞書型で正解者と不正解者に分かれたユーザのUUIDのリスト。
def get_scored_users(target_quiz_uuid):
    try:
        target_quiz = Quizzes.objects.get(id=target_quiz_uuid)
        target_answers = UserAnswers.objects.filter(quiz=target_quiz)  # 引数のクイズに対する解答のみに絞り込み。
        correctly_answered_users = target_answers.filter(choice=target_quiz.question.correctChoice).values_list("user", flat=True)  # 正しい解答と等しいもののみに
        incorrectly_answered_users = target_answers.exclude(choice=target_quiz.question.correctChoice).values_list("user", flat=True)  # 正しい回答と異なるもののみに
        scored_users = {
            "correct": correctly_answered_users,
            "incorrect": incorrectly_answered_users,
        }
    except Exception as err:
        print("ERROR: ", *traceback.format_exception_only(type(err), err))
        return {}

    return scored_users


# 対象ユーザに対して加点(減点)を行う。
# target_event_id: クイズ大会の開催回のID。
# target_users_uuid: 得点操作を行う対象のユーザのUUIDのリスト。
# points: 増減させる得点の整数値。(負数も可)
# inc_correctNums_flg: 正解数を「+1(インクリメント)」するかのフラグ。(真偽値)
# 戻り値: None
def users_add_score(target_event_id, target_users_uuid, points, inc_correctNums_flg=True):
    try:
        target_event = QuizEvents.objects.get(pk=target_event_id)
        event_joined_users = UserScores.objects.filter(event=target_event_id)  # 引数の開催回のみのスコアに絞り込み。
        
        for target_uuid in target_users_uuid:  # 指定した各ユーザに対して
            try:
                target_user = event_joined_users.get(user=target_uuid)  # 指定した開催回に対する、スコアが存在すれば取得。
            except UserScores.DoesNotExist:  # 指定した開催回に対する、スコアが存在しなければ作成。
                user_obj = UserData.objects.get(id=target_uuid)
                target_user = UserScores(event=target_event, user=user_obj)
            
            target_user.score += points  # 加点(あるいは減点)
            if inc_correctNums_flg:
                target_user.correctNums += 1  # フラグが立っていればカウント
            target_user.save()
    except Exception as err:
        print("ERROR: ", *traceback.format_exception_only(type(err), err))
        return -1
    
    return 0

# 対象ユーザに対してスコアの初期化を行う。
# target_event_id: クイズ大会の開催回のID。
# target_users_uuid: 初期化を行う対象のユーザのUUIDのリスト。
# score_flg: 得点を初期化するかのフラグ。(真偽値)
# correctNums_flg: 正解数を初期化するかのフラグ。(真偽値)
# 戻り値: None
def users_reset_score(target_event_id, target_users_uuid, score_flg=False, correctNums_flg=False):
    try:
        target_event = QuizEvents.objects.get(pk=target_event_id)
        event_joined_users = UserScores.objects.filter(event=target_event_id)  # 引数の開催回のみのスコアに絞り込み。
        
        for target_uuid in target_users_uuid:
            try:
                target_user = event_joined_users.get(user=target_uuid)  # 指定した開催回に対する、スコアが存在すれば取得。
            except UserScores.DoesNotExist:  # 指定した開催回に対する、スコアが存在しなければ作成。
                user_obj = UserData.objects.get(id=target_uuid)
                target_user = UserScores(event=target_event, user=user_obj)
            
            # フラグが立っていれば初期化
            if score_flg:
                target_user.score = 0
            if correctNums_flg:
                target_user.correctNums = 0
            
            target_user.save()
    except Exception as err:
        print("ERROR: ", *traceback.format_exception_only(type(err), err))
        return -1
    
    return 0

# 特定の開催回、ユーザのスコアを取得する。
# target_event_id: クイズ大会の開催回のID。
# target_users_uuid: 対象のユーザのUUID。指定しない場合は、開催回に参加したユーザ全て
# 戻り値: UserScoresオブジェクトまたは、そのリスト
def get_users_score(target_event_id, target_user_uuid=None):
    try:
        if target_user_uuid is None:
            ret = UserScores.objects.filter(event=target_event_id)
        else:
            ret = UserScores.objects.get(event=target_event_id, user=target_user_uuid)
    except Exception as err:
        print("ERROR: ", *traceback.format_exception_only(type(err), err))
        return None
    
    return ret

# 指定した開催回のランキングを更新する。
# target_event_id: クイズ大会の開催回のID。
# この関数を実行時に、UserScoresのtemp_rankが更新される。
def update_ranking(target_event_id):
    if target_event_id is None:
        return -1
    
    try:
        event_obj = QuizEvents.objects.get(id=target_event_id)
        event_joind_users = UserAnswers.objects.filter(quiz__event=target_event_id).values_list("user", flat=True)  # 開催回で回答したことのあるユーザを取得
        exist_score_users = UserScores.objects.filter(event=target_event_id).values_list("user", flat=True)  # 既にUserScoresが存在するユーザを取得
        not_exist_score_users = event_joind_users.difference(exist_score_users)  # 差集合で、UserScoresが存在しないユーザを抽出。
        for user in not_exist_score_users:
            user_obj = UserData.objects.get(id=user)
            UserScores.objects.create(event=event_obj, user=user_obj)
        
        # 指定した開催回のユーザのスコアを、scoreが高い順で取得。
        users_score = UserScores.objects.filter(event=target_event_id).order_by("-score")
        
        # 同率順位を計算しながらランキングを更新。
        rank = 0
        before_score = None
        tie_count = 1
        for user in users_score:
            if before_score != user.score:
                rank += tie_count
                tie_count = 1
            else:
                tie_count += 1
            user.temp_rank = rank
            before_score = user.score
            user.save()
    except Exception as err:
        print("ERROR: ", *traceback.format_exception_only(type(err), err))
        return -1
    
    return 0

# ユーザへメッセージを送信する。
# dst_user_uuid: 送信先となるユーザのUUID
# message: 送りたいメッセージ(JSON推奨)
def user_send_message(dst_user_uuid, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(dst_user_uuid),
        {
            "type": "spread_send",
            "message": message,
        }
    )

# 全ユーザへメッセージを送信。
def all_user_send_message(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "INIAD_FES_06_quiz_group",
        {
            "type": "spread_send",
            "message": message,
        }
    )

# 採点の一連の流れ
# quiz_uuid: 採点する対象のクイズ
# points: 加算したい点数
def sequence_scoring(quiz_uuid, points):
    try:
        quiz = Quizzes.objects.get(id=quiz_uuid)
        scored_users = get_scored_users(quiz_uuid)
        
        users_add_score(quiz.event.id, scored_users.get("correct"), points, True)

        message = {
            "messageType": "scoringResult",
            "correctChoice": quiz.question.correctChoice,
            "isCorrect": None,
        }

        message["isCorrect"] = True
        for user in scored_users.get("correct"):
            user_send_message(user, message)
            print(message)
        
        message["isCorrect"] = False
        for user in scored_users.get("incorrect"):
            user_send_message(user, message)
            print(message)
    except Exception as err:
        print("ERROR: ", *traceback.format_exception_only(type(err), err))
        return -1
    
    return 0

# 中間・最終発表の一連の流れ
# event_id: 発表する対象の開催回
# is_fin: 中間か最終かのフラグ
def sequence_rank_display(event_id, is_fin):
    err = update_ranking(event_id)
    if err < 0:
        return -1
    
    users_score = get_users_score(event_id)

    for user in users_score:
        message = {
            "messageType": "rankDisplay",
            "rank": user.temp_rank,
            "score": user.score,
            "correctNums": user.correctNums,
            "isFin": is_fin,
        }
        user_send_message(user.user.id, message)
        print(message)
    
    return 0


def sequence_save_user_answer(quiz_uuid, user_uuid, user_nickname, choice):
    try:
        usr_obj, _ = UserData.objects.get_or_create(id=user_uuid, defaults={"nickname": user_nickname})
        quiz_obj = Quizzes.objects.get(id=quiz_uuid)
        obj = UserAnswers(user=usr_obj, quiz=quiz_obj, choice=choice)
        obj.full_clean()
        obj.save()
    except Exception as err:
        print("ERROR: ", *traceback.format_exception_only(type(err), err))
        return -1
    
    return 0
