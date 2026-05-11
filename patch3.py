with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 첫 화면 상단 여백 제거
content = content.replace(
    "if st.session_state.step == 0:\n    st.markdown(\"<div style='height: 20px;'></div>\", unsafe_allow_html=True)\n    if os.path.exists(\"univ_bg.png\"):",
    "if st.session_state.step == 0:\n    if os.path.exists(\"univ_bg.png\"):"
)

# 결과 화면 상단 여백 제거
content = content.replace(
    "    my_pct = round(my_count / total * 100, 1)\n\n    st.markdown(\"<div style='height: 20px;'></div>\", unsafe_allow_html=True)\n    st.markdown(",
    "    my_pct = round(my_count / total * 100, 1)\n\n    st.markdown("
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("완료!")
