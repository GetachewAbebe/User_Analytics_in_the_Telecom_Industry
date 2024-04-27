import streamlit as st
import pandas as pd

# Assuming you have already loaded and cleaned your DataFrame
cleaned_df = pd.DataFrame({
    'Handset Type': ['iPhone 12', 'Galaxy S21', 'Pixel 5', 'iPhone 13', 'Galaxy S22', 'Pixel 6', 'iPhone 14', 'Galaxy S23', 'Pixel 7']
})

# Extracting the manufacturer information from the 'Handset Type' column
cleaned_df['Manufacturer'] = cleaned_df['Handset Type'].str.split().str[0]

# Use value_counts to count the occurrences of each manufacturer and select the top 3
top_3_manufacturers = cleaned_df['Manufacturer'].value_counts().head(3)

st.title("Top 3 Manufacturers and Their Top 5 Handsets")

# Iterate through the top 3 manufacturers and display the top 5 handsets for each
for manufacturer in top_3_manufacturers.index:
    top_5_handsets = cleaned_df[cleaned_df['Manufacturer'] == manufacturer]['Handset Type'].value_counts().head(5)
    st.subheader(f"Top 5 handsets for {manufacturer}:")
    st.write(top_5_handsets)
    st.write("\n")
