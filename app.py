import streamlit as st
import pandas as pd
import datetime
import altair as alt

from grade_calculator import calculate_subject_grades, get_academic_rank


# Khởi tạo trạng thái hệ thống nếu chưa có
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_info" not in st.session_state:
    st.session_state.student_info = {}

# Cấu hình trang Web mặc định
st.set_page_config(
    page_title="Cổng Thông Tin Sinh Viên - HITC TP.HCM Portal", 
    page_icon="🎓", 
    layout="centered"
)

# =========================================================================
# PHẦN 1: CẤU HÌNH THEME DARK MODE & COLOR ĐẶC TRƯNG HITC TP.HCM
# =========================================================================
# Cho người dùng lựa chọn chế độ màu sắc ở Sidebar bên trái
theme_choice = st.sidebar.selectbox("🎨 Chế độ hiển thị màn hình", ["Giao diện Sáng (Light)", "Giao diện Tối (Dark Mode)"])

# Thiết lập hệ màu dựa trên lựa chọn (Đỏ đô chủ đạo của Cao đẳng Công thương TP.HCM)
if theme_choice == "Giao diện Tối (Dark Mode)":
    bg_color = "#121212"      
    text_color = "#FFFFFF"    
    card_bg = "#1E1E1E"       
    border_color = "#333333"  
else:
    bg_color = "#FFFFFF"      
    text_color = "#333333"    
    card_bg = "#F8F9FA"       
    border_color = "#E0E0E0"  

# Bơm CSS động thay đổi giao diện theo thương hiệu HITC TP.HCM
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    h1, h2, h3, h4, h5, h6, label, p, span {{
        color: {text_color} !important;
    }}
    
    /* Thiết kế phần HEADER rực rỡ mang bản sắc HITC TP.HCM (Đỏ đô sang trọng) */
    .hitc-header {{
        background: linear-gradient(135deg, #A31D1D 70%, #E8B86D 100%); /* Tông màu đỏ - vàng đặc trưng của trường */
        padding: 22px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }}
    .hitc-header h1 {{
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: bold !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }}
    .hitc-header p {{
        color: #F5E7B2 !important;
        font-size: 15px !important;
        margin: 5px 0 0 0 !important;
        font-style: italic;
    }}
    
    /* Các nút bấm theo tông đỏ đô thương hiệu */
    .stButton>button {{
        background-color: #A31D1D !important;
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
    }}
    .stButton>button:hover {{
        background-color: #E8B86D !important;
        color: #A31D1D !important;
        box-shadow: 0 4px 10px rgba(232, 184, 109, 0.4) !important;
    }}
    
    /* Khối Form đăng nhập bo tròn */
    div[data-testid="stForm"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px !important;
        padding: 25px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05) !important;
    }}
    
    /* Thiết kế phần FOOTER chuẩn HITC TP.HCM */
    .hitc-footer {{
        margin-top: 50px;
        padding: 15px;
        background-color: {card_bg};
        border-top: 3px solid #A31D1D;
        border-radius: 5px;
        text-align: center;
        font-size: 13px;
        color: {text_color};
    }}
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# GIAO DIỆN CHÍNH HÀNH TRÌNH ĐĂNG NHẬP & PORTAL
# =========================================================================

# 1. HIỂN THỊ TRANG TRÍ HEADER CHUNG TRÊN ĐẦU TRANG
st.markdown("""
    <div class="hitc-header">
        <h1>🏫 TRƯỜNG CAO ĐẲNG CÔNG THƯƠNG THÀNH PHỐ HỒ CHÍ MINH</h1>
        <p>Hệ Thống Cổng Thông Tin & Quản Lý Tiến Độ Học Tập Sinh Viên (HITC Portal)</p>
    </div>
""", unsafe_allow_html=True)

# 2. KIỂM TRA ĐIỀU KIỆN HIỂN THỊ TRANG ĐĂNG NHẬP HOẶC TRANG TRONG
if not st.session_state.logged_in:
    st.subheader("🔑 Đăng nhập tài khoản sinh viên")
    
    with st.form(key="login_form"):
        ho_ten = st.text_input("Họ và tên sinh viên:", placeholder="Ví dụ: Nguyễn Tấn Dũng")
        mssv = st.text_input("Mã số sinh viên (MSSV):", placeholder="Ví dụ: 2125.... (8 chữ số)")
        lop_hoc = st.text_input("Lớp học khóa học:", placeholder="Ví dụ: CCQ2511B")
        
        btn_login = st.form_submit_button("🔓 Đăng nhập vào hệ thống")
        
    if btn_login:
        if ho_ten.strip() == "" or mssv.strip() == "" or lop_hoc.strip() == "":
            st.error("❌ Vui lòng điền đầy đủ thông tin để hệ thống xác thực dữ liệu!")
        else:
            st.session_state.student_info = {"name": ho_ten.strip(), "id": mssv.strip(), "class": lop_hoc.strip()}
            st.session_state.logged_in = True
            st.success("Đăng nhập thành công vào HITC Portal!")
            st.rerun()

else:
    sv = st.session_state.student_info

    # THANH SIDEBAR HIỂN THỊ THÔNG TIN SINH VIÊN ĐỘNG
    st.sidebar.markdown("### 👤 THÔNG TIN SINH VIÊN")
    st.sidebar.info(f"""
    **Họ và tên:** {sv['name']}  
    **Mã số SV:** {sv['id']}  
    **Lớp học:** {sv['class']}  
    **Khóa học:** Khóa 49 / 50 (Chính Quy)  
    **Cơ sở:** 20 Tăng Nhơn Phú, Thủ Đức  
    **Trạng thái:** Đang học tích cực
    """)
    
    if st.sidebar.button("🔒 Đăng xuất khỏi hệ thống"):
        st.session_state.logged_in = False
        st.session_state.student_info = {}
        st.rerun()

    if "academic_records" not in st.session_state:
        st.session_state.academic_records = pd.DataFrame(columns=["Ngày nhập", "Học kỳ", "Môn học", "Điểm số", "Loại điểm"])

    # FORM NHẬP ĐIỂM
    st.header("📥 Cập nhật kết quả điểm số mới")
    with st.form(key="study_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Ngày đánh giá", datetime.date.today())
            semester = st.selectbox("Học kỳ đánh giá", [
                "Học kỳ I", "Học kỳ II", "Học kỳ III", "Học kỳ IV", "Học kỳ V", "Học kỳ VI", "Học kỳ Phụ / Cải thiện"
            ])
            subject = st.selectbox("Môn học (Chương trình đào tạo Khoa CNTT - HITC)", [
                # --- 1. Khối Kiến thức Đại cương & Kỹ năng ---
                "Triết học Mác - Lênin",
                "Tư tưởng Hồ Chí Minh",
                "Pháp luật đại cương",
                "Tin học đại cương",
                "Tiếng Anh cơ bản 1",
                "Tiếng Anh cơ bản 2",
                "Tiếng Anh chuyên ngành CNTT",
                "Kỹ năng mềm & Làm việc nhóm",
                "Giáo dục thể chất",
                "Giáo dục quốc phòng - An ninh",
                
                # --- 2. Khối Cơ sở ngành CNTT ---
                "Toán ứng dụng CNTT (Toán rời rạc)",
                "Nhập môn lập trình (C/C++)",
                "Kỹ thuật lập trình (C/C++)",
                "Kiến trúc máy tính & Vi xử lý",
                "Hệ điều hành (Windows & Linux)",
                "Lắp ráp, cài đặt & Bảo trì máy tính",
                "Mạng máy tính cơ bản",
                "Quản trị mạng máy tính (CCNA)",
                "Cơ sở dữ liệu (SQL Server)",
                "Hệ quản trị CSDL MySQL",
                "Cấu trúc dữ liệu và Giải thuật",
                "Thiết kế đồ họa đa phương tiện (Photoshop / AI)",
                
                # --- 3. Khối Chuyên ngành Lập trình & Kỹ thuật Phần mềm ---
                "Ngôn ngữ lập trình Python",
                "Lập trình hướng đối tượng (OOP Java / C#)",
                "Lập trình Windows Forms & .NET Core",
                "Phân tích & Thiết kế hệ thống thông tin",
                "Thiết kế Web căn bản (HTML5/CSS3/JavaScript)",
                "Lập trình Web Frontend (ReactJS / VueJS)",
                "Lập trình Web Backend (PHP & Laravel / NodeJS)",
                "Lập trình Web ASP.NET Core MVC / Web API",
                "Thiết kế trải nghiệm & Giao diện UI/UX (Figma)",
                "Lập trình ứng dụng Di động (Android / Kotlin)",
                "Lập trình ứng dụng Di động đa nền tảng (Flutter)",
                "Kiểm thử và Đảm bảo chất lượng phần mềm (QA/QC)",
                
                # --- 4. Khối Chuyên ngành Mạng & An toàn thông tin ---
                "An toàn & Bảo mật thông tin mạng",
                "Quản trị máy chủ Linux & Windows Server",
                "Điện toán đám mây & DevOps căn bản (Docker/AWS)",
                "Trí tuệ nhân tạo (AI) & Học máy (Machine Learning)",
                "Khai phá dữ liệu & Phân tích dữ liệu lớn",
                
                # --- 5. Khối Thực tập & Khóa luận Tốt nghiệp ---
                "Chuyên đề công nghệ mới",
                "Thực tập tốt nghiệp tại doanh nghiệp",
                "Đồ án chuyên ngành CNTT",
                "Đồ án / Khóa luận tốt nghiệp",
                
                # --- 6. Tùy chọn mở rộng ---
                "📌 [Môn học khác - Nhập tên bên dưới]"
            ])
            if subject == "📌 [Môn học khác - Nhập tên bên dưới]":
                custom_subject = st.text_input("Nhập tên môn học khác:", placeholder="Ví dụ: Lập trình Game Unity, Lập trình iOS...")
            else:
                custom_subject = ""
        with col2:
            score = st.number_input("Điểm số thành phần", min_value=0.0, max_value=10.0, step=0.5, value=7.0)
            grade_type = st.selectbox("Loại điểm đánh giá", ["Điểm chuyên cần (10%)", "Điểm kiểm tra giữa kỳ (30%)", "Điểm thi kết thúc học phần (60%)"])
            
        submit_button = st.form_submit_button(label="🚀 Cập nhật kết quả")

    if submit_button:
        # Xác định tên môn học cuối cùng
        if subject == "📌 [Môn học khác - Nhập tên bên dưới]":
            if custom_subject.strip() == "":
                st.error("❌ Vui lòng nhập tên môn học vào ô bên dưới khi chọn tùy chọn 'Môn học khác'!")
                final_subject = None
            else:
                final_subject = custom_subject.strip()
        else:
            final_subject = subject

        if final_subject:
            new_data = pd.DataFrame([{"Ngày nhập": date.strftime("%Y-%m-%d"), "Học kỳ": semester, "Môn học": final_subject, "Điểm số": float(score), "Loại điểm": grade_type}])
            st.session_state.academic_records = pd.concat([st.session_state.academic_records, new_data], ignore_index=True)
            st.success(f"Hệ thống HITC Portal đã đồng bộ điểm số môn '{final_subject}' thành công!")

    # HIỂN THỊ KẾT QUẢ TRA CỨU
    st.divider()
    st.header("📊 Tra Cứu Kết Quả Học Tập Tích Lũy")
    df = st.session_state.academic_records

    if df.empty:
        st.info("Hiện hệ thống trống dữ liệu. Vui lòng cập nhật điểm số để kích hoạt bảng tra cứu học phần!")
    else:
        # Tính điểm tổng kết từng môn học theo trọng số 10% - 30% - 60%
        subject_summary = calculate_subject_grades(df)
        average_score = float(subject_summary["Điểm tổng kết"].mean()) if not subject_summary.empty else 0.0

        hoc_luc = get_academic_rank(average_score)

        c1, c2, c3 = st.columns(3)
        c1.metric(label="📈 Điểm trung bình tích lũy (GPA)", value=f"{average_score:.2f} / 10")
        c2.metric(label="🎓 Học lực dự kiến", value=hoc_luc)
        c3.metric(label="📚 Tổng số môn học", value=f"{len(subject_summary)} môn ({len(df)} đầu điểm)")
        
        st.subheader("📋 Chi tiết các đầu điểm đã nhập")
        st.dataframe(df, use_container_width=True)

        st.subheader("📑 Bảng tổng kết môn học (theo trọng số CC 10% - GK 30% - CK 60%)")
        st.dataframe(subject_summary, use_container_width=True)

        # Chức năng tải về và quản lý dữ liệu
        col_act1, col_act2 = st.columns([1, 1])
        with col_act1:
            csv_data = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải bảng điểm (CSV)",
                data=csv_data,
                file_name=f"Bang_diem_{sv['id']}_{datetime.date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_act2:
            if st.button("🗑️ Xóa toàn bộ dữ liệu bảng điểm", use_container_width=True):
                st.session_state.academic_records = pd.DataFrame(columns=["Ngày nhập", "Học kỳ", "Môn học", "Điểm số", "Loại điểm"])
                st.rerun()

        # Xóa từng dòng điểm nếu nhập nhầm
        with st.expander("✂️ Xóa một dòng điểm nhập nhầm"):
            row_labels = [f"Dòng {i+1}: [{row['Học kỳ']}] {row['Môn học']} - {row['Loại điểm']}: {row['Điểm số']}đ" for i, row in df.iterrows()]
            del_idx = st.selectbox("Chọn dòng điểm cần xóa:", options=list(range(len(row_labels))), format_func=lambda x: row_labels[x])
            if st.button("Xác nhận xóa dòng này"):
                st.session_state.academic_records = df.drop(index=del_idx).reset_index(drop=True)
                st.success("Đã xóa dòng điểm thành công!")
                st.rerun()
        
        st.subheader("📊 Đồ thị phân bổ năng lực môn học")
        chart = alt.Chart(subject_summary).mark_bar(color="#A31D1D").encode(
            x=alt.X("Môn học:N", axis=alt.Axis(labelAngle=0, labelOverlap=False), title="Môn học"),
            y=alt.Y("Điểm tổng kết:Q", scale=alt.Scale(domain=[0, 10]), title="Điểm tổng kết"),
            tooltip=["Môn học", "Điểm tổng kết", "Số đầu điểm"]
        ).properties(
            width="container",
            height=350
        )
        st.altair_chart(chart, use_container_width=True)

        # =========================================================================
        # PHẦN 4: TRỢ LÝ CỐ VẤN HỌC TẬP THÔNG MINH (HITC ADVISOR & CREWAI)
        # =========================================================================
        st.divider()
        st.header("🤖 Cố Vấn Học Tập & Định Hướng Nghề Nghiệp CNTT")
        st.caption("Hệ thống cung cấp 2 chế độ cố vấn: **Cố vấn Tự động Chuẩn HITC (Không cần API Key)** và **Phi đội AI Đa tác nhân (CrewAI)**.")

        ai_mode = st.radio(
            "Chọn chế độ cố vấn học tập:",
            [
                "⚡ Chế độ Tự động Chuẩn HITC (Không cần API Key - Khuyên dùng để demo)",
                "🌐 Chế độ AI Multi-Agent Trực tuyến (Cần Google Gemini / OpenAI API Key)"
            ],
            index=0
        )

        user_api_key = None
        provider_choice = "gemini"
        model_choice = "gemini-1.5-flash"

        if "Trực tuyến" in ai_mode:
            with st.expander("⚙️ Cấu hình Nhà cung cấp AI & Khóa API", expanded=True):
                st.info("💡 **Bạn chưa có API Key?** Bạn có thể lấy **Google Gemini API Key hoàn toàn MIỄN PHÍ** trong 30 giây bằng tài khoản Gmail tại: [Google AI Studio (aistudio.google.com)](https://aistudio.google.com/app/apikey)")
                ai_col1, ai_col2 = st.columns(2)
                with ai_col1:
                    provider_choice = st.selectbox(
                        "Nhà cung cấp Mô hình:",
                        options=["gemini", "openai"],
                        format_func=lambda x: "Google Gemini (Miễn phí qua AI Studio)" if x == "gemini" else "OpenAI (GPT-4o / GPT-4o-mini)"
                    )
                with ai_col2:
                    if provider_choice == "gemini":
                        model_choice = st.selectbox("Mô hình AI:", ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"])
                    else:
                        model_choice = st.selectbox("Mô hình AI:", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
                
                user_api_key = st.text_input(
                    f"Nhập API Key ({'Google Gemini Key' if provider_choice == 'gemini' else 'OpenAI Key'}):",
                    type="password",
                    help="Khóa API chỉ sử dụng cho phiên hiện tại, không lưu trữ trên máy chủ."
                )

        btn_run_ai = st.button("🚀 Kích hoạt Báo Cáo Tư Vấn Học Tập", type="primary")

        if btn_run_ai:
            from ai_advisor import run_crewai_advisor, generate_smart_academic_advice
            
            if "Không cần API Key" in ai_mode:
                with st.spinner("⏳ Hệ thống đang tổng hợp dữ liệu học phần và đối chiếu quy chế HITC..."):
                    advice_content = generate_smart_academic_advice(
                        student_name=sv["name"],
                        student_id=sv["id"],
                        student_class=sv["class"],
                        records_df=df,
                        gpa=average_score,
                        academic_rank=hoc_luc
                    )
                    st.success("✅ Đã hoàn tất phân tích học lực và lập kế hoạch hành động thành công!")
                    st.markdown("### 📋 Kết Quả Phân Tích & Lộ Trình Đề Xuất:")
                    with st.container(border=True):
                        st.markdown(advice_content)
            else:
                with st.spinner("⏳ Phi đội AI Agents (CrewAI) đang phối hợp phân tích và lập kế hoạch..."):
                    result = run_crewai_advisor(
                        student_name=sv["name"],
                        student_id=sv["id"],
                        student_class=sv["class"],
                        records_df=df,
                        gpa=average_score,
                        academic_rank=hoc_luc,
                        api_key=user_api_key.strip() if user_api_key else None,
                        provider=provider_choice,
                        model_name=model_choice
                    )

                    if result["success"]:
                        st.success("✅ Phi đội AI Cố vấn đã hoàn thành báo cáo tư vấn học tập!")
                        st.markdown("### 📋 Kết Quả Phân Tích & Lộ Trình Đề Xuất:")
                        with st.container(border=True):
                            st.markdown(result['output'])
                    else:
                        st.error(f"❌ {result['error']}")




# 3. TRANG TRÍ FOOTER CHUYÊN NGHIỆP Ở CUỐI TRANG
st.markdown("""
    <div class="hitc-footer">
        <p><b>© 2026 - Bản quyền thuộc về Trung tâm Đào tạo - Trường Cao đẳng Công thương TP.HCM (HITC)</b></p>
        <p>📍 Địa chỉ: Số 20 Tăng Nhơn Phú, P. Phước Long B, TP. Thủ Đức, TP. Hồ Chí Minh</p>
        <p><i>Hệ thống phát triển bởi Sinh viên khoa CNTT HITC - Nguyễn Tấn Dũng</i></p>
    </div>
""", unsafe_allow_html=True)
