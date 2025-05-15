
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('unicorns.csv')
df.columns = df.columns.str.strip()
df['Valuation ($B)'] = df['Valuation ($B)'].astype(str).str.replace('[^0-9.]', '', regex=True)
df['Valuation ($B)'] = pd.to_numeric(df['Valuation ($B)'], errors='coerce')
df['Date Joined'] = pd.to_datetime(df['Date Joined'], errors='coerce')
df['Year Joined'] = df['Date Joined'].dt.year

# App title and introduction
st.title("🦄 Unicorn Startups Dashboard")
st.markdown("""
Welcome to the **Unicorn Startups Analysis App**!  
This dashboard presents visual insights into unicorn companies (startups valued at over $1 billion).  
It covers key aspects like company valuation distribution, geographic concentration, industry trends, and founding timelines.
""")

# Graph 1 – Distribution of Unicorn Company Valuations
st.subheader("1. Distribution of Unicorn Company Valuations")
filtered_val = df[df['Valuation ($B)'] < 200]
fig1, ax1 = plt.subplots()
sns.histplot(data=filtered_val, x='Valuation ($B)', bins=30, kde=True, color='skyblue', ax=ax1)
ax1.set_title("Distribution of Unicorn Valuations")
ax1.set_xlabel("Valuation ($B)")
st.pyplot(fig1)
st.markdown("This histogram shows how unicorn valuations are distributed, revealing a concentration of companies around lower valuation ranges and fewer outliers with extreme values.")

# Graph 2 – Top 10 Countries by Number of Unicorns
st.subheader("2. Top 10 Countries by Number of Unicorns")
top_countries = df['Country'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis', ax=ax2)
ax2.set_title("Top Countries")
ax2.set_xlabel("Number of Unicorns")
ax2.set_ylabel("Country")
st.pyplot(fig2)
st.markdown("This bar chart highlights the top countries with the highest number of unicorn companies, showcasing global centers of innovation and investment.")

# Graph 3 – Valuation Distribution by Industry (Top 10 only)
st.subheader("3. Valuation Distribution by Industry (Top 10 Industries)")
top_industries = df['Industry'].value_counts().head(10).index
filtered_df = df[df['Industry'].isin(top_industries)].copy()
order = filtered_df.groupby('Industry')['Valuation ($B)'].median().sort_values(ascending=False).index
fig3, ax3 = plt.subplots(figsize=(14, 6))
sns.boxplot(data=filtered_df, x='Industry', y='Valuation ($B)', order=order, palette='Set2', ax=ax3, showfliers=False)
medians = filtered_df.groupby('Industry')['Valuation ($B)'].median().reindex(order)
for i, median_val in enumerate(medians):
    ax3.text(i, median_val + 0.5, f'{median_val:.1f}B', ha='center', fontsize=10, weight='bold')
plt.xticks(rotation=30, ha='right')
ax3.set_ylabel("Valuation in Billions of Dollars ($B)")
st.pyplot(fig3)
st.markdown("This colorful boxplot compares company valuations across the top 10 industries. It helps highlight industries where startups tend to be valued higher.")

# Graph 4 – Unicorns Founded per Year
st.subheader("4. Number of Unicorns Founded Per Year")
year_counts = df['Year Joined'].value_counts().sort_index()
fig4, ax4 = plt.subplots()
sns.lineplot(x=year_counts.index, y=year_counts.values, marker='o', ax=ax4)
ax4.set_title("Unicorns Founded Per Year")
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Unicorns")
st.pyplot(fig4)
st.markdown("This line plot reveals trends in unicorn company formations across years, highlighting periods of growth and slowdowns in the startup ecosystem.")

