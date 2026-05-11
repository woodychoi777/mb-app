import streamlit as st
import base64
import os
import json

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"total": 0, "types": {}}

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False)

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="나의 연구실 생존 MBTI", page_icon="🎓", layout="centered")

# --- UI 숨기기 CSS 주입 ---
hide_streamlit_style = """
            <style>
            /* 상단 헤더 전체 숨기기 (Deploy 및 ... 메뉴 포함) */
            [data-testid="stHeader"] {
                visibility: hidden;
            }

            /* 혹시 모를 툴바 강제 숨김 */
            [data-testid="stToolbar"] {
                visibility: hidden !important;
            }

            /* 하단의 'Made with Streamlit' 워터마크 숨기기 */
            footer {
                visibility: hidden;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 2. 로컬 배경 이미지 적용 (Base64 변환) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    if os.path.exists(png_file):
        bin_str = get_base64(png_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        '''
    else:
        # 파일이 없을 경우 기본 배경색
        page_bg_img = '<style>.stApp { background-color: #f0f2f6; }</style>'

    st.markdown(page_bg_img, unsafe_allow_html=True)


# 모바일 최적화 스타일
st.markdown("""
    <style>
    /* 모바일 반응형 설정 */
    @media (max-width: 768px) {
        .stApp { padding: 10px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 18px !important; }
        p, div { font-size: 15px !important; line-height: 1.6 !important; }
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        padding: 18px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 16px;
        font-weight: 600;
        margin: 8px 0;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-align: left;
        line-height: 1.5;
        word-wrap: break-word;
        white-space: normal;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* 질문 박스 */
    .question-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 25px 20px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 20px 0;
        border: 2px solid rgba(102, 126, 234, 0.2);
        animation: fadeIn 0.5s ease-in;
    }
    
    /* 결과 카드 */
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin: 15px 0;
        border-left: 5px solid #667eea;
        animation: slideUp 0.6s ease-out;
    }
    
    /* 프로그레스 바 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 컬럼 내부 텍스트 강제 검은색 */
    .stColumn p, .stColumn div, .stColumn span, .stColumn strong, .stColumn b {
        color: #1a1a1a !important;
    }
    
    /* 애니메이션 정의 */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(30px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* 로딩 애니메이션 */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 뒤로가기 버튼 */
    .back-button {
        background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%) !important;
        margin-top: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 배경화면 실행 (파일명이 univ_bg.jpg 인지 확인해주세요!)
set_background("univ_bg.png")

# --- 3. 데이터 세팅 ---
questions = [
    {"q": "Q1. 코드가 터졌다! (또는 실험을 망쳤다!) 멘붕에 빠진 나의 첫 번째 행동은?",
     "options": [
         "\"선배님... 커피 드실래요...?\" 조용히 옆자리 랩원이나 선배를 찾아간다.",
         "\"답은 인터넷에 있다.\" 에러 코드를 복붙하며 폭풍 검색과 함께 혼자만의 싸움을 시작한다."
     ], "type": "EI"},

    {"q": "Q2. 내가 꿈꾸는 완벽한 랩실(연구실)의 분위기는?",
     "options": [
         "적당한 백색소음은 필수! 랩원들과 스몰톡과 아이디어가 자유롭게 오가는 활기찬 랩실.",
         "도서관 그 자체! 파티션으로 철저히 분리되어 이어폰 꽂고 집중할 수 있는 나만의 지정석."
     ], "type": "EI"},

    {"q": "Q3. 지옥 같았던 프로젝트가 드디어 끝났다! 오늘 밤 나의 스케줄은?",
     "options": [
         "\"오늘 다 죽어~!\" 고생한 랩원들과 삼겹살에 소주 한잔하며 회포 풀기.",
         "\"아무도 날 찾지 마.\" 칼퇴 후 곧장 내 방 침대로 다이빙해서 유튜브나 넷플릭스 정주행."
     ], "type": "EI"},

    {"q": "Q4. 악마가 나타나 둘 중 하나만 평생 하라고 한다. 나의 선택은?",
     "options": [
         "엑셀, 파이썬과 물아일체 되어 수만 개의 데이터 속에서 숨겨진 패턴 찾아내기.",
         "전공 서적과 씨름하며 누구도 반박할 수 없는 완벽한 논리와 수식 증명하기."
     ], "type": "DT"},

    {"q": "Q5. 산더미처럼 쌓인 영문 논문... 내 눈동자가 가장 먼저 향하는 곳은?",
     "options": [
         "\"그래서 결론이 얼만데?\" p-value와 통계 결과가 요약된 표(Table)부터 훑어본다.",
         "\"왜 이 짓을 한 거지?\" 이 연구의 배경과 뼈대를 알 수 있는 서론(Introduction)부터 읽는다."
     ], "type": "DT"},

    {"q": "Q6. 연구하면서 나도 모르게 \"미쳤다!\" 하고 짜릿함을 느끼는 순간은?",
     "options": [
         "며칠 내내 날 괴롭히던 빨간색 에러 메시지가 드디어 사라지고 'Success'가 뜰 때.",
         "산발적으로 흩어져 있던 어려운 개념들이 내 머릿속에서 완벽한 논리로 퍼즐처럼 맞춰질 때."
     ], "type": "DT"},

    {"q": "Q7. 내가 (만약) 대학원이라는 험난한 길을 선택한다면, 그 이유는?",
     "options": [
         "석/박사 타이틀 달고 더 높은 연봉과 좋은 조건으로 취업하기 위한 특급 스펙업!",
         "\"이 분야의 끝판왕이 되고 싶어!\" 나의 순수한 학문적 호기심과 지적 갈증을 채우기 위해."
     ], "type": "PA"},

    {"q": "Q8. 교수님: \"자네... 요즘 아주 핫한 주제인데, 나랑 이거 같이 해볼래?\" 나의 속마음은?",
     "options": [
         "'잠깐, 이거 나중에 내 이력서나 취업 포트폴리오에 쓸모가 있을까?'",
         "'오, 이 주제 좀 흥미로운데? 밤새워서 파고들면 진짜 재밌는 결과가 나오겠어!'"
     ], "type": "PA"},

    {"q": "Q9. 길고 길었던 학위 수여식 날! 학사모를 던지며 상상하는 나의 미래는?",
     "options": [
         "배운 지식을 실무에 바로 적용해 압도적인 성과를 내는 기업의 핵심 스페셜리스트.",
         "대학이나 국책 연구소에 남아 후학을 양성하고 끊임없이 연구를 이어가는 참된 학자."
     ], "type": "PA"},

    {"q": "Q10. 나는 어떤 스타일의 시간 관리가 더 잘 맞을까?",
     "options": [
         "\"나인 투 식스는 진리!\" 정해진 시간에 출퇴근하고 주말은 무조건 쉰다.",
         "\"밤공기가 집중력에는 최고지!\" 삘(Feel) 꽂히면 밤새고, 안 풀릴 땐 낮잠도 자는 자유로운 영혼."
     ], "type": "SF"},

    {"q": "Q11. 덜덜 떨리는 대규모 학회 발표가 2주 앞으로 다가왔다! 나의 준비 과정은?",
     "options": [
         "D-14부터 캘린더에 일정 쪼개놓고 매일매일 PPT를 한 장씩 장인처럼 깎아나간다.",
         "D-2. \"아직 시간 있어.\" 마감 직전 폭발하는 아드레날린의 힘을 믿고 벼락치기에 돌입한다."
     ], "type": "SF"},

    {"q": "Q12. 교수님: \"OO아, 이 논문 초안 언제쯤 볼 수 있을까~?\" 나의 대답은?",
     "options": [
         "\"이번 주 금요일 오후 3시까지 수정해서 메일로 보내드리겠습니다!\" (구체적)",
         "\"최대한 빨리 다듬어서 늦어도 이번 주말 안에는 보여드리겠습니다!\" (유동적)"
     ], "type": "SF"}
]

results_map = {
    "EDPS": {
        "name": "랩실의 행동대장, 프로젝트 지배자",
        "traits": "소통+데이터+실용+계획",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": '"일정 딜레이는 용납 못 해!" 팀원들을 이끌고 방대한 데이터를 척척 분석해 내는 실무 에이스입니다. 졸업 후 어느 기업을 가든 일잘러로 사랑받을 확률 100%입니다.',
        "best": "**ITAF (고독한 철학자)**\n\n**[멱살 캐리 듀오]**\n구름 잡는 소리만 하는 ITAF의 심오한 아이디어를, EDPS가 멱살을 잡고 현실로 끌어내려 기어코 데이터를 돌리고 논문으로 완성시킵니다.",
        "worst": '**ETAS (스터디 영원한 리더)**\n\n**[사공이 둘인 배]**\nEDPS는 "빨리 STATA 돌려서 실적 내자!"는데, ETAS는 "이론적 배경부터 완벽히 파고들자!"며 싸웁니다. 랩실의 주도권 쟁탈전이 벌어집니다.',
        "career": "데이터 사이언티스트, 프로젝트 매니저, 컨설턴트",
        "research": "실증 경제학, 빅데이터 분석, 정책 평가 연구",
        "strength": "팀을 이끄는 리더십, 데이터 분석 능력, 체계적인 일정 관리",
        "weakness": "완벽주의로 인한 스트레스, 융통성 부족, 팀원들에게 과도한 압박",
        "tip": "가끔은 계획을 벗어나도 괜찮아요. 커피 한 잔의 여유를 가져보세요!"
    },
    "EDPF": {
        "name": "오지랖 넓은 인싸형 실무 마스터",
        "traits": "소통+데이터+실용+유연",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": '"이 데이터 나한테 있는데, 공유해 줄까?" 주변 인맥을 총동원해 소스를 구하고 위기를 넘기는 랩실의 마당발입니다. 예측 불허의 상황에서도 가성비 좋게 결과를 뽑아냅니다.',
        "best": "**ITAS (숨막히는 원칙주의자)**\n\n**[완벽한 산학협력]**\nEDPF가 발 넓게 돌아다니며 데이터와 소스를 구해오면, 방구석에 있던 ITAS가 이를 탄탄한 이론과 FM 논문으로 포장해 주는 완벽한 분업이 일어납니다.",
        "worst": "**IDPF (방구석 해커)**\n\n**[내일의 나에게 미루기]**\n둘 다 데드라인 개념이 희박합니다(F). 내일이 교수님 미팅인데 같이 딴짓하다가 전날 밤 랩실에서 부둥켜안고 오열합니다.",
        "career": "스타트업 창업가, 마케팅 리서처, 산학협력 담당자",
        "research": "소셜 네트워크 분석, 소비자 행동 연구, 협업 플랫폼 개발",
        "strength": "뛰어난 네트워킹 능력, 위기 대처 능력, 실용적 문제 해결",
        "weakness": "산만함, 계획성 부족, 여러 일을 동시에 벌려놓고 마무리 못함",
        "tip": "인맥도 좋지만 가끔은 혼자만의 시간도 필요해요. 집중 타임을 만들어보세요!"
    },
    "EDAS": {
        "name": "학회장 단골 손님, 데이터 전도사",
        "traits": "소통+데이터+학구+계획",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": '"이 결과 흥미롭지 않아?" 자신이 분석한 데이터를 동료들에게 설명할 때 눈이 반짝입니다. 꾸준한 루틴으로 연구를 진행하며, 국내외 학회에서 네트워킹하는 것을 즐깁니다.',
        "best": "**IDPF (방구석 해커)**\n\n**[기적의 구원투수]**\n꼼꼼하게 스케줄을 짜는 EDAS가 포기할 즈음, 벼락치기 천재 IDPF가 새벽 3시에 에러를 잡아내며 기적같이 분석 결과를 던져줍니다.",
        "worst": '**ETAF (밤샘 토론 매니아)**\n\n**[속 터지는 실증주의자]**\nEDAS는 데이터를 돌려 증명하고 싶은데, ETAF는 "이 변수의 철학적 의미가 뭘까?"라며 코딩은 안 하고 입만 살아서 돌아다닙니다.',
        "career": "대학 교수, 연구소 연구원, 데이터 애널리스트",
        "research": "계량경제학, 머신러닝 응용, 학술 데이터베이스 구축",
        "strength": "학술적 열정, 체계적 연구 수행, 학회 발표 능력",
        "weakness": "학회 중독, 실무 감각 부족, 너무 학술적이라 일반인이 이해 못함",
        "tip": "학회도 좋지만 가끔은 현실 세계도 돌아보세요. 취업 시장도 체크!"
    },
    "EDAF": {
        "name": "영감 넘치는 빅데이터 예술가",
        "traits": "소통+데이터+학구+유연",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": "갑자기 엄청난 가설이 떠오르면 랩원들을 소집해 밤샘 코딩을 시작합니다. 정해진 틀보다는 삘(Feel)을 중시하며, 때론 엉뚱하지만 혁신적인 분석 결과를 만들어냅니다.",
        "best": "**ETPS (PPT의 마술사)**\n\n**[천재와 편집자]**\nEDAF가 파이썬으로 온갖 기괴하고(?) 혁신적인 분석 결과를 뱉어내면, ETPS가 이를 교수님이 좋아할 만한 깔끔한 기획서로 정제해 줍니다.",
        "worst": "**IDAF (매드 사이언티스트)**\n\n**[데이터의 늪]**\n둘 다 데이터 파도타기에 중독되었습니다. 목적(논문 완성)은 잊은 채 끝없이 변수만 추가하다가 졸업을 1년 미루게 됩니다.",
        "career": "AI 연구원, 데이터 아티스트, 혁신 연구소 연구원",
        "research": "딥러닝, 창의적 데이터 시각화, 학제간 융합 연구",
        "strength": "창의적 사고, 새로운 방법론 개척, 팀 분위기 메이커",
        "weakness": "마감 개념 부재, 너무 창의적이라 교수님이 이해 못함, 졸업 지연",
        "tip": "창의성도 좋지만 졸업이 먼저! 교수님이 원하는 걸 먼저 하세요."
    },
    "ETPS": {
        "name": "PPT의 마술사, 전략 기획자",
        "traits": "소통+이론+실용+계획",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": '"결국 핵심은 이 개념이야." 방대한 문헌과 이론을 깔끔하게 요약하여 팀 프로젝트를 하드캐리합니다. 취업과 실무에 필요한 알짜배기 스펙을 계획적으로 쌓아갑니다.',
        "best": '**IDAF (매드 사이언티스트)**\n\n**[흙 속의 진주 찾기]**\nIDAF가 목적 없이 딥다이브해서 찾아낸 복잡한 데이터 결과를, ETPS가 "이거 학회 발표용으로 딱인데?"라며 기가 막히게 살려냅니다.',
        "worst": '**EDPS (랩실 행동대장)**\n\n**[포장 vs 알맹이]**\nETPS는 발표 준비와 서론 작성에 목숨을 거는데, EDPS는 "그래서 실증 분석 결과 어딨냐고!"라며 본질적인 알맹이만 요구해 매일 충돌합니다.',
        "career": "전략 컨설턴트, 정책 연구원, 기업 기획자",
        "research": "정책 이론, 조직 이론, 전략 경영 연구",
        "strength": "뛰어난 문서 작성 능력, 이론 정리 능력, 프레젠테이션 스킬",
        "weakness": "실무 경험 부족, 이론만 강조해 실행력 약함, PPT만 예쁘고 내용 없음",
        "tip": "발표 자료도 중요하지만 실제 분석 결과가 더 중요해요. 손 좀 더러워져 보세요!"
    },
    "ETPF": {
        "name": "말빨로 교수님 홀리는 네트워커",
        "traits": "소통+이론+실용+유연",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": '"교수님, 그건 이런 관점에서 보면..." 뛰어난 임기응변과 이론적 배경을 무기로 위기를 부드럽게 넘깁니다. 빡빡한 일정 속에서도 요령껏 살아남는 랩실의 생존 전문가입니다.',
        "best": "**IDAS (인간 STATA/Python)**\n\n**[최강의 꿀빠는 조합]**\nIDAS가 묵묵히 코딩해서 완벽한 결과물을 만들어주면, ETPF가 화려한 말빨로 교수님 디펜스를 방어해 냅니다. 무임승차 같지만 효율은 최고입니다.",
        "worst": '**EDPF (오지랖 실무 마스터)**\n\n**[말만 번지르르]**\n둘 다 입은 살았고 유연한(F) 성격입니다. 서로 "네가 코딩할 거지?", "아니, 네가 데이터 클리닝한다며?" 하다가 아무것도 진행되지 않습니다.',
        "career": "영업/마케팅 전문가, 대외협력 담당, 정치인 보좌관",
        "research": "커뮤니케이션 이론, 설득 심리학, 협상 전략 연구",
        "strength": "뛰어난 말솜씨, 위기 대처 능력, 인간관계 관리 능력",
        "weakness": "실속 없음, 말만 앞서고 실행력 부족, 신뢰도 하락 위험",
        "tip": "말도 중요하지만 가끔은 행동으로 보여주세요. 신뢰가 쌓여야 오래 갑니다!"
    },
    "ETAS": {
        "name": "스터디 그룹의 영원한 리더",
        "traits": "소통+이론+학구+계획",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": "후배들이 모르는 것을 물어보면 칠판까지 동원해 원리부터 설명해 주는 참된 지식인입니다. 계획적인 문헌 탐구와 학술적 토론을 통해 랩실의 학구열을 책임집니다.",
        "best": "**IDPF (방구석 해커)**\n\n**[뼈대와 근육]**\nETAS가 짜놓은 완벽한 이론적 프레임워크(뼈대) 위에, 벼락치기형 IDPF가 막판에 폭발적인 집중력으로 데이터(근육)를 붙여 완성합니다.",
        "worst": "**ITAS (숨막히는 원칙주의자)**\n\n**[학자들의 자존심 싸움]**\n둘 다 굽힐 줄 모르는 이론형 학자들입니다. 선행연구 논문 한 줄의 해석을 두고 자존심을 건 100분 토론을 벌이다 프로젝트가 멈춥니다.",
        "career": "대학 교수, 교육 컨설턴트, 학원 강사",
        "research": "교육학, 학습 이론, 지식 전달 방법론 연구",
        "strength": "뛰어난 교육 능력, 체계적 지식 정리, 후배 양성 능력",
        "weakness": "꼰대 기질, 자기 방식만 고집, 실무보다 이론 선호",
        "tip": "가르치는 것도 좋지만 배우는 자세도 필요해요. 후배들의 새로운 아이디어도 들어보세요!"
    },
    "ETAF": {
        "name": "밤샘 토론 매니아, 예비 아인슈타인",
        "traits": "소통+이론+학구+유연",
        "traits_desc": {
            "E": "모르는 게 생기면 혼자 끙끙대기보다, 옆자리 선배나 다른 랩실 사람들에게 커피 한 잔 사 들고 가서 물어보는 인싸력!",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": "교수님과 학문적 토론을 하는 것을 두려워하지 않습니다. 호기심이 발동하면 밤새워 논문을 읽는 학자 스타일이지만, 가끔 데드라인을 놓쳐서 식은땀을 흘리기도 합니다.",
        "best": '**EDPS (랩실 행동대장)**\n\n**[몽상가와 회초리]**\n뜬구름 잡는 ETAF의 아이디어를 EDPS가 매몰차게 팩트 폭행하며 "당장 내일까지 서론 써와!"라고 통제해 주어 무사히 졸업하게 만듭니다.',
        "worst": "**ITAF (고독한 철학자)**\n\n**[신선놀음에 도끼자루 썩는다]**\n둘이 모이면 랩실이 철학관으로 변합니다. 심오한 연구 주제를 논하느라 밤을 새우지만, 정작 코딩 창은 텅 비어 있습니다.",
        "career": "철학자, 이론 물리학자, 사상가",
        "research": "순수 이론 연구, 철학적 담론, 개념적 프레임워크 구축",
        "strength": "깊은 사고력, 창의적 이론 개발, 학문적 열정",
        "weakness": "현실 감각 제로, 마감 개념 없음, 졸업 불가능",
        "tip": "이론도 중요하지만 졸업은 더 중요해요. 현실과 타협하는 법을 배워보세요!"
    },
    "IDPS": {
        "name": "칼퇴를 꿈꾸는 데이터 장인",
        "traits": "독립+데이터+실용+계획",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": '"내 코드는 완벽해. 이제 퇴근한다." 할 일만 딱 끝나면 뒤도 안 돌아보고 퇴근합니다. 쓸데없는 회의보다는 코드 에러 잡는 시간이 더 소중한 실무 특화형 인재입니다.',
        "best": "**ETPF (말빨 네트워커)**\n\n**[방패막이 확보]**\nIDPS가 제일 싫어하는 교수님 면담과 잡무를 ETPF가 다 막아줍니다. IDPS는 평화롭게 데이터만 돌리고 칼퇴할 수 있습니다.",
        "worst": '**EDPF (오지랖 실무 마스터)**\n\n**[기 빨리는 회식 요정]**\n이어폰 꽂고 조용히 코딩 좀 하려는데, EDPF가 자꾸 "오늘 다 같이 치맥 어때요?"라며 사람들을 끌어들여 IDPS의 기를 다 빨아먹습니다.',
        "career": "데이터 엔지니어, 백엔드 개발자, 퀀트 애널리스트",
        "research": "알고리즘 최적화, 데이터베이스 설계, 자동화 시스템 구축",
        "strength": "완벽한 코드 품질, 효율적인 시간 관리, 독립적 문제 해결",
        "weakness": "팀워크 부족, 소통 기피, 융통성 없음",
        "tip": "가끔은 동료들과 커피 한잔 하며 이야기 나눠보세요. 혼자만의 세계에서 벗어나면 새로운 아이디어가 생깁니다!"
    },
    "IDPF": {
        "name": "방구석 해커, 마감 직전의 에이스",
        "traits": "독립+데이터+실용+유연",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": "평소엔 조용하지만 마감일이 다가오면 엄청난 아드레날린과 타건 속도를 자랑합니다. 혼자서 벼락치기로 데이터를 돌려 기적같이 쓸만한 결과물을 만들어냅니다.",
        "best": "**ETAS (스터디 영원한 리더)**\n\n**[등대와 배]**\n어디로 튈지 모르는 IDPF에게, ETAS의 확고한 이론적 틀과 잔소리가 무사히 학위 논문을 마칠 수 있게 해주는 등대 역할을 합니다.",
        "worst": "**EDAF (빅데이터 예술가)**\n\n**[대환장 카오스]**\n계획성(S)이라곤 1도 없는 두 사람이 만났습니다. 엄청난 발견을 한 것 같아 신나게 분석하다가 며칠 뒤 흥미를 잃고 프로젝트를 던져버립니다.",
        "career": "프리랜서 개발자, 게임 개발자, 독립 연구자",
        "research": "실험적 알고리즘, 비정형 데이터 분석, 프로토타입 개발",
        "strength": "폭발적 집중력, 위기 대처 능력, 창의적 문제 해결",
        "weakness": "계획성 제로, 평소 생산성 낮음, 건강 관리 부실",
        "tip": "마감 전날 밤샘은 이제 그만! 조금씩이라도 미리미리 하는 습관을 들여보세요."
    },
    "IDAS": {
        "name": "흔들리지 않는 편안함, 인간 STATA/Python",
        "traits": "독립+데이터+학구+계획",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": '"오늘도 루틴대로." 매일 같은 자리에 앉아 조용히 데이터를 돌리고 논문을 쓰는 연구 머신입니다. 성실함과 꼼꼼함으로 교수님들의 무한한 신뢰를 받는 랩실의 기둥입니다.',
        "best": "**ETPF (말빨 네트워커)**\n\n**[영업사원과 개발자]**\n나는 묵묵히 개발(분석)만 하고 싶은데 연구비 수주나 교수님 설득은 못 하겠다면? 영업왕 ETPF가 최고의 파트너입니다.",
        "worst": "**ITAS (숨막히는 원칙주의자)**\n\n**[숨막히는 정적]**\n데이터만 보는 IDAS와 문헌만 보는 ITAS. 랩실에 단둘이 남으면 하루 종일 타건 소리와 책장 넘기는 소리만 날 뿐, 서로 말 한마디 섞지 않습니다.",
        "career": "연구소 연구원, 통계 전문가, 데이터 과학자",
        "research": "장기 데이터 분석, 재현 가능한 연구, 방법론 표준화",
        "strength": "꾸준함, 신뢰성, 완벽한 문서화",
        "weakness": "변화 거부, 새로운 시도 기피, 지루함",
        "tip": "루틴도 좋지만 가끔은 새로운 방법론도 시도해보세요. 성장은 변화에서 옵니다!"
    },
    "IDAF": {
        "name": "데이터의 늪에 빠진 매드 사이언티스트",
        "traits": "독립+데이터+학구+유연",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "D": "복잡한 수식 증명보다는, 파이썬이나 통계 프로그램을 돌려서 눈에 보이는 확실한 데이터 패턴을 찾아내는 것을 선호합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": "한번 데이터에 꽂히면 시간 가는 줄 모르고 며칠이고 혼자 파고듭니다. 남들이 뭐라든 나만의 연구를 하겠다는 순수한 학문적 열정(혹은 광기)을 가졌습니다.",
        "best": "**ETPS (PPT의 마술사)**\n\n**[번역기 장착]**\n아무도 이해 못 하는 IDAF의 기괴한 분석 코드를 ETPS가 대중적이고 실용적인 언어로 번역해 주어 세상의 빛을 보게 해 줍니다.",
        "worst": "**EDAF (빅데이터 예술가)**\n\n**[브레이크 고장난 8톤 트럭]**\n둘 다 데이터만 보면 흥분하는 타입입니다. 서로의 이상한 가설을 부추기며 통계적 유의성도 없는 데이터를 끝없이 돌리며 시간을 낭비합니다.",
        "career": "연구 중심 박사, 독립 연구자, 혁신 연구소 연구원",
        "research": "탐색적 데이터 분석, 비주류 방법론, 학제간 융합",
        "strength": "순수한 학문적 열정, 독창성, 깊은 몰입",
        "weakness": "사회성 제로, 졸업 불가능, 현실 감각 부재",
        "tip": "연구도 좋지만 사람도 만나세요. 세상과 단절되면 연구도 의미를 잃습니다!"
    },
    "ITPS": {
        "name": "효율 200% 자격증/스펙 수집가",
        "traits": "독립+이론+실용+계획",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": "남들과 어울리기보단 조용히 내 갈 길을 갑니다. 졸업 요건과 취업에 필요한 지식을 체계적으로 습득하며, 가성비와 효율을 극대화하여 조용히 승자가 되는 타입입니다.",
        "best": "**EDAF (빅데이터 예술가)**\n\n**[보물 사냥꾼]**\n톡톡 튀지만 정리가 안 된 EDAF의 연구 결과물들을, ITPS가 재빠르게 주워 담아 공모전 입상이나 취업 스펙용으로 알뜰하게 써먹습니다.",
        "worst": "**ETPS (PPT의 마술사)**\n\n**[서로 미루기 눈치게임]**\n둘 다 큰 그림(기획, PPT)만 그리고 싶어 하고 진짜 피곤한 코딩이나 데이터 클리닝(D)은 안 하려 합니다. 결국 빈 껍데기 프로젝트가 됩니다.",
        "career": "전문직(변호사, 회계사), 기술 전문가, 자격증 강사",
        "research": "응용 연구, 실무 중심 연구, 기술 문서 작성",
        "strength": "목표 지향적, 효율적 학습, 자기 관리 능력",
        "weakness": "너무 계산적, 인간미 부족, 스펙만 쌓고 경험 부족",
        "tip": "스펙도 중요하지만 실제 경험이 더 중요해요. 가끔은 비효율적이어도 도전해보세요!"
    },
    "ITPF": {
        "name": "벼락치기의 신, 가성비 천재",
        "traits": "독립+이론+실용+유연",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "P": "\"그래서 이거 하면 내 이력서에 도움 돼?\" 순수 학문 탐구보다는 당장 써먹을 수 있는 실무 스펙을 중시합니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": "두꺼운 전공 서적에서 필요한 부분만 기가 막히게 발췌해서 읽는 능력을 가졌습니다. 최소한의 노력으로 최대의 아웃풋(학점, 실적)을 뽑아내는 요령이 탁월합니다.",
        "best": "**EDAS (학회장 단골 손님)**\n\n**[무임승차 아닙니다]**\n평소엔 EDAS가 성실하게 데이터를 쌓아두고, 마감 직전 ITPF가 각성하여 화려한 문장력으로 결론과 시사점을 뽑아내는 기적의 호흡입니다.",
        "worst": "**ETPF (말빨 네트워커)**\n\n**[변명 대회 1등]**\n둘 다 벼락치기에 요령만 피우는 타입. 교수님 미팅 날 아침, 서로 자기가 코딩 안 한 그럴싸한 변명을 지어내느라 바쁩니다.",
        "career": "프리랜서, 단기 프로젝트 전문가, 컨설턴트",
        "research": "빠른 프로토타이핑, 개념 증명, 파일럿 연구",
        "strength": "빠른 학습 능력, 핵심 파악 능력, 적응력",
        "weakness": "깊이 부족, 지속성 없음, 신뢰도 낮음",
        "tip": "요령도 좋지만 가끔은 깊이 있게 파고들어보세요. 진짜 실력은 그때 생깁니다!"
    },
    "ITAS": {
        "name": "숨막히는 원리원칙주의자, 독거 학자",
        "traits": "독립+이론+학구+계획",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "S": "\"D-14부터 시작!\" 마감 훨씬 전부터 캘린더에 일정을 쪼개놓고 차근차근 진행하는 계획의 달인입니다."
        },
        "desc": "완벽한 논문을 위해 매일 정해진 루틴으로 문헌을 탐구하는 학계의 정석입니다. 빈틈없는 논리로 무장하여 심사 때 교수님들의 공격을 철벽 방어해 냅니다.",
        "best": "**EDPF (오지랖 실무 마스터)**\n\n**[우물 안 개구리 탈출]**\n이론에만 갇혀있는 ITAS에게 EDPF가 현업의 핫한 이슈와 외부 데이터를 물어다 주어 연구의 스펙트럼을 넓혀줍니다.",
        "worst": "**ETAS (스터디 영원한 리더)**\n\n**[소리 없는 아우성]**\n방향성이 조금만 달라도 절대 타협하지 않는 두 꼰대(?) 학자의 만남. 겉으로는 웃고 있지만 속으로는 서로의 이론을 경멸하고 있습니다.",
        "career": "대학 교수, 이론 연구자, 학술지 편집자",
        "research": "순수 이론 연구, 문헌 고증, 개념 정립",
        "strength": "완벽한 논리, 학문적 엄밀성, 비판적 사고",
        "weakness": "융통성 제로, 사회성 부족, 현실 적용 불가",
        "tip": "완벽주의도 좋지만 때로는 80%만 해도 충분해요. 완벽을 추구하다 아무것도 못할 수 있습니다!"
    },
    "ITAF": {
        "name": "시대를 앞서간 고독한 철학자",
        "traits": "독립+이론+학구+유연",
        "traits_desc": {
            "I": "막히는 게 있으면 스택오버플로우와 구글이 내 선생님. 혼자 조용히 해결하는 것이 가장 편하고 효율적입니다.",
            "T": "데이터를 돌리기 전에, 먼저 이 연구가 왜 필요한지 이론적 배경과 논리적 뼈대를 완벽하게 세우는 것을 중시합니다.",
            "A": "\"이 분야의 끝판왕이 되고 싶어!\" 취업 스펙보다는 순수한 학문적 호기심과 지적 갈증을 채우는 것이 연구의 원동력입니다.",
            "F": "빡빡한 계획표보다는 삘(Feel) 꽂힐 때 몰아서 하는 융통성(과 벼락치기)의 달인입니다."
        },
        "desc": "현실적인 제약보다는 나만의 학문적 세계와 통찰을 중요하게 생각합니다. 혼자서 논문을 읽다가 깊은 사색에 빠지며, 가끔 범인들은 이해하기 힘든 심오한 질문을 던집니다.",
        "best": '**EDPS (랩실 행동대장)**\n\n**[강제 하드캐리]**\n랩실 구석에서 사색만 하던 ITAF를 EDPS가 끄집어내어 키보드 앞에 앉히고 "제발 엔터 좀 쳐!"라며 강제로 실적을 만들어줍니다.',
        "worst": '**ETAF (밤샘 토론 매니아)**\n\n**[무한 루프]**\n둘 다 꼬리에 꼬리를 무는 질문에 심취해 있습니다. "이 연구의 진정한 목적이 뭘까?"라는 주제 하나로 1년을 허비할 수 있습니다.',
        "career": "철학자, 이론 물리학자, 작가",
        "research": "패러다임 전환 연구, 철학적 탐구, 개념적 혁신",
        "strength": "독창적 사고, 시대를 앞서감, 깊은 통찰",
        "weakness": "현실과 동떨어짐, 소통 불가, 이해받지 못함",
        "tip": "당신의 아이디어는 소중하지만 세상과 소통해야 빛을 발합니다. 대중화 노력도 필요해요!"
    }
}

# --- 4. 세션 상태 초기화 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {"E": 0, "I": 0, "D": 0, "T": 0, "P": 0, "A": 0, "S": 0, "F": 0}
    st.session_state.answer_history = []  # 답변 기록 추가
    st.session_state.loading = False  # 로딩 상태 추가
    st.session_state.show_detail = False  # 상세 정보 표시 여부

# --- 5. 화면 렌더링 ---
# (1) 인트로 화면
if st.session_state.step == 0:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if os.path.exists("univ_bg.png"):
        st.image("univ_bg.png", use_container_width=True)
    
    st.markdown(
        """
        <div class='question-box' style='text-align: center;'>
            <h1 style='color: #667eea; margin-bottom: 15px; font-weight: 700;'>🎓 연구실 생존 MBTI</h1>
            <p style='font-size: 16px; line-height: 1.8; color: #444; margin: 20px 0;'>
                <b style='color: #764ba2; font-size: 17px;'>"나는 교수님의 애착 인형일까,<br>고독한 연구실 늑대일까?"</b>
            </p>
            <div style='background: #f8f9ff; padding: 20px; border-radius: 15px; margin: 20px 0;'>
                <p style='font-size: 15px; line-height: 1.7; color: #555;'>
                    단 12개의 질문으로<br>
                    <b>업무 스타일 · 연구 방법론 · 시간 관리법</b>을<br> 분석하여
                    내 안에 숨겨진 '대학원생 DNA'를 찾아드립니다 🧬
                </p>
            </div>
            <p style='font-size: 14px; line-height: 1.6; color: #666;'>
                16가지 랩실 생존 유형부터<br>
                찰떡궁합 메이트와 최악의 파멸 조합까지!<br>
                지금 바로 테스트해 보세요 👀✨
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🚀 테스트 시작하기"):
        st.session_state.step = 1
        st.rerun()
    
    st.markdown(
        "<p style='text-align: center; color: #aaa; font-size: 13px; margin-top: 10px;'>made by 대학원 홍보단 최원걸</p>",
        unsafe_allow_html=True
    )

# (2) 질문 진행 화면
elif 1 <= st.session_state.step <= 12:
    q_idx = st.session_state.step - 1
    current_q = questions[q_idx]

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.progress(st.session_state.step / 12)
    st.markdown(f"<p style='text-align: center; color: #667eea; font-weight: 600; font-size: 16px; margin: 15px 0;'>질문 {st.session_state.step} / 12</p>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='question-box'>
            <h3 style='color: #333; font-size: 17px; line-height: 1.6; margin: 0; font-weight: 600;'>{current_q['q']}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )

    if st.button(f"A. {current_q['options'][0]}", key=f"opt1_{q_idx}"):
        st.session_state.scores[current_q['type'][0]] += 1
        st.session_state.answer_history.append((q_idx, 0, current_q['type'][0]))
        if st.session_state.step == 12:
            st.session_state.loading = True
        st.session_state.step += 1
        st.rerun()

    if st.button(f"B. {current_q['options'][1]}", key=f"opt2_{q_idx}"):
        st.session_state.scores[current_q['type'][1]] += 1
        st.session_state.answer_history.append((q_idx, 1, current_q['type'][1]))
        if st.session_state.step == 12:
            st.session_state.loading = True
        st.session_state.step += 1
        st.rerun()
    
    # 뒤로가기 버튼
    if st.session_state.step > 1:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⬅️ 이전 질문으로", key="back_btn"):
                # 마지막 답변 취소
                if st.session_state.answer_history:
                    last_answer = st.session_state.answer_history.pop()
                    st.session_state.scores[last_answer[2]] -= 1
                st.session_state.step -= 1
                st.rerun()

# (3) 로딩 화면
elif st.session_state.step == 13 and st.session_state.loading:
    # 통계 업데이트
    mbti_temp = ""
    mbti_temp += "E" if st.session_state.scores["E"] >= st.session_state.scores["I"] else "I"
    mbti_temp += "D" if st.session_state.scores["D"] >= st.session_state.scores["T"] else "T"
    mbti_temp += "P" if st.session_state.scores["P"] >= st.session_state.scores["A"] else "A"
    mbti_temp += "S" if st.session_state.scores["S"] >= st.session_state.scores["F"] else "F"
    stats = load_stats()
    stats["total"] += 1
    stats["types"][mbti_temp] = stats["types"].get(mbti_temp, 0) + 1
    save_stats(stats)
    count = stats["total"]
    st.markdown(
        f"""
        <div class='loading-container'>
            <div class='spinner'></div>
            <h2 style='color: #667eea; margin-top: 30px; font-size: 22px;'>🧬 {count}번째 DNA 분석 중...</h2>
            <p style='color: #666; margin-top: 10px; font-size: 16px;'>잠시만 기다려주세요</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    import time
    time.sleep(2)
    st.session_state.loading = False
    st.rerun()

# (4) 결과 화면
else:
    mbti = ""
    mbti += "E" if st.session_state.scores["E"] >= st.session_state.scores["I"] else "I"
    mbti += "D" if st.session_state.scores["D"] >= st.session_state.scores["T"] else "T"
    mbti += "P" if st.session_state.scores["P"] >= st.session_state.scores["A"] else "A"
    mbti += "S" if st.session_state.scores["S"] >= st.session_state.scores["F"] else "F"

    result = results_map[mbti]
    st.balloons()

    # 통계 로드
    stats = load_stats()
    total = stats["total"] if stats["total"] > 0 else 1
    my_count = stats["types"].get(mbti, 0)
    my_pct = round(my_count / total * 100, 1)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='question-box' style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
            <h2 style='margin: 0; font-size: 20px; font-weight: 700;'>🎉 당신의 유형은</h2>
            <h1 style='margin: 15px 0; font-size: 24px; font-weight: 800;'>{result['name']}</h1>
            <p style='font-size: 48px; font-weight: 800; margin: 10px 0; letter-spacing: 5px;'>{mbti}</p>
            <p style='font-size: 16px; margin: 8px 0; opacity: 0.95;'>전체 응시자 중 <b>{my_pct}%</b>가 같은 유형이에요!</p>
            <p style='font-size: 13px; margin: 4px 0; opacity: 0.75;'>지금까지 총 {total}명이 테스트했어요 🚀</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    img_path = f"images/{mbti}.png"
    if os.path.exists(img_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img_path, use_container_width=True)

    st.markdown(
        f"""
        <div class='result-card'>
            <p style='font-size: 16px; line-height: 1.8; color: #333; margin: 0;'>💡 {result['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 성향 조합 해석
    if 'traits_desc' in result:
        icons = {"E": "🗣️", "I": "🎧", "D": "📊", "T": "📚", "P": "💼", "A": "🔬", "S": "📅", "F": "🌙"}
        labels = {"E": "E (소통형)", "I": "I (독립형)", "D": "D (데이터/실증)", "T": "T (이론/논리)",
                  "P": "P (실용/취업지향)", "A": "A (학구/순수학문)", "S": "S (계획형)", "F": "F (유연/올빼미형)"}
        items_html = "".join([
            f"<div style='margin: 12px 0; padding: 12px 15px; background: #f8f9ff; border-radius: 12px; border-left: 4px solid #667eea;'>"
            f"<b style='color: #667eea; font-size: 15px;'>{icons.get(k, '')} {labels.get(k, k)}</b>"
            f"<p style='color: #333; font-size: 14px; margin: 6px 0 0 0; line-height: 1.6;'>{v}</p></div>"
            for k, v in result['traits_desc'].items()
        ])
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color: #764ba2;'>
                <h3 style='color: #764ba2; font-size: 18px; margin-bottom: 10px;'>🧬 나의 성향 조합 해석</h3>
                {items_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # 환상의 메이트
    best_mbti = result['best'].split('**')[1].split(' ')[0] if '**' in result['best'] else ""
    best_img_path = f"images/{best_mbti}.png"
    
    st.markdown(
        """
        <div class='result-card' style='border-left-color: #4CAF50;'>
            <h3 style='color: #4CAF50; font-size: 18px; margin-bottom: 15px;'>💙 환상의 메이트</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_best1, col_best2 = st.columns([1, 2])
    with col_best1:
        if os.path.exists(best_img_path):
            st.image(best_img_path, use_container_width=True)
    with col_best2:
        # Markdown의 ** 처리를 HTML로 변환
        best_text = result['best'].replace('**', '<strong style="color: #1a1a1a;">')
        best_text = best_text.replace('**', '</strong>')
        st.markdown(
            f"<div style='background: white; padding: 15px; border-radius: 10px;'><p style='font-size: 15px; line-height: 1.7; color: #1a1a1a !important; margin: 0; white-space: pre-line;'>{best_text}</p></div>",
            unsafe_allow_html=True
        )

    # 최악의 파멸 조합
    worst_mbti = result['worst'].split('**')[1].split(' ')[0] if '**' in result['worst'] else ""
    worst_img_path = f"images/{worst_mbti}.png"
    
    st.markdown(
        """
        <div class='result-card' style='border-left-color: #f44336; margin-top: 20px;'>
            <h3 style='color: #f44336; font-size: 18px; margin-bottom: 15px;'>💣 최악의 파멸 조합</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_worst1, col_worst2 = st.columns([1, 2])
    with col_worst1:
        if os.path.exists(worst_img_path):
            st.image(worst_img_path, use_container_width=True)
    with col_worst2:
        # Markdown의 ** 처리를 HTML로 변환
        worst_text = result['worst'].replace('**', '<strong style="color: #1a1a1a;">')
        worst_text = worst_text.replace('**', '</strong>')
        st.markdown(
            f"<div style='background: white; padding: 15px; border-radius: 10px;'><p style='font-size: 15px; line-height: 1.7; color: #1a1a1a !important; margin: 0; white-space: pre-line;'>{worst_text}</p></div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # 더 알아보기 버튼
    col_detail1, col_detail2, col_detail3 = st.columns([1, 2, 1])
    with col_detail2:
        if st.button("📖 더 알아보기 (추천 진로 & 연구 분야)"):
            st.session_state.show_detail = not st.session_state.show_detail
            st.rerun()
    
    # 상세 정보 표시
    if st.session_state.show_detail and 'career' in result:
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color: #FF9800; animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #FF9800; font-size: 18px; margin-bottom: 15px;'>🎯 당신에게 추천하는 진로</h3>
                <p style='font-size: 15px; line-height: 1.7; color: #333; margin: 10px 0;'>{result.get('career', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color: #2196F3; animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #2196F3; font-size: 18px; margin-bottom: 15px;'>🔬 추천 연구 분야</h3>
                <p style='font-size: 15px; line-height: 1.7; color: #333; margin: 10px 0;'>{result.get('research', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color: #4CAF50; animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #4CAF50; font-size: 18px; margin-bottom: 15px;'>💪 당신의 강점</h3>
                <p style='font-size: 15px; line-height: 1.7; color: #333; margin: 10px 0;'>{result.get('strength', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color: #f44336; animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #f44336; font-size: 18px; margin-bottom: 15px;'>⚠️ 주의할 점</h3>
                <p style='font-size: 15px; line-height: 1.7; color: #333; margin: 10px 0;'>{result.get('weakness', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div class='result-card' style='border-left-color: #9C27B0; animation: fadeIn 0.5s ease-in;'>
                <h3 style='color: #9C27B0; font-size: 18px; margin-bottom: 15px;'>💡 생존 팁</h3>
                <p style='font-size: 15px; line-height: 1.7; color: #333; margin: 10px 0;'>{result.get('tip', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # 인스타 버튼 (중앙)
    col_i1, col_i2, col_i3 = st.columns([1, 2, 1])
    with col_i2:
        st.markdown(
            "<a href='https://www.instagram.com/knu_monit?igsh=MWF4bnluN200Z2Exdw==' target='_blank'>"
            "<button style='width:100%; border-radius:25px; padding:18px 20px; "
            "background:linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); "
            "color:white; font-size:16px; font-weight:600; border:none; cursor:pointer;'>"
            "📸 대학원 홍보단 인스타</button></a>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 다시 테스트 + 링크 복사
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 다시 테스트하기"):
            st.session_state.step = 0
            st.session_state.scores = {"E": 0, "I": 0, "D": 0, "T": 0, "P": 0, "A": 0, "S": 0, "F": 0}
            st.session_state.answer_history = []
            st.session_state.loading = False
            st.session_state.show_detail = False
            st.rerun()
    with col_b:
        share_url = "https://your-app-url.com"  # 실제 배포 URL로 변경
        if st.button("🔗 테스트 링크 복사하기"):
            st.code(share_url, language=None)
            st.success("링크를 복사해서 친구들과 공유하세요! 📤")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)