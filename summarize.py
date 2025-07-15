import re

def summarize_text(text):
    keywords = ['모집', '신청', '접수']
    
    # 문장 단위로 분리 (정규식 사용)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # 키워드 포함 문장 필터링
    matched = [s.strip() for s in sentences if any(k in s for k in keywords)]

    # 없으면 "해당 없음" 반환
    if not matched:
        return "키워드 포함 문장 없음"

    return ' '.join(matched)
