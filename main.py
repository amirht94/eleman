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
    
   # تعیین رشته و پایه به صورت لیست انتخابی
    stream_options = ["ریاضی", "تجربی", "انسانی"]
    grade_options = ["دهم", "یازدهم", "دوازدهم"]
    
    stream = st.selectbox("رشته‌ی دانش‌آموز:", stream_options)
    grade = st.selectbox("پایه‌ی تحصیلی دانش‌آموز:", grade_options)
    
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

    # تخصیص ساعات مطالعه هفتگی به هر درس
    
    # استفاده از st.columns برای جمع‌وجور کردن فرم
    st.write("ساعات مطالعه هر درس را وارد کنید:")
    subject_hours = {}
    remaining_hours = total_weekly_hours
    
    # تعداد ستون‌ها (مثلاً ۳ ستون)
    num_columns = 3
    columns = st.columns(num_columns)
    
    for i, subject in enumerate(main_subjects):
        with columns[i % num_columns]:  # توزیع دروس بین ستون‌ها
            hours = st.number_input(
                f"{subject}",
                min_value=0,
                max_value=remaining_hours,
                step=1,
                key=subject  # کلید منحصر به فرد برای هر درس
            )
            subject_hours[subject] = hours
            remaining_hours -= hours
    
    if remaining_hours > 0:
        st.warning(f"⚠️ {remaining_hours} ساعت باقی‌مانده و تخصیص نیافته است!")
    
    # ایجاد برنامه‌ی هفتگی با بازه‌های 1.5 ساعته
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    schedule = {day: [] for day in days}
    
    for subject, hours in subject_hours.items():
        total_slots = hours * 2 // 3
        extra_slots = total_slots % len(days)
        daily_slots = total_slots // len(days)
        
        for i, day in enumerate(days):
            slots = daily_slots + (1 if i < extra_slots else 0)
            schedule[day].append({"name": subject, "slots": slots})
    
    avg_daily_hours = total_weekly_hours / len(days)
    
    # نمایش جدول در Streamlit
    st.subheader("برنامه‌ی هفتگی شما:")
    table_data = []

    for day, tasks in schedule.items():
        row = [day]
        for task in tasks:
            row.append(f"{task['name']}: {task['slots'] * 1.5:.1f} ساعت")
        table_data.append(row)
    
    df = pd.DataFrame(table_data, columns=["روز"] + [task['name'] for task in tasks])
    
    # تنظیمات استایل برای جدول
    styled_df = df.style.set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]},
        {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]},
        {'selector': 'tbody tr:hover', 'props': [('background-color', '#ddd')]}
    ]).set_properties(**{'text-align': 'center'})
    
    st.write(styled_df.to_html(), unsafe_allow_html=True)

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
