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
rcParams['font.family'] = 'B Nazanin'

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
        student_type = "نهایی"
    
    # تعیین دروس بر اساس رشته و نوع دانش‌آموز
    main_subjects = []
    if stream == "ریاضی":
        main_subjects = ["گسسته", "حسابان", "هندسه", "فیزیک", "شیمی"]
        if student_type == "کنکوری":
            main_subjects += ["حسابان (یازدهم)", "آمار و احتمال (یازدهم)", "هندسه (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)", 
                              "هندسه (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
    elif stream == "تجربی":
        main_subjects = ["زیست", "شیمی", "ریاضی", "فیزیک"]
    elif stream == "انسانی":
        main_subjects = ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
    else:
        st.error("⚠️ رشته وارد شده صحیح نیست!")
        return

    # بخش انتخاب دروس با اولویت بالا با استفاده از جدول تیک‌دار (Multiselect)
    st.subheader("انتخاب دروس با اولویت بالا")
    high_priority_subjects = st.multiselect("درس‌هایی که می‌خواهید اولویت بالا داشته باشند را انتخاب کنید:", main_subjects)
    
    st.subheader("دروس با اولویت بالا")
    if high_priority_subjects:
        df_high_priority = pd.DataFrame(high_priority_subjects, columns=["درس‌های با اولویت بالا"])
        st.table(df_high_priority)
    else:
        st.write("هیچ درسی با اولویت بالا انتخاب نشده است.")
    
    # تخصیص ساعات مطالعه هفتگی به هر درس
    total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت): ", min_value=1, step=1)
    subject_hours = {}
    remaining_hours = total_weekly_hours
    
    for subject in main_subjects:
        max_hours = remaining_hours if remaining_hours > 0 else 0
        hours = st.number_input(f"چند ساعت از {total_weekly_hours} ساعت را برای {subject} اختصاص می‌دهید؟", min_value=0, max_value=max_hours, step=1)
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
        for i in range(hours):
            day = days[i % len(days)]
            if sum(task[1] for task in schedule[day]) < max_daily_hours[day]:
                schedule[day].append((subject, 1))
    
    # نمایش جدول برنامه‌ی هفتگی
    st.subheader("برنامه‌ی هفتگی شما:")
    table_data = [[day] + [f"{s[0]}: {s[1]} ساعت" for s in tasks] for day, tasks in schedule.items()]
    
    # تعیین ستون‌ها به صورت دینامیک
    all_subjects_in_schedule = list({s[0] for tasks in schedule.values() for s in tasks})
    columns = ["روز"] + all_subjects_in_schedule
    
    # تطبیق تعداد ستون‌ها در هر سطر
    new_table_data = []
    for row in table_data:
        row_extended = row + [""] * (len(columns) - len(row))
        new_table_data.append(row_extended)
    
    df = pd.DataFrame(new_table_data, columns=columns)
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
