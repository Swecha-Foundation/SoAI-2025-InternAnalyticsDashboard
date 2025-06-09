import streamlit as st
import pandas as pd
import altair as alt

def display_data(data, cohort_type, intern_type):
    df = pd.DataFrame(data)

    if intern_type == "ai":
        filter_data = 25000
    elif intern_type == "techlead":
        filter_data = 1730
    else:
        st.info("Please select intern type.")
        return


    if cohort_type == "cohort1":
        df = df[df['Id'] <= filter_data]
    else:
        df = df[df['Id'] > filter_data]

    # Rename columns for easier access
    df.rename(columns={
        'Affiliation (College/Company/Organization Name)': 'CollegeName',
        'Full Name': 'FullName',
        'Id': 'StudentID'
    }, inplace=True)

    # Clean and type-cast
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Gender'] = df['Gender'].str.strip().str.title()
    df['CollegeName'] = df['CollegeName'].str.strip()

    st.header("📊 College Wise Registrations")

    college_data = df.groupby('CollegeName')['StudentID'].count().reset_index()
    college_data.rename(columns={'StudentID': 'TotalRegistrations'}, inplace=True)

    total_registrations = college_data['TotalRegistrations'].sum()
    total_colleges = college_data['CollegeName'].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Registrations", f"{total_registrations:,}")
    col2.metric("Number of Colleges", f"{total_colleges}")

    st.subheader("🏆 Registrations by College")
    top_n = st.slider("Select number of top colleges", min_value=5, max_value=50, value=10)
    top_df = college_data.sort_values(by="TotalRegistrations", ascending=False).head(top_n)

    top_df_display = top_df.reset_index(drop=True)
    top_df_display.index = top_df_display.index + 1
    st.dataframe(top_df_display, use_container_width=True)

    st.subheader("📈 Bar Chart - Top Colleges")
    chart = alt.Chart(top_df).mark_bar().encode(
        x=alt.X('TotalRegistrations:Q', title='Registrations'),
        y=alt.Y('CollegeName:N', sort='-x', title='College Name'),
        tooltip=['CollegeName', 'TotalRegistrations']
    )
    st.altair_chart(chart, use_container_width=True)

    st.subheader("🏫 All Colleges - Registration Wise")

    # Sort all colleges by registration count (optional for visualization)
    all_df = college_data.sort_values(by="TotalRegistrations", ascending=False)

    with st.container():
        search_query_all = st.text_input("Enter college name", placeholder="e.g., NIT, IIT, SRM")

        if search_query_all:
            filtered_all_df = all_df[all_df["CollegeName"].str.contains(search_query_all, case=False, na=False)]
            st.success(f"Found {len(filtered_all_df)} matching colleges")
        else:
            filtered_all_df = all_df

        all_df_display = filtered_all_df.reset_index(drop=True)
        all_df_display.index = all_df_display.index + 1

        st.dataframe(all_df_display, use_container_width=True)

    # Age Analysis
    st.header("🎂 Registrations by Age")
    age_df = df.dropna(subset=['Age'])
    bins = [15, 18, 21, 24, 27, 30, float('inf')]
    labels = ['15-18', '19-21', '22-24', '25-27', '28-30', '30-above']
    age_df['AgeGroup'] = pd.cut(age_df['Age'], bins=bins, labels=labels, right=False)

    age_group_data = age_df.groupby('AgeGroup', observed=False)['StudentID'].count().reset_index()
    age_group_data.rename(columns={'StudentID': 'TotalStudents'}, inplace=True)

    st.dataframe(age_group_data, use_container_width=True)

    age_chart = alt.Chart(age_group_data).mark_bar().encode(
        x=alt.X('AgeGroup:N', title='Age Group'),
        y=alt.Y('TotalStudents:Q', title='Total Students'),
        color='AgeGroup:N',
        tooltip=['AgeGroup', 'TotalStudents']
    ).properties(width=700, height=400)

    st.altair_chart(age_chart, use_container_width=True)

    # Gender Analysis
    st.header("🚻 Registrations by Gender")
    gender_data = df.groupby('Gender')['StudentID'].count().reset_index()
    gender_data.rename(columns={'StudentID': 'TotalStudents'}, inplace=True)

    st.dataframe(gender_data, use_container_width=True)

    gender_chart = alt.Chart(gender_data).mark_bar().encode(
        x=alt.X('Gender:N', title='Gender'),
        y=alt.Y('TotalStudents:Q', title='Total Students'),
        color='Gender:N',
        tooltip=['Gender', 'TotalStudents']
    ).properties(width=700, height=400)

    st.altair_chart(gender_chart, use_container_width=True)