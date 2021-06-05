from datetime import datetime

import thecampy

SOLDIER = thecampy.Soldier(
    '문승기', 20010527, 20210607, '육군훈련소'
)


def send(subject, content):
    content += '\n[FINISH]'
    msg_num = 0
    char_count, enter_count = 0, 0
    buffer = []
    for i, char in enumerate(content):
        buffer.append(char)
        char_count += 1
        if char == '\n':
            enter_count += 1

        if char_count > 1495 or enter_count > 22 or i == len(content) - 1:
            _send(subject + f" - {msg_num}", ''.join(buffer))

            char_count, enter_count = 0, 0
            buffer = []

            msg_num += 1


def _send(subject, content):
    try:
        message = thecampy.Message(subject, content)
        client = thecampy.client()
        client.login('ns_giya@naver.com', 'mtmdg052701*')
        client.get_soldier(SOLDIER)
        client.send_message(SOLDIER, message)
        print(f"[+] {datetime.now()} - NEWS SENT")
    except:
        print(f"[-] {datetime.now()} - SEND FAILED")