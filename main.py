import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import streamlit as st

# پنهان کردن عنوان و متن پیش‌فرض Streamlit
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
    
    # دریافت ورودی‌های اولیه (رشته و پایه) در قالب ستون‌ها
    col1, col2 = st.columns(2)
    with col1:
        stream = st.text_input("رشته‌ی دانش‌آموز (ریاضی/تجربی/انسانی): ").strip()
    with col2:
        grade = st.text_input("پایه‌ی تحصیلی دانش‌آموز (دهم/یازدهم/دوازدهم): ").strip()
    
    # در صورتی که رشته یا پایه وارد نشده باشد، ادامه اجرا متوقف می‌شود
    if not stream or not grade:
        st.info("لطفاً ابتدا رشته و پایه را وارد کنید.")
        st.stop()
    
    # تعیین نوع دانش‌آموز؛ در صورت پایه دوازدهم، کاربر نوع دانش‌آموز (کنکوری/نهایی) را انتخاب می‌کند
    if grade == "دوازدهم":
        student_type = st.radio("آیا دانش‌آموز کنکوری است یا فقط امتحانات نهایی دارد؟", ("کنکوری", "نهایی"))
    else:
        student_type = "نهایی"
    
    # تعیین دروس بر اساس رشته و پایه
    if stream == "ریاضی":
        if grade == "دهم":
            main_subjects = ["هندسه", "فیزیک", "شیمی"]
        elif grade == "یازدهم":
            main_subjects = ["حسابان", "آمار و احتمال", "هندسه", "فیزیک", "شیمی"]
        elif grade == "دوازدهم":
            main_subjects = ["گسسته", "حسابان", "هندسه", "فیزیک", "شیمی"]
            if student_type == "کنکوری":
                main_subjects += ["حسابان (یازدهم)", "آمار و احتمال (یازدهم)", "هندسه (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)"]
                main_subjects += ["هندسه (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
        else:
            st.error("پایه وارد شده صحیح نیست!")
            st.stop()
    elif stream == "تجربی":
        if grade in ["دهم", "یازدهم", "دوازدهم"]:
            main_subjects = ["زیست", "شیمی", "ریاضی", "فیزیک"]
            if grade == "دوازدهم" and student_type == "کنکوری":
                main_subjects += ["زیست (یازدهم)", "ریاضی (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)"]
                main_subjects += ["زیست (دهم)", "ریاضی (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
        else:
            st.error("پایه وارد شده صحیح نیست!")
            st.stop()
    elif stream == "انسانی":
        if grade in ["دهم", "یازدهم", "دوازدهم"]:
            main_subjects = ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
            if grade == "دوازدهم" and student_type == "کنکوری":
                main_subjects += ["فارسی (یازدهم)", "عربی (یازدهم)", "دین و زندگی (یازدهم)", "زبان انگلیسی (یازدهم)"]
                main_subjects += ["فارسی (دهم)", "عربی (دهم)", "دین و زندگی (دهم)", "زبان انگلیسی (دهم)"]
        else:
            st.error("پایه وارد شده صحیح نیست!")
            st.stop()
    else:
        st.error("رشته وارد شده صحیح نیست!")
        st.stop()
    
    # فرم برای دریافت کل ساعت مطالعه هفتگی و تخصیص ساعت به هر درس
    with st.form("study_hours_form"):
        total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت): ", min_value=1, step=1)
        st.write("لطفاً تخصیص ساعت مطالعه برای هر درس را مشخص کنید:")
        subject_hours = {}
        for subject in main_subjects:
            hours = st.number_input(f"{subject} (ساعت)", min_value=0, step=1, key=subject)
            subject_hours[subject] = hours
        submitted = st.form_submit_button("ثبت برنامه")
    
    if not submitted:
        st.info("لطفاً اطلاعات را وارد کرده و فرم را ارسال کنید.")
        st.stop()
    
    # بررسی تطابق مجموع ساعات تخصیص‌یافته با کل ساعت مطالعه‌ی هفتگی
    total_allocated = sum(subject_hours.values())
    if total_allocated != total_weekly_hours:
        st.error(f"مجموع ساعت‌های تخصیص داده شده ({total_allocated}) با کل ساعت مطالعه‌ی هفتگی ({total_weekly_hours}) برابر نیست. لطفاً مجدداً بررسی کنید.")
        st.stop()
    
    # ایجاد برنامه هفتگی؛ هر اسلات معادل 1.5 ساعت است
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    schedule = {day: [] for day in days}
    
    for subject, hours in subject_hours.items():
        # محاسبه تعداد اسلات به ازای هر درس؛ به صورت تقریبی (ساعات * 2/3)
        total_slots = int(hours * 2 / 3)
        daily_slots = total_slots // len(days)
        extra_slots = total_slots % len(days)
        for i, day in enumerate(days):
            slots = daily_slots + (1 if i < extra_slots else 0)
            schedule[day].append({"name": subject, "slots": slots})
    
    # نمایش برنامه هفتگی در قالب جدول
    st.subheader("برنامه‌ی هفتگی شما:")
    table_data = []
    for day in days:
        row = [day]
        # سطر را بر اساس ترتیب دروس اصلی تکمیل می‌کنیم
        for subject in main_subjects:
            # جستجو برای دریافت اطلاعات تخصیص‌یافته به هر درس در آن روز
            task = next((item for item in schedule[day] if item["name"] == subject), None)
            hours_str = f"{task['slots'] * 1.5:.1f} ساعت" if task else "0 ساعت"
            row.append(hours_str)
        table_data.append(row)
    
    columns = ["روز"] + main_subjects
    df = pd.DataFrame(table_data, columns=columns)
    st.table(df)
    
    # ذخیره جدول به صورت تصویر با استفاده از matplotlib
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    table_plot = plt.table(cellText=df.values, colLabels=df.columns, loc='center',
                           cellLoc='center', colColours=["#f5f5f5"] * len(df.columns))
    filename = f"schedule_{stream}_{grade}_{student_type}.png"
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    
    # دکمه دانلود تصویر
    with open(filename, "rb") as file:
        st.download_button(label="دانلود جدول به صورت تصویر", data=file, file_name=filename, mime="image/png")

# اجرای برنامه
generate_schedule()
