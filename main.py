import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import streamlit as st


def generate_schedule():
    st.title("برنامه‌ریزی هفتگی برای دانش‌آموزان")
    
    # تعیین رشته و پایه
    stream = st.selectbox("رشته‌ی دانش‌آموز", ["ریاضی", "تجربی", "انسانی"])
    grade = st.selectbox("پایه‌ی تحصیلی دانش‌آموز", ["دهم", "یازدهم", "دوازدهم"])
    
    # تعیین نوع دانش‌آموز (کنکوری/نهایی)
    if grade == "دوازدهم":
        student_type = st.selectbox("آیا دانش‌آموز کنکوری است یا فقط امتحانات نهایی دارد؟", ["کنکوری", "نهایی"])
    else:
        student_type = "نهایی"  # برای دانش‌آموزان دهم و یازدهم
    
    # تعیین دروس بر اساس رشته و نوع دانش‌آموز
    if stream == "ریاضی":
        main_subjects = ["حسابان", "گسسته", "فیزیک", "شیمی"]
    elif stream == "تجربی":
        main_subjects = ["زیست", "شیمی", "ریاضی", "فیزیک"]
    elif stream == "انسانی":
        main_subjects = ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
    else:
        st.error("⚠️ رشته وارد شده صحیح نیست!")
        return
    
    # دروس اضافی برای کنکوری‌ها
    if grade == "دوازدهم" and student_type == "کنکوری":
        additional_subjects = [f"{sub} (یازدهم)" for sub in main_subjects] + [f"{sub} (دهم)" for sub in main_subjects]
    else:
        additional_subjects = []
    
    subjects = main_subjects + additional_subjects

    # تخصیص ساعات مطالعه هفتگی به هر درس
    total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت)", min_value=1, step=1)
    subject_hours = {}
    remaining_hours = total_weekly_hours
    
    for subject in subjects:
        hours = st.number_input(f"چند ساعت از {total_weekly_hours} ساعت را برای {subject} اختصاص می‌دهید؟ (حداکثر {remaining_hours})", min_value=0, max_value=remaining_hours)
        if hours > remaining_hours:
            st.warning(f"⚠️ نمی‌توانید بیش از {remaining_hours} ساعت اختصاص دهید!")
            hours = remaining_hours
        subject_hours[subject] = hours
        remaining_hours -= hours
    
    if remaining_hours > 0:
        st.warning(f"⚠️ {remaining_hours} ساعت باقی‌مانده و تخصیص نیافته است!")
    
    # ایجاد برنامه‌ی هفتگی با بازه‌های 1.5 ساعته
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]  # جمعه حذف شد
    schedule = {day: [] for day in days}
    
    for subject, hours in subject_hours.items():
        total_slots = hours * 2 // 3  # تعداد بازه‌های 1.5 ساعته
        extra_slots = total_slots % len(days)  # اضافه برای توزیع در روزها
        daily_slots = total_slots // len(days)
        
        for i, day in enumerate(days):
            slots = daily_slots + (1 if i < extra_slots else 0)
            schedule[day].append({"name": subject, "slots": slots})
    
    # محاسبه میانگین مطالعه روزانه
    avg_daily_hours = total_weekly_hours / len(days)
    
    # نمایش برنامه
    st.subheader("برنامه‌ی هفتگی شما:")
    for day, tasks in schedule.items():
        st.write(f"**{day}:**")
        for task in tasks:
            st.write(f"- {task['name']}: {task['slots'] * 1.5:.1f} ساعت ({task['slots']} بازه‌ی 1.5 ساعته)")
    st.write(f"\nمیانگین ساعت مطالعه روزانه: {avg_daily_hours:.2f} ساعت")
    
    # ایجاد DataFrame با روزها به عنوان ردیف‌ها و دروس به عنوان ستون‌ها
    df = pd.DataFrame(index=days + ['جمعه'])  # جمعه به عنوان ردیف در اکسل اضافه می‌شود
    
    for subject in subjects:
        df[subject] = 0  # مقداردهی اولیه ستون‌ها به صفر
    
    for day, tasks in schedule.items():
        for task in tasks:
            df.at[day, task['name']] = task['slots'] * 1.5  # مقداردهی به سلول‌ها با ساعت مطالعه
    
    # اضافه کردن جمعه با مقدار صفر
    for subject in subjects:
        df.at['جمعه', subject] = 0
    
    # حذف ستون‌هایی که مقدار صفر دارند
    df = df.loc[:, (df != 0).any(axis=0)]
    
    # ذخیره تصویر جدول
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    

    
    # ذخیره تصویر جدول به عنوان فایل PNG
    filename = f"schedule_{stream}_{grade}_{student_type}.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.05)
    plt.close()

    # نمایش تصویر جدول در Streamlit
    st.image(filename)
    st.success(f"✅ برنامه با موفقیت در فایل {filename} ذخیره شد!")

# اجرای برنامه
generate_schedule()
