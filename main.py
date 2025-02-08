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
    
    # اضافه کردن اطلاعات درباره موسسه
    st.markdown("**جمعی از دانش‌آموختگان شریف**")
    st.markdown("**موسسه آموزشی المان**")
    
    # نمایش لینک به سایت elemankonkur.com
    st.markdown("برای کسب اطلاعات بیشتر، به سایت [elemankonkur.com](http://elemankonkur.com) مراجعه کنید.")
    
    # تعیین رشته و پایه
    stream = st.text_input("رشته‌ی دانش‌آموز (ریاضی/تجربی/انسانی): ").strip()
    grade = st.text_input("پایه‌ی تحصیلی دانش‌آموز (دهم/یازدهم/دوازدهم): ").strip()
    
    # تعیین نوع دانش‌آموز (کنکوری/نهایی)
    student_type = ""
    if grade == "دوازدهم":
        student_type = st.radio("آیا دانش‌آموز کنکوری است یا فقط امتحانات نهایی دارد؟", ("کنکوری", "نهایی"))
    else:
        student_type = "نهایی"  # برای دانش‌آموزان دهم و یازدهم
    
    # تعیین دروس بر اساس رشته و نوع دانش‌آموز
    if stream == "ریاضی" and grade == "دهم":
        main_subjects = ["هندسه", "فیزیک", "شیمی"]
    elif stream == "ریاضی" and grade == "یازدهم":
        main_subjects = ["حسابان", "آمار و احتمال", "هندسه", "فیزیک", "شیمی"]     
    elif stream == "ریاضی" and grade == "دوازدهم":
        main_subjects = ["گسسته", "حسابان", "هندسه", "فیزیک", "شیمی"]
        if student_type == "کنکوری":
            main_subjects += ["حسابان (یازدهم)", "آمار و احتمال (یازدهم)", "هندسه (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)"] + ["هندسه (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
    elif stream == "تجربی" and (grade == "دهم" or grade == "یازدهم" or grade == "دوازدهم"):
        main_subjects = ["زیست", "شیمی", "ریاضی", "فیزیک"]  
        if student_type == "کنکوری":
            main_subjects += ["زیست (یازدهم)", "ریاضی (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)"] + ["زیست (دهم)", "ریاضی (دهم)", "فیزیک (دهم)", "شیمی (دهم)"] 
    elif stream == "انسانی" and (grade == "دهم" or grade == "یازدهم" or grade == "دوازدهم"):  
        main_subjects = ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
        if student_type == "کنکوری":
            main_subjects += ["فارسی (یازدهم)", "عربی (یازدهم)", "دین و زندگی (یازدهم)", "زبان انگلیسی (یازدهم)"] + ["فارسی (دهم)", "عربی (دهم)", "دین و زندگی (دهم)", "زبان انگلیسی (دهم)"]  
    else:
        st.error("⚠️ رشته وارد شده صحیح نیست!")
        return

    # اولویت‌بندی دروس
    st.subheader("اولویت‌بندی دروس")
    subject_priority = {}
    for subject in main_subjects:
        priority = st.selectbox(f"اولویت درس {subject} را انتخاب کنید:", ["بالا", "متوسط", "پایین"])
        subject_priority[subject] = priority

    # تخصیص ساعات مطالعه هفتگی به هر درس
    total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت): ", min_value=1, step=1)
    subject_hours = {}
    remaining_hours = total_weekly_hours
    
    for subject in main_subjects:
        hours = st.number_input(f"چند ساعت از {total_weekly_hours} ساعت را برای {subject} اختصاص می‌دهید؟", min_value=0, max_value=remaining_hours, step=1)
        subject_hours[subject] = hours
        remaining_hours -= hours
    
    if remaining_hours > 0:
        st.warning(f"⚠️ {remaining_hours} ساعت باقی‌مانده و تخصیص نیافته است!")
    
    # تنظیم محدودیت‌های روزانه
    st.subheader("محدودیت‌های روزانه")
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    max_daily_hours = {}
    for day in days:
        max_daily_hours[day] = st.number_input(f"حداکثر ساعت مطالعه برای {day}:", min_value=1, max_value=24, step=1)

    # ایجاد برنامه‌ی هفتگی با توزیع متعادل
    schedule = {day: [] for day in days}
    for subject, hours in subject_hours.items():
        total_slots = hours * 2 // 3
        for i in range(total_slots):
            day = days[i % len(days)]
            if sum(task['slots'] for task in schedule[day]) < max_daily_hours[day] * 2 // 3:
                schedule[day].append({"name": subject, "slots": 1})

    # نمایش جدول در Streamlit
    st.subheader("برنامه‌ی هفتگی شما:")
    table_data = []

    for day, tasks in schedule.items():
        row = [day]
        for task in tasks:
            row.append(f"{task['name']}: {task['slots'] * 1.5:.1f} ساعت")
        table_data.append(row)
    
    df = pd.DataFrame(table_data, columns=["روز"] + [task['name'] for task in tasks])
    st.table(df)

    # ذخیره تصویر جدول
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    table = plt.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellLoc='center', colColours=["#f5f5f5"] * len(df.columns))
    
    filename = f"schedule_{stream}_{grade}_{student_type}.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.05)
    plt.close()

    # ایجاد دکمه دانلود
    with open(filename, "rb") as file:
        st.download_button(label="دانلود جدول به صورت تصویر", data=file, file_name=filename, mime="image/png")

# اجرای برنامه
generate_schedule()
