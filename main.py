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
    
    # دریافت اطلاعات اولیه: رشته و پایه (با استفاده از ستون‌ها برای بهبود نمایش)
    col1, col2 = st.columns(2)
    with col1:
        stream = st.text_input("رشته‌ی دانش‌آموز (ریاضی/تجربی/انسانی):").strip()
    with col2:
        grade = st.text_input("پایه‌ی تحصیلی دانش‌آموز (دهم/یازدهم/دوازدهم):").strip()
    
    if not stream or not grade:
        st.info("لطفاً ابتدا رشته و پایه را وارد کنید.")
        st.stop()
    
    # تعیین نوع دانش‌آموز برای پایه دوازدهم
    if grade == "دوازدهم":
        student_type = st.radio("آیا دانش‌آموز کنکوری است یا فقط امتحانات نهایی دارد؟", ("کنکوری", "نهایی"))
    else:
        student_type = "نهایی"
    
    # تعیین لیست دروس بر اساس رشته و پایه
    if stream == "ریاضی":
        if grade == "دهم":
            main_subjects = ["هندسه", "فیزیک", "شیمی"]
        elif grade == "یازدهم":
            main_subjects = ["حسابان", "آمار و احتمال", "هندسه", "فیزیک", "شیمی"]
        elif grade == "دوازدهم":
            main_subjects = ["گسسته", "حسابان", "هندسه", "فیزیک", "شیمی"]
            if student_type == "کنکوری":
                main_subjects += ["حسابان (یازدهم)", "آمار و احتمال (یازدهم)", "هندسه (یازدهم)",
                                  "فیزیک (یازدهم)", "شیمی (یازدهم)",
                                  "هندسه (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
        else:
            st.error("پایه وارد شده صحیح نیست!")
            st.stop()
    elif stream == "تجربی":
        if grade in ["دهم", "یازدهم", "دوازدهم"]:
            main_subjects = ["زیست", "شیمی", "ریاضی", "فیزیک"]
            if grade == "دوازدهم" and student_type == "کنکوری":
                main_subjects += ["زیست (یازدهم)", "ریاضی (یازدهم)", "فیزیک (یازدهم)", "شیمی (یازدهم)",
                                  "زیست (دهم)", "ریاضی (دهم)", "فیزیک (دهم)", "شیمی (دهم)"]
        else:
            st.error("پایه وارد شده صحیح نیست!")
            st.stop()
    elif stream == "انسانی":
        if grade in ["دهم", "یازدهم", "دوازدهم"]:
            main_subjects = ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
            if grade == "دوازدهم" and student_type == "کنکوری":
                main_subjects += ["فارسی (یازدهم)", "عربی (یازدهم)", "دین و زندگی (یازدهم)", "زبان انگلیسی (یازدهم)",
                                  "فارسی (دهم)", "عربی (دهم)", "دین و زندگی (دهم)", "زبان انگلیسی (دهم)"]
        else:
            st.error("پایه وارد شده صحیح نیست!")
            st.stop()
    else:
        st.error("رشته وارد شده صحیح نیست!")
        st.stop()
    
    # دریافت کل ساعت مطالعه‌ی هفتگی
    total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت):", min_value=1, step=1, key="total_hours")
    
    # اگر متغیر subject_hours قبلاً در session_state تعریف نشده باشد، آن را مقداردهی اولیه می‌کنیم.
    if "subject_hours" not in st.session_state:
        st.session_state.subject_hours = {subject: 0 for subject in main_subjects}
    else:
        # در صورتی که دروس تغییر کرده باشند، موارد جدید را اضافه می‌کنیم.
        for subject in main_subjects:
            if subject not in st.session_state.subject_hours:
                st.session_state.subject_hours[subject] = 0
    
    # محاسبه تخصیص کل شده و ساعات باقی‌مانده
    allocated = sum(st.session_state.subject_hours.get(sub, 0) for sub in main_subjects)
    remaining = total_weekly_hours - allocated
    st.markdown(f"### ساعات باقی‌مانده: **{remaining}**")
    
    st.markdown("#### لطفاً تخصیص ساعت برای هر درس را مشخص کنید:")
    # نمایش هر درس به همراه ورودی تخصیص ساعت؛ با استفاده از ستون‌ها جهت صرفه‌جویی در فضا
    for subject in main_subjects:
        colA, colB = st.columns([2, 1])
        with colA:
            st.write(subject)
        with colB:
            # مقدار پیش‌فرض از session_state گرفته شده است؛ تغییرات به محض وارد شدن ذخیره می‌شود.
            st.session_state.subject_hours[subject] = st.number_input(
                f"ساعت برای {subject}",
                min_value=0,
                step=1,
                value=st.session_state.subject_hours[subject],
                key=subject
            )
        # پس از هر ورودی، دوباره مقدار تخصیص شده و باقی‌مانده محاسبه می‌شود.
        allocated = sum(st.session_state.subject_hours.get(sub, 0) for sub in main_subjects)
        remaining = total_weekly_hours - allocated
        st.write(f"ساعات باقی‌مانده: {remaining}")
    
    # دکمه ثبت برنامه؛ پس از کلیک، در صورت تطابق مجموع ساعت‌ها، برنامه ساخته می‌شود.
    if st.button("ثبت برنامه"):
        if remaining != 0:
            st.error(f"مجموع ساعت‌های تخصیص داده شده ({allocated}) با کل ساعت مطالعه‌ی هفتگی ({total_weekly_hours}) برابر نیست!")
            st.stop()
        
        # ایجاد برنامه هفتگی؛ هر اسلات معادل 1.5 ساعت است.
        days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
        schedule = {day: [] for day in days}
        for subject, hours in st.session_state.subject_hours.items():
            total_slots = int(hours * 2 / 3)  # تبدیل ساعت به تعداد اسلات (هر اسلات 1.5 ساعت)
            daily_slots = total_slots // len(days)
            extra_slots = total_slots % len(days)
            for i, day in enumerate(days):
                slots = daily_slots + (1 if i < extra_slots else 0)
                schedule[day].append({"name": subject, "slots": slots})
        
        # نمایش برنامه هفتگی به صورت جدول
        st.subheader("برنامه‌ی هفتگی شما:")
        table_data = []
        for day in days:
            row = [day]
            for subject in main_subjects:
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
        
        with open(filename, "rb") as file:
            st.download_button(label="دانلود جدول به صورت تصویر", data=file, file_name=filename, mime="image/png")

# اجرای برنامه
generate_schedule()
