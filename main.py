import streamlit as st
import pandas as pd
from fpdf import FPDF  # برای ایجاد PDF

def generate_schedule():
    st.title("برنامه‌ریزی هفتگی برای دانش‌آموزان")
    
    # رشته و پایه
    stream = st.selectbox("رشته‌ی دانش‌آموز", ["ریاضی", "تجربی"])
    grade = st.selectbox("پایه‌ی تحصیلی", ["دهم", "یازدهم", "دوازدهم"])
    
    # نوع دانش‌آموز
    student_type = st.selectbox("نوع دانش‌آموز", ["نهایی", "کنکوری"]) if grade == "دوازدهم" else "نهایی"
    
    # تعیین دروس
    main_subjects = ["ریاضی", "فیزیک", "شیمی"] if stream == "ریاضی" else ["زیست", "شیمی", "ریاضی", "فیزیک"]
    
    # دروس اضافی برای کنکوری‌ها
    if student_type == "کنکوری" and grade == "دوازدهم":
        main_subjects += [f"{sub} (یازدهم)" for sub in main_subjects] + [f"{sub} (دهم)" for sub in main_subjects]
    
    total_weekly_hours = st.number_input("کل ساعت مطالعه هفتگی (ساعت)", min_value=1, value=20)
    
    # تخصیص ساعت‌ها
    subject_hours = {}
    remaining_hours = total_weekly_hours
    for subject in main_subjects:
        hours = st.number_input(f"چند ساعت برای {subject} اختصاص می‌دهید؟", min_value=0, max_value=remaining_hours, value=remaining_hours // len(main_subjects))
        subject_hours[subject] = hours
        remaining_hours -= hours
    
    # ساخت برنامه هفتگی
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    schedule = {day: [] for day in days}
    
    # توزیع دروس به روزها
    for subject, hours in subject_hours.items():
        daily_slots = hours // len(days)  # تقسیم منصفانه ساعات به روزها
        remaining_slots = hours % len(days)
        
        for i, day in enumerate(days):
            slots = daily_slots + (1 if i < remaining_slots else 0)
            schedule[day].append({"name": subject, "slots": slots})
    
    # نمایش برنامه
    st.write("برنامه هفتگی شما:")
    for day, tasks in schedule.items():
        st.write(f"**{day}:**")
        for task in tasks:
            st.write(f"- {task['name']}: {task['slots']} ساعت")
    
    # ذخیره به اکسل
    st.write("برنامه خود را به صورت فایل اکسل یا PDF دانلود کنید:")
    
    # ذخیره به اکسل
    if st.button("ذخیره برنامه به فایل اکسل"):
        df = pd.DataFrame(schedule)
        df = df.transpose()  # تبدیل جدول به حالت مناسب برای دانلود
        df.to_excel("schedule.xlsx", index=False)
        
        # برای اینکه در Streamlit فایل دانلود شود:
        with open("schedule.xlsx", "rb") as f:
            st.download_button("دانلود برنامه به صورت اکسل", f, file_name="schedule.xlsx")
    
    # ذخیره به PDF
    if st.button("ذخیره برنامه به فایل PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # عنوان برنامه
        pdf.cell(200, 10, txt="برنامه هفتگی شما:", ln=True, align="C")
        
        # افزودن اطلاعات برنامه
        for day, tasks in schedule.items():
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"{day}:", ln=True)
            for task in tasks:
                pdf.cell(200, 10, txt=f"- {task['name']}: {task['slots']} ساعت", ln=True)
        
        # ذخیره PDF
        pdf.output("schedule.pdf")
        
        # دانلود PDF
        with open("schedule.pdf", "rb") as f:
            st.download_button("دانلود برنامه به صورت PDF", f, file_name="schedule.pdf")

# اجرای اپلیکیشن
generate_schedule()
