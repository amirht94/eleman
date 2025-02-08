import streamlit as st

# استایل سفارشی برای بهبود نمایش
st.markdown("""
    <style>
        .stTextInput, .stNumberInput {
            width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)

# عنوان برنامه
st.title("برنامه‌ریزی هفتگی مطالعه")

# دریافت کل ساعات مطالعه‌ی هفتگی
total_weekly_hours = st.number_input("کل ساعت مطالعه‌ی هفتگی (به ساعت):", min_value=1, step=1, key="total_hours")

# دروس مورد نظر (می‌توان بر اساس رشته و پایه شخصی‌سازی کرد)
main_subjects = ["ریاضی", "فیزیک", "شیمی", "زیست", "ادبیات"]

# ذخیره ساعات مطالعه‌ی هر درس در session_state برای مدیریت مقادیر
if "subject_hours" not in st.session_state:
    st.session_state.subject_hours = {subject: 0 for subject in main_subjects}

# نمایش مقدار ساعات باقی‌مانده در بالای فرم
allocated = sum(st.session_state.subject_hours.values())  # جمع کل ساعات تخصیص داده شده
remaining = total_weekly_hours - allocated  # ساعت‌های باقی‌مانده
st.markdown(f"### ⏳ ساعات باقی‌مانده: **{remaining} ساعت**")

# فرم ورودی ساعت‌های هر درس
st.markdown("#### ⏬ تخصیص ساعات برای هر درس:")
for subject in main_subjects:
    st.session_state.subject_hours[subject] = st.number_input(
        f"⏳ ساعت برای {subject}", min_value=0, step=1, value=st.session_state.subject_hours[subject], key=subject
    )

# بروزرسانی مقدار ساعات باقی‌مانده پس از هر تغییر
allocated = sum(st.session_state.subject_hours.values())
remaining = total_weekly_hours - allocated
st.markdown(f"### ⏳ ساعات باقی‌مانده: **{remaining} ساعت**")

# پیام هشدار در صورت تخصیص بیش از حد
if remaining < 0:
    st.error("⚠️ مجموع ساعت‌های تخصیص‌یافته بیش از کل ساعت مطالعه‌ی هفتگی است!")

