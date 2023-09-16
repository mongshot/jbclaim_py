
from flask import Flask, render_template, request
from telegram import Bot

app = Flask(__name__)
app.debug = True

TELEGRAM_BOT_TOKEN = '6560335312:AAHo82hdFJr1q_6CKUkms7NkL68kwgMul08'
TELEGRAM_CHAT_ID = '71046013'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.route('/')
def home():
    return render_template('report.html')

@app.route('/submit', methods=['POST'])
def submit():
    reporter = request.form['reporter']
    location = request.form['location']
    complaint = request.form['complaint']

    message = f'신고자: {reporter}\n위치: {location}\n불편내용: {complaint}'

    send_telegram_message(message)

    return '신고가 접수되었습니다. 감사합니다!'

def send_telegram_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print('An error occurred:', str(e))
