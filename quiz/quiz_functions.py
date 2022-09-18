from quiz.models import Questions, UserAnswers, Quizzes, UserData, QuizEvents, UserScores

# クイズに対しての採点結果を取得する。
# target_quiz_uuid: 採点したいクイズのUUID。
# 戻り値: 辞書型で正解者と不正解者に分かれたユーザのUUIDのリスト。
def get_scored_users(target_quiz_uuid):
    target_quiz = Quizzes.objects.get(id=target_quiz_uuid)
    target_answers = UserAnswers.objects.filter(quiz=target_quiz)  # 引数のクイズに対する解答のみに絞り込み。
    correctly_answered_users = target_answers.filter(choice=target_quiz.question.correctChoice).values_list("user", flat=True)  # 正しい解答と等しいもののみに
    incorrectly_answered_users = target_answers.exclude(choice=target_quiz.question.correctChoice).values_list("user", flat=True)  # 正しい回答と異なるもののみに
    scored_users = {
        "correct": correctly_answered_users,
        "incorrect": incorrectly_answered_users,
    }
    return scored_users


# 対象ユーザに対して加点(減点)を行う。
# target_event_id: クイズ大会の開催回のID。
# target_users_uuid: 得点操作を行う対象のユーザのUUIDのリスト。
# points: 増減させる得点の整数値。(負数も可)
# inc_correctNums_flg: 正解数を「+1(インクリメント)」するかのフラグ。(真偽値)
# 戻り値: None
def users_add_score(target_event_id, target_users_uuid, points, inc_correctNums_flg=True):
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

# 対象ユーザに対してスコアの初期化を行う。
# target_event_id: クイズ大会の開催回のID。
# target_users_uuid: 初期化を行う対象のユーザのUUIDのリスト。
# score_flg: 得点を初期化するかのフラグ。(真偽値)
# correctNums_flg: 正解数を初期化するかのフラグ。(真偽値)
# 戻り値: None
def users_reset_score(target_event_id, target_users_uuid, score_flg=False, correctNums_flg=False):
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

# 特定の開催回、ユーザのスコアを取得する。
# target_event_id: クイズ大会の開催回のID。
# target_users_uuid: 初期化を行う対象のユーザのUUID。
# 戻り値: UserScoresオブジェクト
def get_user_score(target_event_id, target_user_uuid):
    target_user = UserScores.objects.get(event=target_event_id, user=target_user_uuid)
    return target_user

# 指定した開催回のランキングを更新する。
# target_event_id: クイズ大会の開催回のID。
# この関数を実行時に、UserScoresのtemp_rankが更新される。
def update_ranking(target_event_id):
    event_joined_users = UserScores.objects.filter(event=target_event_id).order_by("-score")  # 指定した開催回のユーザのスコアを、scoreが高い順で取得。

    # 同率順位を計算しながらランキングを更新。
    rank = 0
    before_score = None
    tie_count = 1
    for user in event_joined_users:
        if before_score != user.score:
            rank += tie_count
            tie_count = 1
        else:
            tie_count += 1
        user.temp_rank = rank
        before_score = user.score
        user.save()