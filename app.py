import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Retail Data Analysis", layout="wide")
st.title("Online Retail Dataset Analysis")

uploaded_file = st.file_uploader("Upload OnlineRetail.xlsx file", type=["xlsx"])

if uploaded_file is not None:
    pdf = pd.read_excel(uploaded_file, sheet_name=0)
    st.success("File uploaded successfully.")

    pdf = pdf.dropna(subset=["Country", "Description", "Quantity", "UnitPrice"])
    pdf["TotalPrice"] = pdf["Quantity"] * pdf["UnitPrice"]

    Q1 = pdf["UnitPrice"].quantile(0.25)
    Q3 = pdf["UnitPrice"].quantile(0.75)
    IQR = Q3 - Q1
    lower_iqr = Q1 - 3 * IQR
    upper_iqr = Q3 + 3 * IQR

    pdf = pdf[(pdf["UnitPrice"] >= lower_iqr) & (pdf["UnitPrice"] <= upper_iqr)]

    scaler = StandardScaler()
    pdf[["Quantity_scaled", "UnitPrice_scaled", "TotalPrice_scaled"]] = scaler.fit_transform(
        pdf[["Quantity", "UnitPrice", "TotalPrice"]]
    )

    if st.checkbox("Show raw data"):
        st.dataframe(pdf.head(50))

    st.subheader("Boxplot of Quantity, UnitPrice, and TotalPrice")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=pdf[["Quantity", "UnitPrice", "TotalPrice"]], ax=ax)
    st.pyplot(fig)

    grouped = pdf.groupby(["Country", "Description"]).agg({
        "Quantity": "sum",
        "UnitPrice": "mean",
        "TotalPrice": "sum"
    }).reset_index()

    country = st.selectbox("Select a country", grouped["Country"].unique())

    def top_bottom_items(data, feature):
        temp = data[data["Country"] == country].sort_values(by=feature, ascending=False)
        top_3 = temp.head(3)[["Description", feature]]
        bottom_3 = temp.tail(3)[["Description", feature]]
        return top_3, bottom_3

    st.subheader(f"Top and Bottom Items by Quantity in {country}")
    top_q, bottom_q = top_bottom_items(grouped, "Quantity")
    st.write("Top 3")
    st.dataframe(top_q)
    st.write("Bottom 3")
    st.dataframe(bottom_q)

    st.subheader(f"Top and Bottom Items by UnitPrice in {country}")
    top_p, bottom_p = top_bottom_items(grouped, "UnitPrice")
    st.write("Top 3")
    st.dataframe(top_p)
    st.write("Bottom 3")
    st.dataframe(bottom_p)

    st.subheader(f"Top and Bottom Items by TotalPrice in {country}")
    top_t, bottom_t = top_bottom_items(grouped, "TotalPrice")
    st.write("Top 3")
    st.dataframe(top_t)
    st.write("Bottom 3")
    st.dataframe(bottom_t)
