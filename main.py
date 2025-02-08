from ast import main
from numpy import add
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import streamlit as st

# مخفی کردن عنوان و متن پیش‌فرض استریم‌لیت
st.markdown("""
    <style>
        .css-1v3fvcr {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# تنظیم فونت برای پشتیبانی از فارسی
rcParams['font.family'] = 'B Nazanin'  # یا 'Vazir'

def generate_schedule():
    st.title("برنامه‌ریزی هفتگی برای دانش‌آموزان")
    
    st.markdown("**جمعی از دانش‌آموختگان شریف**")
    st.markdown("**موسسه آموزشی المان**")
    
    st.markdown("برای کسب اطلاعات بیشتر، به سایت [elemankonkur.com](http://elemankonkur.com) مراجعه کنید.")
    
    stream = st.text_input("رشته‌ی دانش‌آموز (ریاضی/تجربی/انسانی): ").strip()
    grade = st.text_input("پایه‌ی تحصیلی دانش‌آموز (دهم/یازدهم/دوازدهم): ").strip()
    
    student_type = ""
    if grade == "دوازدهم":
        student_type = st.radio("آیا دانش‌آموز کنکوری است یا فقط امتحانات نهایی دارد؟", ("کنکوری", "نهایی"))
    else:
        student_type = "نهایی"
    
    subjects = {
        "ریاضی": {"دهم": ["هندسه", "فیزیک", "شیمی"], "یازدهم": ["حسابان", "آمار و احتمال", "هندسه", "فیزیک", "شیمی"], "دوازدهم": ["گسسته", "حسابان", "هندسه", "فیزیک", "شیمی"]},
        "تجربی": {"دهم": ["زیست", "شیمی", "ریاضی", "فیزیک"], "یازدهم": ["زیست", "شیمی", "ریاضی", "فیزیک"], "دوازدهم": ["زیست", "شیمی", "ریاضی", "فیزیک"]},
        "انسانی": {"دهم": ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"], "یازدهم": ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"], "دوازدهم": ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]}
    }
    
    if stream in subjects and grade in subjects[stream]:
        main_subjects = subjects[stream][grade]
        if student_type == "کنکوری" and grade == "دوازدهم":
            main_subjects += [f"{s} ({y})" for y in ["دهم", "یازدهم"] for s in subjects[stream][y]]
    else:
        st.error("⚠️ رشته یا پایه وارد شده صحیح نیست!")
        return

    st.subheader("اولویت‌بندی دروس")
    subject_priority = {s: st.selectbox(f"اولویت درس {s}:", ["بالا", "متوسط", "پایین"]) for s in main_subjects}
    
    total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت):", min_value=1, step=1)
    subject_hours = {}
    remaining_hours = total_weekly_hours
    
    for subject in main_subjects:
        max_hours = remaining_hours if remaining_hours > 0 else 0
        hours = st.number_input(f"ساعات مطالعه برای {subject}:", min_value=0, max_value=max_hours, step=1)
        subject_hours[subject] = hours
        remaining_hours -= hours
    
    if remaining_hours > 0:
        st.warning(f"⚠️ {remaining_hours} ساعت باقی‌مانده و تخصیص نیافته است!")
    
    st.subheader("محدودیت‌های روزانه")
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    max_daily_hours = {d: st.number_input(f"حداکثر ساعت مطالعه برای {d}:", min_value=1, max_value=24, step=1) for d in days}
    
    schedule = {d: [] for d in days}
    for subject, hours in subject_hours.items():
        for i in range(hours):
            day = days[i % len(days)]
            if sum(t[1] for t in schedule[day]) < max_daily_hours[day]:
                schedule[day].append((subject, 1))
    
    st.subheader("برنامه‌ی هفتگی شما:")
    table_data = [[d] + [f"{s[0]}: {s[1]} ساعت" for s in tasks] for d, tasks in schedule.items()]
    
    if any(table_data):
        columns = ["روز"] + list(set(s[0] for day in schedule.values() for s in day))
        df = pd.DataFrame(table_data, columns=columns)
        st.table(df)
        
        plt.figure(figsize=(10, 6))
        plt.axis('off')
        plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=["#f5f5f5"] * len(df.columns))
        filename = f"schedule_{stream}_{grade}_{student_type}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.05)
        plt.close()
        
        with open(filename, "rb") as file:
            st.download_button(label="دانلود جدول به صورت تصویر", data=file, file_name=filename, mime="image/png")
    else:
        st.error("⚠️ برنامه‌ی هفتگی خالی است. لطفاً ساعات را به درستی وارد کنید.")

generate_schedule()
