from flask import Flask, render_template, request
from telegram import Bot
import asyncio, httpcore  # 비동기 작업을 위해 asyncio 모듈을 가져옵니다.

app = Flask(__name__)
app.debug = True

TELEGRAM_BOT_TOKEN = '6560335312:AAHo82hdFJr1q_6CKUkms7NkL68kwgMul08'
TELEGRAM_CHAT_ID = '71046013'

bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    connector=httpcore.AsyncHTTPTransport,  # AsyncHTTPTransport를 사용합니다.
    max_connections=10  # 연결 풀 크기를 적절히 조정합니다.
)
# httpcore 연결 풀의 타임아웃 설정
httpcore.DEFAULT_CONNECTION_TIMEOUT = 60.0  # 60초로 타임아웃을 늘립니다.

@app.route('/')
def home():
    return render_template('report.html')

@app.route('/submit', methods=['POST'])
def submit():
    reporter = request.form['reporterName']
    location = request.form['reportLocation']
    complaint = request.form['complaint']

    message = f'신고인: {reporter}\n신고위치: {location}\n신고사항: {complaint}'

    loop = asyncio.new_event_loop()  # 비동기 작업을 위한 이벤트 루프를 생성합니다.
    asyncio.set_event_loop(loop)  # 현재 이벤트 루프를 설정합니다.

    try:
        loop.run_until_complete(send_telegram_message(message))  # 메시지 전송을 비동기로 실행합니다.
    finally:
        loop.close()  # 이벤트 루프를 닫습니다.

    return '신고가 접수되었습니다. 감사합니다!'

async def send_telegram_message(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print('An error occurred:', str(e))
