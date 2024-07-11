# myproject/utils.py

from datetime import datetime
import pytz

# 현재 시간을 한국 시간대로 변환하는 함수
def convert_to_korea_time(utc_time):
    korea_tz = pytz.timezone('Asia/Seoul')
    return utc_time.astimezone(korea_tz)
