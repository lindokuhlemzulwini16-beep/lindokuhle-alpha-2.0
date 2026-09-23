import streamlit as st, yfinance as yf, time
from datetime import datetime
st.set_page_config(page_title="ALPHA 2.0 PRO", layout="centered")
st.title("🦁 LINDOKUHLE ALPHA 2.0 PRO MAX")
st.caption("Profit Filter + Anti-Excess")

# Risk
max_trades = st.sidebar.slider("Max trades/day",1,5,2)
cool = st.sidebar.slider("Cooldown min",30,180,60)
pairs_map={"GOLD":"GC=F","EURUSD":"EURUSD=X","GBPUSD":"GBPUSD=X","BTCUSD":"BTC-USD"}
pairs=st.multiselect("Pairs",list(pairs_map.keys()),default=["GOLD"])
lot=st.number_input("Lot",0.05)

if 'count' not in st.session_state:
    st.session_state.count=0
    st.session_state.last=None

def get_sig(sym):
    try:
        df=yf.download(sym,period="2d",interval="15m",progress=False)
        if len(df)<30: return None
        close=df['Close'].iloc[-1]
        hi=df['High'].iloc[-20:-1].max()
        lo=df['Low'].iloc[-20:-1].min()
        if close>float(hi):
            return {"action":"BUY","entry":float(close),"sl":float(lo),"tp":float(close+(close-lo)*1.5)}
        if close<float(lo):
            return {"action":"SELL","entry":
