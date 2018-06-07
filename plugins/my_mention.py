# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

@respond_to('hello')
def mention_func(message):
    message.reply('hello') # メンション
    message.react('+1') # リアクション

sushida_results = {}

@respond_to('sushida')
def update_sushida_result_table(message):
    # 各点数をまとめ，テキスト形式で返却
    def results_text():
        text = ''
        for id in sushida_results:
            text += '{0}: {1}\n'.format(sushida_results[id]['name'], sushida_results[id]['result'])
        return text

    # メッセージを取得し，空白で split
    text = message.body['text'].split()
    # メッセージが sushida だけなら return
    if len(text) < 2:
        message.send(results_text())
        return
    # "sushida xxx" の xxx が10進数でなければ return
    if not text[1].isdecimal():
        message.send('以下の様に，「sushida」の後に点数を入力してください．'
            + '@uttapp sushida 1000'
            )
        return

    # 点数を更新(または結果一覧に追加)
    user_id = message.user['id']
    user_name = message.user['real_name']
    this_result = int(text[1])
    if user_id in sushida_results:
        sushida_results[user_id]['result'] = this_result
    else:
        sushida_results[user_id] = {
            'result': this_result,
            'name': user_name
        }
    message.send(results_text())

@listen_to('kawarasoba')
def listen_func(message):
    message.send('Someone said "kawarasoba"') # ただの投稿
    message.reply('You？') # メンション

# count = 0
# @default_reply()
# def default_func(message):
#     global count        # 外で定義した変数の値を変えられるようにする
#     count += 1
#     message.reply('%d 回目のデフォルトの返事です' % count)  # メンション
