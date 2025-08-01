import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Room Appliance Usage & Energy Dashboard")
st.markdown("""
This app visualizes how long appliances were used and how much energy they consumed.
Upload a CSV with columns: `Appliance`, `Power (W)`, `Hours/Day`, and `Days`.
""")

# Upload CSV file
uploaded_file = st.file_uploader("energy_days.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Validate columns
    required_cols = ["Appliance", "Power (W)", "Hours/Day", "Days"]
    if not all(col in df.columns for col in required_cols):
        st.error("CSV must contain columns: Appliance, Power (W), Hours/Day, Days")
    else:
        # Compute energy in kWh
        df["Energy (kWh)"] = (df["Power (W)"] * df["Hours/Day"] * df["Days"]) / 1000

        # Show data
        st.subheader("Appliance Data with Energy Calculated")
        st.dataframe(df)

        for metric in ["Days", "Energy (kWh)"]:
            st.subheader(f"{metric} per Appliance")

            # Line Chart
            fig1, ax1 = plt.subplots(figsize=(6, 3))
            ax1.plot(df["Appliance"], df[metric], marker='o', color='teal')
            ax1.set_title(f"Line Chart - {metric}")
            ax1.set_ylabel(metric)
            ax1.set_xlabel("Appliance")
            st.pyplot(fig1)

            # Bar Chart
            fig2, ax2 = plt.subplots(figsize=(6, 3))
            bars = ax2.bar(df["Appliance"], df[metric], color='skyblue')
            ax2.set_title(f"Bar Chart - {metric}")
            ax2.set_ylabel(metric)
            ax2.set_xlabel("Appliance")
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{height:.2f}', ha='center')
            st.pyplot(fig2)

            # Pie Chart
            fig3, ax3 = plt.subplots(figsize=(4, 4))
            ax3.pie(df[metric], labels=df["Appliance"], autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
            ax3.set_title(f"Pie Chart - {metric}")
            ax3.axis('equal')
            st.pyplot(fig3)
