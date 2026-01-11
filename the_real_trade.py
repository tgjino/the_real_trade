import streamlit as st 
st.title("The Real Trade")

sell_premium = st.number_input("Sell Premium", value = 0.0)
buy_premium = st.number_input("Buy Premium", value = 0.0)

if st.buttom("Calculate Profit"):
    if sell_premium > 0:
        net_profit = (sell_premium - buy_premium) * 25
        st.sucess(f"Yours approximate profit: {net_profit}")
    else:
        st.warning("Give a amount")