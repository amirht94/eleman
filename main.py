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
            main_subjects += ["حسابان (یازدهم)", "آمار و احتمال (یازدهم)", "هندسه (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)", "هندسه (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
    elif stream == "تجربی":
        main_subjects = ["زیست", "شیمی", "ریاضی", "فیزیک"]
    elif stream == "انسانی":
        main_subjects = ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
    else:
        st.error("⚠️ رشته وارد شده صحیح نیست!")
        return

    # اولویت‌بندی دروس
    st.subheader("اولویت‌بندی دروس")
    high_priority_subjects = []
    for subject in main_subjects:
        priority = st.selectbox(f"اولویت درس {subject} را انتخاب کنید:", ["بالا", "متوسط", "پایین"])
        if priority == "بالا":
            high_priority_subjects.append(subject)
    
    # نمایش جدول فقط برای دروس با اولویت بالا
    st.subheader("دروس با اولویت بالا")
    if high_priority_subjects:
        df_high_priority = pd.DataFrame(high_priority_subjects, columns=["درس‌های با اولویت بالا"])
        st.table(df_high_priority)
    else:
        st.write("هیچ درسی با اولویت بالا انتخاب نشده است.")

# اجرای برنامه
generate_schedule()
