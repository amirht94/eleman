# درون فرم ورودی‌ها:
for subject in main_subjects:
    colA, colB = st.columns([2, 1])
    with colA:
        st.write(subject)
    with colB:
        hours = st.number_input("ساعت", min_value=0, step=1, key=subject)
    subject_hours[subject] = hours

# پس از ثبت فرم:
total_allocated = sum(subject_hours.values())
if total_allocated != total_weekly_hours:
    st.warning(f"مجموع ساعت‌های تخصیص داده شده ({total_allocated}) برابر با کل ساعت تعیین شده ({total_weekly_hours}) نیست. لطفاً مجدداً تخصیص را بررسی کنید.")
