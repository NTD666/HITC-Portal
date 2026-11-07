import pandas as pd

GRADE_WEIGHTS = {
    "Điểm chuyên cần (10%)": 0.1,
    "Điểm kiểm tra giữa kỳ (30%)": 0.3,
    "Điểm thi kết thúc học phần (60%)": 0.6,
}

def calculate_subject_grades(records_df: pd.DataFrame) -> pd.DataFrame:
    """
    Tính điểm tổng kết cho từng môn học theo đúng quy chế đào tạo HITC:
    - Điểm chuyên cần (10%)
    - Điểm kiểm tra giữa kỳ (30%)
    - Điểm thi kết thúc học phần (60%)
    Nếu môn chưa có đủ 3 đầu điểm, hệ thống chuẩn hóa theo tổng trọng số hiện có.
    """
    if records_df.empty:
        return pd.DataFrame(columns=["Môn học", "Điểm tổng kết", "Số đầu điểm"])
    
    rows = []
    for subject, group in records_df.groupby("Môn học", sort=False):
        total_weight = 0.0
        weighted_sum = 0.0
        for _, row in group.iterrows():
            weight = GRADE_WEIGHTS.get(row["Loại điểm"], 0.0)
            weighted_sum += float(row["Điểm số"]) * weight
            total_weight += weight
            
        final_score = (weighted_sum / total_weight) if total_weight > 0 else float(group["Điểm số"].mean())
        rows.append({
            "Môn học": subject,
            "Điểm tổng kết": round(final_score, 2),
            "Số đầu điểm": len(group)
        })
    return pd.DataFrame(rows)

def get_academic_rank(gpa: float) -> str:
    """Phân loại học lực theo chuẩn đào tạo tín chỉ."""
    if gpa >= 8.5:
        return "Xuất sắc 🏆"
    elif gpa >= 8.0:
        return "Giỏi 🥇"
    elif gpa >= 6.5:
        return "Khá 🥈"
    elif gpa >= 5.0:
        return "Trung bình 🥉"
    else:
        return "Yếu"
