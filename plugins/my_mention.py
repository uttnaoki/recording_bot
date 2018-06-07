# coding: utf-8

import sqlite3
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

dbpath = 'DB/sqlite3.db'

@respond_to('hello')
def mention_func(message):
    message.reply('hello') # メンション
    message.react('+1') # リアクション

# sushida コマンド
@respond_to('sushida')
def update_sushida_result_table(message):
    # 各点数をまとめ，テキスト形式で返却
    def results_text():
        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
        sql = 'SELECT * from sushida'
        text = ''
        for row in cur.execute(sql):
            print(row)
            text += '{0}: {1}\n'.format(row[1], row[2])
        conn.close()
        return text

    # メッセージを取得し，空白で split
    text = message.body['text'].split()

    # メッセージが sushida だけなら return
    if len(text) < 2:
        message.send(results_text())
        return

    # "sushida xxx" の xxx が10進数でなければ return
    if not text[1].isdecimal():
        message.send('以下の様に，「sushida」の後に点数を入力してください．\n'
            + '@uttapp sushida 1000'
            )
        return

    # 点数を更新(または結果一覧に追加)
    def update_sushida_db(id, name, result):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        sql = 'INSERT OR REPLACE INTO sushida (id, name, result) VALUES (?,?,?)'
        user = (id, name, result)
        c.execute(sql, user)
        conn.commit()
        conn.close()

    user_id = message.user['id']
    user_name = message.user['real_name']
    user_result = int(text[1])
    update_sushida_db(user_id, user_name, user_result)
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
