import os
import sys
import tempfile
from pathlib import Path
import pandas as pd
from typing import Optional, Dict, Any

# Đảm bảo LOCALAPPDATA trỏ đến thư mục có quyền ghi trước khi import crewai
if sys.platform == "win32":
    try:
        test_cred_path = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "crewai" / "credentials"
        test_cred_path.mkdir(parents=True, exist_ok=True)
    except Exception:
        fallback_dir = Path(tempfile.gettempdir()) / "crewai_local"
        fallback_dir.mkdir(parents=True, exist_ok=True)
        os.environ["LOCALAPPDATA"] = str(fallback_dir)

# Flag kiểm tra xem crewai đã được cài đặt trong môi trường hay chưa
try:
    from crewai import Agent, Crew, Process, Task, LLM
    CREWAI_AVAILABLE = True
except Exception:
    CREWAI_AVAILABLE = False


def build_academic_analysis_prompt(student_name: str, student_id: str, student_class: str, records_df: pd.DataFrame, gpa: float, academic_rank: str) -> str:
    """Tạo chuỗi dữ liệu tổng hợp về kết quả học tập của sinh viên."""
    table_summary = records_df.to_string(index=False)
    
    # Tìm môn cao nhất và thấp nhất
    top_subjects = records_df.sort_values(by="Điểm số", ascending=False).head(3)
    weak_subjects = records_df.sort_values(by="Điểm số", ascending=True).head(3)
    
    prompt = f"""
THÔNG TIN SINH VIÊN:
- Họ và tên: {student_name}
- MSSV: {student_id}
- Lớp: {student_class}
- Điểm trung bình (GPA): {gpa:.2f}/10
- Học lực dự kiến: {academic_rank}

CHI TIẾT CÁC ĐẦU ĐIỂM HỌC PHẦN:
{table_summary}

MÔN CÓ ĐIỂM CAO NHẤT:
{top_subjects[['Môn học', 'Điểm số', 'Học kỳ']].to_string(index=False)}

MÔN CẦN LƯU Ý / ĐIỂM THẤP NHẤT:
{weak_subjects[['Môn học', 'Điểm số', 'Học kỳ']].to_string(index=False)}
"""
    return prompt.strip()


def generate_smart_academic_advice(
    student_name: str,
    student_id: str,
    student_class: str,
    records_df: pd.DataFrame,
    gpa: float,
    academic_rank: str
) -> str:
    """
    Hệ chuyên gia cố vấn học vụ & định hướng CNTT HITC nội bộ (Không cần API Key).
    Tự động phân tích các nhóm môn học, thế mạnh, điểm yếu và đưa ra lộ trình cụ thể.
    """
    if records_df.empty:
        return "Chưa có đủ dữ liệu học phần để hệ thống phân tích học lực."

    from grade_calculator import calculate_subject_grades
    subject_summary = calculate_subject_grades(records_df)

    top_subjects = subject_summary.sort_values(by="Điểm tổng kết", ascending=False).head(3)
    weak_subjects = subject_summary.sort_values(by="Điểm tổng kết", ascending=True).head(3)

    # Phân loại nguy cơ học vụ
    fail_subjects = subject_summary[subject_summary["Điểm tổng kết"] < 5.0]
    warn_subjects = subject_summary[(subject_summary["Điểm tổng kết"] >= 5.0) & (subject_summary["Điểm tổng kết"] < 6.5)]
    strong_subjects = subject_summary[subject_summary["Điểm tổng kết"] >= 8.0]

    # Đánh giá khuynh hướng chuyên ngành CNTT
    all_subject_names = " ".join(subject_summary["Môn học"].tolist()).lower()
    career_suggestions = []
    
    if any(k in all_subject_names for k in ["python", "web", "react", "php", "c#", "java", "oop", "lập trình", "phần mềm"]):
        career_suggestions.append("**Phát triển Phần mềm & Lập trình Web/Mobile** (Tận dụng tốt tư duy thuật toán và lập trình thực chiến).")
    if any(k in all_subject_names for k in ["mạng", "ccna", "linux", "an toàn", "bảo mật", "máy chủ", "server"]):
        career_suggestions.append("**Quản trị Hệ thống, Mạng & An toàn thông tin / DevOps** (Phù hợp với hạ tầng mạng và máy chủ).")
    if any(k in all_subject_names for k in ["dữ liệu", "sql", "mysql", "ai", "học máy", "data"]):
        career_suggestions.append("**Quản trị Cơ sở Dữ liệu & Kỹ sư Dữ liệu / AI** (Thế mạnh về mô hình dữ liệu và SQL).")

    if not career_suggestions:
        career_suggestions.append("**Kỹ sư Công nghệ Thông tin Ứng dụng Toàn diện** (Nền tảng đồng đều giữa lập trình và hạ tầng).")

    top_str = "\n".join([f"- 🌟 **{row['Môn học']}**: `{row['Điểm tổng kết']}/10` điểm" for _, row in top_subjects.iterrows()])
    
    if not fail_subjects.empty:
        risk_str = "⚠️ **CẢNH BÁO NGUY CƠ HỌC VỤ:** Có " + str(len(fail_subjects)) + " môn học có điểm tổng kết dưới 5.0 (cần đặc biệt lưu ý nguy cơ thi lại / học lại cải thiện): **" + ", ".join(fail_subjects["Môn học"].tolist()) + "**."
    elif not warn_subjects.empty:
        risk_str = "⚡ **LƯU Ý CẢI THIỆN:** Có học phần ở mức trung bình (5.0 - 6.5) cần bổ sung kiến thức để kéo chuẩn GPA: **" + ", ".join(warn_subjects["Môn học"].tolist()) + "**."
    else:
        risk_str = "🎉 **TIẾN ĐỘ RẤT TỐT:** Toàn bộ các học phần của bạn đều đạt chuẩn đầu ra (không có môn nào dưới 5.0)."

    advice_md = f"""
## 🎓 BÁO CÁO CỐ VẤN HỌC TẬP & ĐỊNH HƯỚNG NGHỀ NGHIỆP CNTT - HITC

**Sinh viên:** `{student_name}` | **MSSV:** `{student_id}` | **Lớp:** `{student_class}`  
**Điểm trung bình tích lũy (GPA):** `{gpa:.2f} / 10` — **Học lực dự kiến:** `{academic_rank}`

---

### 1. 📊 Đánh Giá Năng Lực Học Tập & Thế Mạnh Nổi Trội
- **Các môn học đạt kết quả cao nhất:**
{top_str}
- **Tình trạng học vụ:**
{risk_str}

---

### 2. 🎯 Kế Hoạch Hành Động Cá Nhân Hóa (4 Bước Chuẩn HITC)
1. **Tận dụng tối đa trọng số thành phần:** Hãy duy trì 10% điểm chuyên cần (đi học đủ, đúng giờ) và đạt ít nhất 7-8 điểm ở 30% giữa kỳ để tạo tâm lý tự tin trước kỳ thi kết thúc học phần (60%).
2. **Cải thiện môn điểm thấp:** Dành thêm 45 - 60 phút mỗi ngày thực hành trực tiếp trên máy tính cá nhân hoặc phòng máy thực hành khoa CNTT HITC.
3. **Chiến lược học nhóm:** Tích cực tham gia các buổi học nhóm, trao đổi đồ án tại Thư viện trường HITC (Cơ sở 20 Tăng Nhơn Phú).
4. **Xây dựng Project thực tế:** Biến các bài tập lớn môn học thành dự án thực chiến lưu trữ trên GitHub để làm hồ sơ ứng tuyển doanh nghiệp.

---

### 3. 💼 Gợi Ý Hướng Chuyên Ngành CNTT Phù Hợp
Dựa trên các học phần bạn đã tích lũy, Ban Cố vấn Khoa CNTT - HITC gợi ý các hướng đi tiềm năng:
""" + "\n".join([f"- {s}" for s in career_suggestions]) + """

---

### 💌 Lời Nhắn Từ Giảng Viên Khoa CNTT - HITC:
> *"Học tập tại Trường Cao đẳng Công thương TP.HCM là một hành trình rèn luyện kỹ năng thực tế. Hãy tự tin phát huy thế mạnh của mình và kiên trì từng ngày. Thầy cô Khoa CNTT luôn sẵn sàng đồng hành cùng bạn!"*
"""
    return advice_md.strip()


def run_crewai_advisor(
    student_name: str,
    student_id: str,
    student_class: str,
    records_df: pd.DataFrame,
    gpa: float,
    academic_rank: str,
    api_key: Optional[str] = None,
    provider: str = "openai",
    model_name: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """
    Kích hoạt phi đội AI Agents (CrewAI) hoặc tự động chuyển sang Chế độ Chuyên gia Nội bộ nếu không có API Key.
    """
    # Nếu không có API Key hoặc không có crewai, kích hoạt ngay Chế độ Cố vấn Nội bộ
    has_key = bool(
        os.getenv("OPENAI_API_KEY") 
        or os.getenv("GEMINI_API_KEY") 
        or os.getenv("GROQ_API_KEY")
        or api_key
    )
    
    if not has_key or not CREWAI_AVAILABLE:
        # Chạy chế độ Cố vấn Chuyên sâu Nội bộ mà không cần API Key!
        smart_output = generate_smart_academic_advice(
            student_name, student_id, student_class, records_df, gpa, academic_rank
        )
        return {
            "success": True,
            "output": smart_output,
            "mode": "offline"
        }

    # Thiết lập API Key cho CrewAI
    if api_key:
        if provider == "openai":
            os.environ["OPENAI_API_KEY"] = api_key
        elif provider == "gemini":
            os.environ["GEMINI_API_KEY"] = api_key

    student_data_text = build_academic_analysis_prompt(
        student_name, student_id, student_class, records_df, gpa, academic_rank
    )

    try:
        # Cấu hình LLM
        llm_instance = None
        if provider == "gemini":
            model_target = f"gemini/{model_name}" if not model_name.startswith("gemini/") else model_name
            llm_instance = LLM(model=model_target, api_key=api_key or os.getenv("GEMINI_API_KEY"))
        else:
            llm_instance = LLM(model=model_name, api_key=api_key or os.getenv("OPENAI_API_KEY"))

        # 1. Agent 1: Chuyên viên Phân tích Học lực HITC
        analyst = Agent(
            role="Chuyên viên Phân tích Học lực Sinh viên HITC",
            goal="Đánh giá chi tiết bảng điểm, chỉ rõ môn thế mạnh, môn yếu cần cải thiện và cảnh báo nguy cơ học vụ.",
            backstory=(
                "Bạn là chuyên viên khảo thí và đảm bảo chất lượng đào tạo tại Trường Cao đẳng Công thương TP.HCM (HITC). "
                "Bạn có sự thấu hiểu sâu sắc về chuẩn đầu ra các môn học CNTT và khả năng phân tích năng lực sinh viên công tâm, chuẩn xác."
            ),
            llm=llm_instance,
            verbose=False
        )

        # 2. Agent 2: Cố vấn Lộ trình Học tập & Hướng nghiệp CNTT
        advisor = Agent(
            role="Cố vấn Lộ trình Học tập & Hướng nghiệp CNTT",
            goal="Đưa ra kế hoạch học tập cá nhân hóa, phương pháp ôn tập môn điểm thấp và định hướng chuyên ngành phù hợp dựa trên kết quả học tập.",
            backstory=(
                "Bạn là giảng viên cao cấp và cố vấn hướng nghiệp Khoa CNTT - HITC. "
                "Bạn luôn truyền cảm hứng, đưa ra lời khuyên thực tế gắn liền với nhu cầu tuyển dụng của doanh nghiệp phần mềm."
            ),
            llm=llm_instance,
            verbose=False
        )

        # Task 1: Phân tích kết quả học tập
        task_analysis = Task(
            description=(
                f"Phân tích dữ liệu học tập sau của sinh viên HITC:\n{student_data_text}\n\n"
                "Yêu cầu:\n"
                "1. Nhận xét tổng quan về GPA và phân loại học lực.\n"
                "2. Xác định các môn học thế mạnh nổi trội (điểm cao).\n"
                "3. Chỉ ra các môn học đang bị đuối hoặc có nguy cơ cần cải thiện.\n"
                "4. Đánh giá tính cân bằng giữa các khối kiến thức (Đại cương, Cơ sở ngành, Lập trình/Mạng)."
            ),
            expected_output="Bản báo cáo phân tích năng lực học tập chi tiết bằng tiếng Việt, có chia mục rõ ràng, súc tích.",
            agent=analyst
        )

        # Task 2: Tư vấn kế hoạch học tập & hướng nghiệp
        task_advisory = Task(
            description=(
                "Dựa trên kết quả phân tích năng lực từ Task 1 và thông tin sinh viên, hãy:\n"
                "1. Đưa ra 3-5 hành động cụ thể giúp sinh viên cải thiện điểm số các môn yếu ngay trong kỳ tới.\n"
                "2. Đề xuất phương pháp học tập và tự học hiệu quả cho ngành CNTT.\n"
                "3. Gợi ý hướng chuyên ngành phù hợp với thế mạnh hiện có (ví dụ: Phát triển Web, Lập trình Di động, Quản trị Mạng, An toàn thông tin, Data/AI).\n"
                "4. Lời khuyên động viên mang phong cách thầy cô HITC gửi gắm đến sinh viên."
            ),
            expected_output="Bản kế hoạch hành động và tư vấn hướng nghiệp định dạng Markdown thân thiện, rõ ràng, mang tính động viên cao.",
            agent=advisor
        )

        # Khởi tạo Crew
        academic_crew = Crew(
            agents=[analyst, advisor],
            tasks=[task_analysis, task_advisory],
            process=Process.sequential,
            verbose=False
        )

        result = academic_crew.kickoff()
        output_str = str(result.raw if hasattr(result, "raw") else result)

        return {
            "success": True,
            "output": output_str,
            "mode": "crewai"
        }

    except Exception as e:
        # Nếu lỗi khi gọi online LLM, tự động fallback sang chế độ nội bộ
        smart_output = generate_smart_academic_advice(
            student_name, student_id, student_class, records_df, gpa, academic_rank
        )
        return {
            "success": True,
            "output": smart_output + f"\n\n*(Lưu ý: Hệ thống đã tự động chuyển sang Chế độ Cố vấn Nội bộ do dịch vụ trực tuyến phản hồi: {str(e)})*",
            "mode": "fallback"
        }
