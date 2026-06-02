import streamlit as st
import pandas as pd
import plotly.express as px

# Page Settings
st.set_page_config(
    page_title="EduPro Dashboard",
    layout="wide"
)
with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# Title
st.title("Learner Demographics and Course Enrollment Behavior Analysis")

# Excel File Load
excel_file = "EduPro Online Platform actualy data.xlsx"

users = pd.read_excel(excel_file, sheet_name="Users")
courses = pd.read_excel(excel_file, sheet_name="Courses")
transactions = pd.read_excel(excel_file, sheet_name="Transactions")
teachers = pd.read_excel(excel_file, sheet_name="Teachers")



# =========================
# SIDEBAR FILTER
# =========================

st.sidebar.header("Filters")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=users["Gender"].unique(),
    default=users["Gender"].unique()
)


# Age Group Creation

users["AgeGroup"] = pd.cut(
    users["Age"],
    bins=[0, 18, 25, 35, 45, 100],
    labels=["<18", "18-25", "26-35", "36-45", "45+"]
)

selected_agegroup = st.sidebar.multiselect(
    "Select Age Group",
    options=users["AgeGroup"].unique(),
    default=users["AgeGroup"].unique()
)
st.sidebar.subheader("Course Filters")

selected_level = st.sidebar.multiselect(
    "Course Level",
    courses["CourseLevel"].unique(),
    default=courses["CourseLevel"].unique()
)
selected_category = st.sidebar.multiselect(
    "Course Category",
    courses["CourseCategory"].unique(),
    default=courses["CourseCategory"].unique()
)



filtered_users = users[
    (users["Gender"].isin(selected_gender))
    &
    (users["AgeGroup"].isin(selected_agegroup))
]

# =========================
# KPI CARDS
# =========================

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Learners", len(filtered_users))

with col2:
    st.metric("Total Courses", len(courses))

with col3:
    st.metric("Total Teachers", len(teachers))

with col4:
    st.metric("Total Transactions", len(transactions))

with col5:
    st.metric("Total Enrollments",len(transactions))
    
    # NEW KPI
avg_courses = round(
    len(transactions) /
    users["UserID"].nunique(),
    2
)

with col6:
    st.metric(
        "Avg Courses/Learner",
        avg_courses
    )

# =========================
# GENDER CHART
# =========================

gender_count = (
    filtered_users["Gender"]
    .value_counts()
    .reset_index()
)

gender_count.columns = ["Gender", "Count"]

fig = px.pie(
    gender_count,
    names="Gender",
    values="Count",
    title="Gender Distribution"
)

# =========================
# COURSE CATEGORY CHART
# =========================

course_count = (
    courses["CourseCategory"]
    .value_counts()
    .reset_index()
)

course_count.columns = ["Course Category", "Count"]

fig2 = px.bar(
    course_count,
    x="Course Category",
    y="Count",
    title="Course Category Distribution"
)

# =========================
# DISPLAY 2 CHARTS IN ROW
# =========================

chart1, chart2 = st.columns(2)

with chart1:
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# REVENUE ANALYSIS
# =========================

st.subheader("Revenue Analysis")

revenue_by_method = (
    transactions.groupby("PaymentMethod")["Amount"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    revenue_by_method,
    x="PaymentMethod",
    y="Amount",
    title="Revenue by Payment Method"
)

st.plotly_chart(fig3, use_container_width=True)


# =========================
# DATA MERGE
# =========================

merged = transactions.merge(
    users,
    on="UserID"
).merge(
    courses,
    on="CourseID"
)

# =========================
# FILTERED MERGED DATA
# =========================
merged["AgeGroup"] = pd.cut(
    merged["Age"],
    bins=[0, 18, 25, 35, 45, 100],
    labels=["<18", "18-25", "26-35", "36-45", "45+"]
)

filtered_merged = merged[
    (merged["CourseLevel"].isin(selected_level))
    &
    (merged["CourseCategory"].isin(selected_category))
    &
    (merged["Gender"].isin(selected_gender))
    &
    (merged["AgeGroup"].isin(selected_agegroup))
]


# =========================
# AGE GROUP CREATION
# =========================

users["AgeGroup"] = pd.cut(
    users["Age"],
    bins=[0, 18, 25, 35, 45, 100],
    labels=["<18", "18-25", "26-35", "36-45", "45+"]
)

# =========================
# AGE DISTRIBUTION
# =========================

st.subheader("Age Distribution of Learners")

age_count = (
    users["AgeGroup"]
    .value_counts()
    .reset_index()
)

age_count.columns = ["Age Group", "Count"]

fig4 = px.bar(
    age_count,
    x="Age Group",
    y="Count",
    title="Age Distribution of Learners"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# GENDER VS COURSE CATEGORY
# =========================

st.subheader("Gender vs Course Category")

gender_course = (
    filtered_merged.groupby(
        ["Gender", "CourseCategory"]
    )
    .size()
    .reset_index(name="Enrollments")
)

fig5 = px.bar(
    gender_course,
    x="CourseCategory",
    y="Enrollments",
    color="Gender",
    barmode="group",
    title="Gender Based Course Preferences"
)

st.plotly_chart(fig5, use_container_width=True)


# =========================
# COURSE LEVEL ANALYSIS
# =========================

st.subheader("Course Level Distribution")

level_count = (
    filtered_merged["CourseLevel"]
    .value_counts()
    .reset_index()
)

level_count.columns = ["Course Level", "Count"]

fig6 = px.bar(
    level_count,
    x="Course Level",
    y="Count",
    color="Course Level",
    title="Course Level Distribution"
)

st.plotly_chart(fig6, use_container_width=True)

# =========================
# COURSE TYPE ANALYSIS
# =========================

st.subheader("Course Type Distribution")

type_count = (
    filtered_merged["CourseType"]
    .value_counts()
    .reset_index()
)

type_count.columns = ["Course Type", "Count"]

fig7 = px.pie(
    type_count,
    names="Course Type",
    values="Count",
    title="Course Type Distribution"
)

st.plotly_chart(fig7, use_container_width=True)

# =========================
# AGE GROUP VS COURSE CATEGORY
# =========================

st.subheader("Age Group vs Course Category")

age_course = (
    filtered_merged.groupby(
        ["AgeGroup", "CourseCategory"]
    )
    .size()
    .reset_index(name="Enrollments")
)

fig8 = px.bar(
    age_course,
    x="AgeGroup",
    y="Enrollments",
    color="CourseCategory",
    barmode="group",
    title="Age Group vs Course Category"
)

st.plotly_chart(fig8, use_container_width=True)

# =========================
# ENROLLMENTS BY AGE GROUP
# =========================

st.subheader("Enrollments by Age Group")

age_enrollment = (
    filtered_merged.groupby("AgeGroup")
    .size()
    .reset_index(name="Enrollments")
)

fig9 = px.bar(
    age_enrollment,
    x="AgeGroup",
    y="Enrollments",
    color="AgeGroup",
    title="Enrollments by Age Group"
)

st.plotly_chart(fig9, use_container_width=True)

# =========================
# TEACHER EXPERTISE ANALYSIS
# =========================

st.subheader("Teacher Expertise Distribution")

teacher_exp = (
    teachers["Expertise"]
    .value_counts()
    .reset_index()
)

teacher_exp.columns = ["Expertise", "Count"]

fig10 = px.bar(
    teacher_exp,
    x="Expertise",
    y="Count",
    color="Expertise",
    title="Teacher Expertise Distribution"
)

st.plotly_chart(fig10, use_container_width=True)

# =========================
# FILTERED DATA TABLE
# =========================

st.markdown("---")
st.subheader("📋 Learner Enrollment Details")

st.dataframe(
    filtered_merged,
    use_container_width=True
)
csv = filtered_merged.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
# =========================
# KEY INSIGHTS
# =========================

st.subheader("📌 Key Insights")

st.markdown("""
- 26-35 age group has the highest enrollments.
- Data Science and AI courses are among the most popular categories.
- Gender distribution is balanced across most course categories.
- Beginner and Intermediate courses attract the majority of learners.
- Online course formats are preferred over offline formats.
""")
st.markdown("---")

st.markdown("---")

st.subheader("📌 Conclusion")

st.write("""
This analysis of the EduPro platform provides valuable insights into learner demographics and course enrollment behavior. 
The results show that learners in the 26–35 age group are the most active participants on the platform. 
Course categories such as Data Science, Artificial Intelligence, Programming, and Web Development attract the highest number of enrollments. 
The analysis also indicates that Beginner and Intermediate level courses are more popular than Advanced courses. 
Revenue trends and payment method analysis help understand the platform's financial performance, while teacher expertise analysis highlights the availability of skilled instructors across different domains. 
Overall, the dashboard enables data-driven decision-making by identifying learner preferences, enrollment patterns, and growth opportunities for the EduPro platform.
""")



st.markdown(
    "Developed using Streamlit, Pandas and Plotly | EduPro Analytics Dashboard"
)

