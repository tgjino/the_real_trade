import streamlit as st
import plotly.graph_objects as go
import yfinance as yf

# ലേഔട്ട് സെറ്റിംഗ്സ്
st.set_page_config(page_title="The Real Trade", layout="wide")
st.markdown("<h1 style='text-align: center;'>THE REAL TRADE</h1>", unsafe_allow_html =True)
st.divider()

# സൈഡ് ബാർ

def get_live_nifty():
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2) 
        else:
            return 0.0
    except:
        return 0.0
live_price = get_live_nifty()
st.sidebar.metric("Nifrty 50 Live", live_price)

st.sidebar.title("Trading Settings")
strategy = st.sidebar.selectbox("Select Strategy", ["Nifty Calculation", "Jade Lizard", "Iron Condor"])

st.header(f"Strategy: {strategy}")


if strategy == "Nifty Calculation":
    col1, col2 = st.columns(2)
    with col1:
        entry = st.number_input("Entry Price", value=22000.0)
        stop_loss_pct = st.slider("Stop Loss (%)", 0.5, 5.0, 1.0)
    
        target = entry + (entry * (stop_loss_pct * 2 / 100))
        sl_price = entry - (entry * (stop_loss_pct / 100))
    
    with col2:
        st.write("### Calculated Levels")
        st.success(f"Target: {target:.2f}")
        st.error(f"Stop Loss: {sl_price:.2f}")
    st.info("Tip: This target is based on a risk rivard of 1:2")
elif strategy =='Jade Lizard':
    st.title("jade Lizard Strategy Analyzer 📈")
    # st.write("Selected Jade Lizard strategy")

elif strategy == "Iron Condor":
    st.title("Iron Condor Analyzer 🦅")
    # st.write("Selected Iron Condor Analyzer")

    col1, col2, col3, col4 = st.columns(4)
    with col1: bp = st.number_input("Buy Put", value=21500)
    with col2: sp = st.number_input("Sell Put", value=21700)
    with col3: sc = st.number_input("Sell Call", value=22000)
    with col4: bc = st.number_input("Buy Call", value=22200)

    prem = st.number_input("Net Premium Recived", value=40.0)


    def calc_ic(p):
        profit = prem
        profit -= max(0, sp - p) - max(0, bp - p)
        profit -= max(0, p - sc) - max(0,p - bc)
        return profit

    
    prices = list(range(bp -200, bc + 200, 10))

    profits = [calc_ic(p) for p in prices]


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prices, y=profits, fill='tozeroy', name='Iron Condor'))
    fig.update_layout(template="plotly_dark", title="Irom Condor Payoff")
    st.plotly_chart(fig, use_container_width=True)

    max_profit = prem
    max_loss = (sp - bp) - prem
    col1, col2 = st.columns(2)
    col1.metric("Max Profit", f"rs {max_profit * 50}")
    col2.metric("Max Loss", f"rs {max_loss * 50}")

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

