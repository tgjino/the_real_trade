import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import time
# ലേഔട്ട് സെറ്റിംഗ്സ്
st.set_page_config(page_title="The Real Trade", layout="wide")
st.markdown("<h1 style='text-align: center;'>THE REAL TRADE</h1>", unsafe_allow_html =True)
st.divider()

# സൈഡ് ബാർ
auto_update = st.sidebar.toggle('Enable Auto Update (10s)')
st.sidebar.title("Trading Settings")
strategy = st.sidebar.selectbox("Select Strategy", ["Nifty Calculation", "Jade Lizard", "Iron Condor"])

def get_live_nifty():
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period="1d")
        if not data.empty:
            current = round(data['Close'].iloc[-1], 2)
            openPrice = round(data['Open'].iloc[-1], 2)
            high = round(data['High'].max(), 2)
            low = round(data['Low'].min(), 2)
            return current, low, high, openPrice
    except:
        return 0.0, 0.0, 0.0

def render_price_ui(current, openPrice):
    if current > 0:
    openCurrent_diff = round(current-openPrice,2)
        # 2. കണ്ടീഷൻ അനുസരിച്ച് കളറും ചിഹ്നവും നിശ്ചയിക്കുന്നു
        if openCurrent_diff >= 0:
            color = "green"
            icon = "▲" # മുകളിലോട്ട്
        else:
            color = "red"
            icon = "▼" # താഴോട്ട്if openCurrent_diff>=0:

        st.markdown(
            f"### Nifty 50 Market Today 📈 : <span style='color:{color}'>{current}({icon}{openCurrent_diff})</span>",unsafe_allow_html=True) 

current, low, high,openPrice = get_live_nifty()

@st.fragment(run_every="10s")
def display_live_price():
    current, low, high,openPrice = get_live_nifty()
    render_price_ui(current,openPrice)

if auto_update:
    display_live_price()
else:
    render_price_ui(current, openPrice)

# st.sidebar.metric("Nifrty 50 Live", live_price)
    # fig_range = go.Figure(go.Indicator(
    # mode = "gauge+number",
    # value = current,
    # domain = {'x': [0,1], 'y': [0,1]},
    # gauge = {
    # 'axis':{'range': [low, high], 'tickwidth':1},
    # 'bar': {'color': "#00eeff"},
    # 'steps':[{'range':[low, high], 'color':"rgba(255, 255, 255, 0.1)"}],
    # 'threshold':{
    # 'line':{'color':"yellow", 'width': 4},
    # 'thickness': 0.75,
    # 'value': current}}))

    # fig_range.update_layout(
    # height=250,
    # margin= dict(l=50, r=50, t=30, b=30),
    # template="plotly_dark"
    # )

    # st.plotly_chart(fig_range, use_container_width = True)
    st.markdown("""<style>[data-testid="stMetricLabel"] {font-size: 14px;}[data-testid="stMetricValue"]{font-size: 20px; /* വാല്യൂവിന്റെ സൈസ് */}</style>""", unsafe_allow_html=True)

    col_o,col_h, col_l =st.columns(3)
    col_o.metric("Open", f"{openPrice}")
    col_h.metric("high", f"{high}")
    col_l.metric("Low", f"{low}")

    st.divider()


# auto_update = st.sidebar.toggle('Enabel Auto Update (10s)')

# if auto_update:
#     time.sleep(10)
#     st.rerun()
    
# def auto_refresh():
#     while True:
#         current_price = get_live_nifty()
#         st.sidebar.metric("Nifty 50 Live", current_price)
#         time.sleep(10)
#         st.rerun()


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
if current > 0:
    fig.add_vline(
        x=current,
        line_dash="dash",
        line_color="yellow",
        annotation_text=f"LTP: {current}",
        annotation_position ="top left"
    )
st.plotly_chart(fig, use_container_width=True)

