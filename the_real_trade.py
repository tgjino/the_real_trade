import streamlit as st 
import plotly.graph_objects as go
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

def plot_payoff(entry, target, sl):
    x = [sl - 100, sl, entry, target, taget + 100]
    Y = [-(entry-sl), -(entry-sl), 0, (target-entry), (target-entry)]

    fig = go.figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='P&L'))

    fig.add_hline(y=0, line_dash="dash", line_color="white")

    fig.update_layout(title="Strategy Payoff Graph", xaxis_title="Price", yaxis_title="Profit/Loss", template="plotly_dark")

st.subheader("Profit/Loss Visualization")

fig = plot_payoff(22000, 22100, 21950)
st.plotly_chart(fig, use_container_width=True)
