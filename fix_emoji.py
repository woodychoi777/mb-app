import re

# 파일 읽기
with open('/Users/xuexi/PycharmProjects/mbti/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 이모지 중복 제거
content = re.sub(r'"career": "💼 ', r'"career": "', content)
content = re.sub(r'"research": "📊 ', r'"research": "', content)
content = re.sub(r'"strength": "⚡ 강점: ', r'"strength": "', content)
content = re.sub(r'"weakness": "⚠️ 주의: ', r'"weakness": "', content)
content = re.sub(r'"tip": "💡 생존 팁: ', r'"tip": "', content)

# 파일 쓰기
with open('/Users/xuexi/PycharmProjects/mbti/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("이모지 중복 제거 완료!")
