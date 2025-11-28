from app.weather import get_simple_weather
from app.graph import run_agent
from app.modules.bot.schemas import ChatRequest

def is_weather_only_query(msg: str) -> bool:
    text = msg.replace(" ", "")
    weather_kw = ["날씨", "비와", "눈와", "기온어때", "기온이어때"]
    sports_kw = ["운동", "헬스장", "수영장", "운동장", "시설", "추천", "코트", "체육관"]
    return any(k in text for k in weather_kw) and not any(k in text for k in sports_kw)

def process_bot_message(req: ChatRequest) -> str:
    # 1. 날씨만 묻는 경우
    if is_weather_only_query(req.message):
        if req.user_lat is None or req.user_lon is None:
            return "날씨를 알려면 위치 정보(위도/경도)가 필요합니다."
        
        info = get_simple_weather(req.user_lat, req.user_lon)
        if info is None:
            return "지금은 기상청 날씨 정보를 가져오지 못했어요. 잠시 후 다시 시도해 주세요."
            
        temp = info["temp_c"]
        cond = info["condition"]
        
        if temp is None:
            return f"현재 하늘 상태는 {cond}입니다."
        else:
            return f"현재 기온은 약 {temp:.1f}도이고, 하늘 상태는 {cond}입니다."

    # 2. 랭체인 에이전트 처리
    user_text = req.message

    if req.user_lat is not None and req.user_lon is not None:
        location_str = (
            f"[사용자 위치 정보] 위도: {req.user_lat}, 경도: {req.user_lon}\n"
            "이 위치를 기준으로 운동 시설을 추천해줘.\n"
        )
        user_text = location_str + user_text

    metrics = []
    if req.height_cm: metrics.append(f"키: {req.height_cm}cm")
    if req.weight_kg: metrics.append(f"체중: {req.weight_kg}kg")
    if req.goal_weight_kg: metrics.append(f"목표 체중: {req.goal_weight_kg}kg")
    if req.weekly_goal_kg: metrics.append(f"주당 증감 목표: {req.weekly_goal_kg}kg")

    if metrics:
        metrics_str = "[체중 관리 프로필]\n" + ", ".join(metrics) + "\n이 정보를 활용해 조언해줘.\n"
        user_text = metrics_str + user_text

    return run_agent(user_text)