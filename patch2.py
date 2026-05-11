with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = """    result = results_map[mbti]
    st.balloons()

    st.markdown(\"<div style='height: 20px;'></div>\", unsafe_allow_html=True)
    st.markdown(
        f\"\"\"
        <div class='question-box' style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
            <h2 style='margin: 0; font-size: 20px; font-weight: 700;'>🎉 당신의 유형은</h2>
            <h1 style='margin: 15px 0; font-size: 24px; font-weight: 800;'>{result['name']}</h1>
            <p style='font-size: 48px; font-weight: 800; margin: 10px 0; letter-spacing: 5px;'>{mbti}</p>
        </div>
        \"\"\", 
        unsafe_allow_html=True
    )"""

new = """    result = results_map[mbti]
    st.balloons()

    # 통계 로드
    stats = load_stats()
    total = stats["total"] if stats["total"] > 0 else 1
    my_count = stats["types"].get(mbti, 0)
    my_pct = round(my_count / total * 100, 1)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f\"\"\"
        <div class='question-box' style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
            <h2 style='margin: 0; font-size: 20px; font-weight: 700;'>🎉 당신의 유형은</h2>
            <h1 style='margin: 15px 0; font-size: 24px; font-weight: 800;'>{result['name']}</h1>
            <p style='font-size: 48px; font-weight: 800; margin: 10px 0; letter-spacing: 5px;'>{mbti}</p>
            <p style='font-size: 16px; margin: 8px 0; opacity: 0.95;'>전체 응시자 중 <b>{my_pct}%</b>가 같은 유형이에요!</p>
            <p style='font-size: 13px; margin: 4px 0; opacity: 0.75;'>지금까지 총 {total}명이 테스트했어요 🚀</p>
        </div>
        \"\"\",
        unsafe_allow_html=True
    )"""

if old in content:
    content = content.replace(old, new)
    print("✓ 패치 성공")
else:
    print("✗ 패치 실패")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
