import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import streamlit as st

# پنهان کردن عنوان پیش‌فرض Streamlit
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
    
    # اطلاعات موسسه
    st.markdown("**جمعی از دانش‌آموختگان شریف**")
    st.markdown("**موسسه آموزشی المان**")
    st.markdown("برای کسب اطلاعات بیشتر، به سایت [elemankonkur.com](http://elemankonkur.com) مراجعه کنید.")
    
    # ورودی‌های اولیه در قالب ستون (برای کاهش فضای اشغال‌شده)
    col1, col2 = st.columns(2)
    with col1:
        stream = st.text_input("رشته‌ی دانش‌آموز (ریاضی/تجربی/انسانی): ").strip()
    with col2:
        grade = st.text_input("پایه‌ی تحصیلی دانش‌آموز (دهم/یازدهم/دوازدهم): ").strip()
    
    # تعیین نوع دانش‌آموز
    if grade == "دوازدهم":
        student_type = st.radio("آیا دانش‌آموز کنکوری است یا فقط امتحانات نهایی دارد؟", ("کنکوری", "نهایی"))
    else:
        student_type = "نهایی"
    
    # تعیین دروس بر اساس رشته و پایه (نمونه‌ای از شرط‌ها)
    if stream == "ریاضی" and grade == "دهم":
        main_subjects = ["هندسه", "فیزیک", "شیمی"]
    elif stream == "ریاضی" and grade == "یازدهم":
        main_subjects = ["حسابان", "آمار و احتمال", "هندسه", "فیزیک", "شیمی"]
    elif stream == "ریاضی" and grade == "دوازدهم":
        main_subjects = ["گسسته", "حسابان", "هندسه", "فیزیک", "شیمی"]
        if student_type == "کنکوری":
            main_subjects += ["حسابان (یازدهم)", "آمار و احتمال (یازدهم)", "هندسه (یازدهم)",
                              "فیزیک (یازدهم)", "شیمی (یازدهم)",
                              "هندسه (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
    elif stream == "تجربی" and grade in ["دهم", "یازدهم", "دوازدهم"]:
        main_subjects = ["زیست", "شیمی", "ریاضی", "فیزیک"]
        if student_type == "کنکوری":
            main_subjects += ["زیست (یازدهم)", "ریاضی (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)",
                              "زیست (دهم)", "ریاضی (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
    elif stream == "انسانی" and grade in ["دهم", "یازدهم", "دوازدهم"]:
        main_subjects = ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
        if student_type == "کنکوری":
            main_subjects += ["فارسی (یازدهم)", "عربی (یازدهم)", "دین و زندگی (یازدهم)", "زبان انگلیسی (یازدهم)",
                              "فارسی (دهم)", "عربی (دهم)", "دین و زندگی (دهم)", "زبان انگلیسی (دهم)"]
    else:
        st.error("⚠️ رشته وارد شده صحیح نیست!")
        return
    
    # استفاده از فرم برای ورودی‌های ساعت مطالعه (کاهش فضای اشغال‌شده)
    with st.form("study_hours_form"):
        total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت): ", min_value=1, step=1)
        st.write("لطفاً تخصیص ساعت مطالعه برای هر درس را مشخص کنید (جمع ساعات باید برابر با کل ساعت باشد):")
        subject_hours = {}
        remaining_hours = total_weekly_hours
        
        # حلقه بر روی دروس با استفاده از ستون‌ها برای نمایش نام درس و ورودی ساعت در یک ردیف
        for subject in main_subjects:
            colA, colB = st.columns([2, 1])
            with colA:
                st.write(subject)
            with colB:
                hours = st.number_input(f"ساعت", min_value=0, max_value=remaining_hours, step=1, key=subject)
            subject_hours[subject] = hours
            remaining_hours -= hours
            st.write(f"ساعات باقی‌مانده: {remaining_hours}")
            
        submitted = st.form_submit_button("ثبت برنامه")
    
    if not submitted:
        st.info("لطفاً اطلاعات را وارد کرده و دکمه ثبت را فشار دهید.")
        return
    
    if remaining_hours > 0:
        st.warning(f"⚠️ {remaining_hours} ساعت باقی‌مانده و تخصیص نیافته است!")
    
    # ایجاد برنامه هفتگی با بازه‌های 1.5 ساعته
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    schedule = {day: [] for day in days}
    
    for subject, hours in subject_hours.items():
        total_slots = hours * 2 // 3  # هر اسلات 1.5 ساعته
        extra_slots = total_slots % len(days)
        daily_slots = total_slots // len(days)
        
        for i, day in enumerate(days):
            slots = daily_slots + (1 if i < extra_slots else 0)
            schedule[day].append({"name": subject, "slots": slots})
    
    # نمایش جدول برنامه در Streamlit
    st.subheader("برنامه‌ی هفتگی شما:")
    table_data = []
    for day, tasks in schedule.items():
        row = [day]
        for task in tasks:
            row.append(f"{task['name']}: {task['slots'] * 1.5:.1f} ساعت")
        table_data.append(row)
    
    # ساخت DataFrame برای نمایش جدول
    # (ستون‌های جدول بر اساس آخرین لیست tasks تعیین شده‌اند)
    df = pd.DataFrame(table_data, columns=["روز"] + [task['name'] for task in tasks])
    st.table(df)
    
    # ذخیره جدول به صورت تصویر
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    table_plot = plt.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center',
                           cellLoc='center', colColours=["#f5f5f5"] * len(df.columns))
    filename = f"schedule_{stream}_{grade}_{student_type}.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    
    # دکمه دانلود تصویر
    with open(filename, "rb") as file:
        st.download_button(label="دانلود جدول به صورت تصویر", data=file, file_name=filename, mime="image/png")

# اجرای برنامه
generate_schedule()
