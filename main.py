import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# استایل سفارشی برای نمایش بهتر ورودی‌ها
st.markdown("""
    <style>
        .stTextInput, .stNumberInput {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# عنوان اصلی برنامه
st.title("📅 برنامه‌ریزی هفتگی مطالعه")

# دریافت اطلاعات کاربر
stream = st.selectbox("📚 رشته تحصیلی:", ["ریاضی", "تجربی", "انسانی"])
grade = st.selectbox("🎓 پایه تحصیلی:", ["دهم", "یازدهم", "دوازدهم"])
student_type = st.radio("🎯 نوع مطالعه:", ["کنکوری", "نهایی"]) if grade == "دوازدهم" else "نهایی"

# تعیین دروس بر اساس رشته و پایه تحصیلی
subject_dict = {
    "ریاضی": {
        "دهم": ["هندسه", "فیزیک", "شیمی"],
        "یازدهم": ["حسابان", "آمار و احتمال", "هندسه", "فیزیک", "شیمی"],
        "دوازدهم": ["گسسته", "حسابان", "هندسه", "فیزیک", "شیمی"]
    },
    "تجربی": {
        "دهم": ["زیست", "شیمی", "ریاضی", "فیزیک"],
        "یازدهم": ["زیست", "شیمی", "ریاضی", "فیزیک"],
        "دوازدهم": ["زیست", "شیمی", "ریاضی", "فیزیک"]
    },
    "انسانی": {
        "دهم": ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"],
        "یازدهم": ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"],
        "دوازدهم": ["فارسی", "عربی", "دین و زندگی", "زبان انگلیسی"]
    }
}

main_subjects = subject_dict[stream][grade]

if student_type == "کنکوری":
    for prev_grade in ["یازدهم", "دهم"]:
        main_subjects += [f"{sub} ({prev_grade})" for sub in subject_dict[stream][prev_grade]]

# دریافت کل ساعات مطالعه‌ی هفتگی
total_weekly_hours = st.number_input("⏳ کل ساعت مطالعه‌ی هفتگی:", min_value=1, step=1, key="total_hours")

# مقداردهی اولیه ساعت مطالعه برای هر درس
if "subject_hours" not in st.session_state:
    st.session_state.subject_hours = {subject: 0 for subject in main_subjects}

allocated = sum(st.session_state.subject_hours.values())
remaining = total_weekly_hours - allocated
st.markdown(f"### ⏳ ساعات باقی‌مانده: **{remaining} ساعت**")

# تخصیص ساعت برای هر درس
st.markdown("#### ⏬ تخصیص ساعات برای هر درس:")
for subject in main_subjects:
    st.session_state.subject_hours[subject] = st.number_input(
        f"⏳ ساعت برای {subject}",
        min_value=0,
        max_value=total_weekly_hours,
        step=1,
        value=st.session_state.subject_hours[subject],
        key=subject
    )

# محاسبه مجدد ساعات باقی‌مانده
allocated = sum(st.session_state.subject_hours.values())
remaining = total_weekly_hours - allocated
st.markdown(f"### ⏳ ساعات باقی‌مانده: **{remaining} ساعت**")

# هشدار در صورت تخصیص بیش از حد
if remaining < 0:
    st.error("⚠️ مجموع ساعت‌های تخصیص‌یافته بیش از کل ساعت مطالعه‌ی هفتگی است!")

# ایجاد برنامه هفتگی
days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
schedule = {day: [] for day in days}

for subject, hours in st.session_state.subject_hours.items():
    if hours > 0:
        slots = (hours * 2) // 3  # تقسیم زمان بر اساس بازه‌های 1.5 ساعته
        extra_slots = slots % len(days)
        daily_slots = slots // len(days)

        for i, day in enumerate(days):
            num_slots = daily_slots + (1 if i < extra_slots else 0)
            if num_slots > 0:
                schedule[day].append(f"{subject} ({num_slots * 1.5:.1f} ساعت)")

# نمایش برنامه هفتگی در جدول
st.subheader("📆 برنامه‌ی هفتگی پیشنهادی:")
df_schedule = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in schedule.items()]))
st.table(df_schedule.fillna(""))

# رسم جدول برنامه هفتگی و امکان دانلود تصویر
def generate_schedule_image(schedule):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("tight")
    ax.axis("off")
    
    # داده‌های جدول
    data = [[", ".join(schedule[day]) if schedule[day] else "❌ استراحت" for day in days]]
    
    # رسم جدول
    table = ax.table(cellText=data, colLabels=days, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width([0, 1, 2, 3, 4, 5])
    
    return fig

if st.button("📥 دانلود جدول برنامه هفتگی"):
    fig = generate_schedule_image(schedule)
    st.pyplot(fig)
    
    # ذخیره تصویر
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    st.download_button(
        label="📸 دانلود تصویر برنامه",
        data=buf,
        file_name="study_schedule.png",
        mime="image/png"
    )
