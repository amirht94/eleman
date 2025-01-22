import streamlit as st
import pandas as pd

def generate_schedule():
    st.title("برنامه‌ریزی هفتگی برای دانش‌آموزان")
    
    # رشته و پایه
    stream = st.selectbox("رشته‌ی دانش‌آموز", ["ریاضی", "تجربی"])
    grade = st.selectbox("پایه‌ی تحصیلی", ["دهم", "یازدهم", "دوازدهم"])
    
    # نوع دانش‌آموز
    student_type = st.selectbox("نوع دانش‌آموز", ["نهایی", "کنکوری"]) if grade == "دوازدهم" else "نهایی"
    
    # تعیین دروس
    main_subjects = ["ریاضی", "فیزیک", "شیمی"] if stream == "ریاضی" else ["زیست", "شیمی", "ریاضی", "فیزیک"]
    
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
        daily_slots = hours * 2 // 3
        for i, day in enumerate(days):
            schedule[day].append({"name": subject, "slots": daily_slots})
    
    # نمایش برنامه
    st.write("برنامه هفتگی شما:")
    for day, tasks in schedule.items():
        st.write(f"**{day}:**")
        for task in tasks:
            st.write(f"- {task['name']}: {task['slots']} ساعت")
    
    # ذخیره به اکسل
    if st.button("ذخیره برنامه به فایل اکسل"):
        df = pd.DataFrame(schedule)
        df.to_excel("schedule.xlsx")
        st.success("برنامه با موفقیت ذخیره شد!")

# اجرای اپلیکیشن
generate_schedule()
