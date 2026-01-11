 import streamlit as st
import plotly.graph_objects as go

# ലേഔട്ട് സെറ്റിംഗ്സ്
st.set_page_config(page_title="The Real Trade", layout="wide")

# സൈഡ് ബാർ
st.sidebar.title("Trading Settings")
strategy = st.sidebar.selectbox("Select Strategy", ["Nifty Calculation", "Jade Lizard", "Iron Condor"])

st.title(f"Strategy: {strategy}")

if strategy == "Nifty Calculation":
    col1, col2 = st.columns(2)
    with col1:
        entry = st.number_input("Entry Price", value=22000.0)
        stop_loss_pct = st.slider("Stop Loss (%)", 0.5, 5.0, 1.0)
    
    target = entry + (entry * (stop_loss_pct * 2 / 100))
    sl_price = entry - (entry * (stop_loss_pct / 100))
    
    with col2:
        st.success(f"Target: {target:.2f}")
        st.error(f"Stop Loss: {sl_price:.2f}")

# പേ-ഓഫ് ഗ്രാഫ് ഫങ്ക്ഷൻ
def plot_payoff(entry, target, sl):
    x = [sl - 100, sl, entry, target, target + 100]
    y = [-(entry-sl), -(entry-sl), 0, (target-entry), (target-entry)]
    
    fig = go.Figure() # F എന്നത് ക്യാപിറ്റൽ ആണ്
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='P&L'))
    fig.add_hline(y=0, line_dash="dash", line_color="white")
    fig.update_layout(title="Strategy Payoff Graph", template="plotly_dark")
    return fig

st.subheader("Profit/Loss Visualization")
# ഗ്രാഫ് കാണിക്കുന്നു
fig = plot_payoff(22000, 22100, 21950)
st.plotly_chart(fig, use_container_width=True)

