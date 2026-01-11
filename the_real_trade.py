import streamlit as st 
st.set_page_config(page_title = "The Real Trade", layout="wide")

st.sidebar.title("Trading Settings")
strategy = st.sidebar.selectbox("Select Strategy", ["Nifty Calculation","Jade Lizard","Iron Condor"])

st.title(f"Strategy: {strategy}")

if strategy == "Nifty Calculation":
    col1, col2 = st.columns(2)

    with col1:
        entry = st.number_input("Entry Price", value=22000.0)
        stop_loss_pct = st.slider("Stop Loss (%)", 0.5, 5.0, 1.0)

        target = entry + (entry * (stop_loss_pct * 2 / 100))
        sl_price = entry - (entry * (stop_loss_pct / 100))

        with col2:
            st.success(f"Target: {target: .2f}")
            st.error(f"Stop Loss: {sl_price: .2f}")
    
elif strategy == "Jade Lizard":
    st.info("Jade Lizard strategy details coming soon...")
    st.write("Here you can set your put option and call spread")

elif strategy == "Iron Condor":
    st.info("Iron condor strategy details coming soon...")

sell_premium = st.number_input("Sell Premium", value = 0.0)
buy_premium = st.number_input("Buy Premium", value = 0.0)

if st.button("Calculate Profit"):
    if sell_premium > 0:
        net_profit = (sell_premium - buy_premium) * 25
        st.success(f"Yours approximate profit: {net_profit}")
    else:
        st.warning("Give a amount")