import pandas as pd
import chardet

# 파일의 인코딩 감지
with open('timetable.csv', 'rb') as f:
    result = chardet.detect(f.read())

# 감지된 인코딩으로 파일 읽고 UTF-8로 저장
try:
    df = pd.read_csv('timetable.csv', encoding=result['encoding'])
    df.to_csv('timetable_utf8.csv', index=False, encoding='utf-8')
    print(f"CSV 파일이 UTF-8로 변환되었습니다. 인코딩: {result['encoding']}")
except Exception as e:
    print(f"오류 발생: {e}")
