import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, date
import time
import numpy as np
import plotly.graph_objects as go

# --- Cache Configuration ---
stock_detail_cache = {}
CACHE_TTL_SECONDS = 15 * 60  # 15 minutes

# --- Configuration ---
NIFTY50_TICKERS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
    "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LTIM.NS",
    "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS",
    "TATAMOTORS.NS", "TCS.NS", "TATASTEEL.NS", "TECHM.NS", "TITAN.NS",
    "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS", "VOLTAS.NS"
]

SHORT_WINDOW = 20
LONG_WINDOW = 50
HISTORY_PERIOD_DAYS = max(LONG_WINDOW, SHORT_WINDOW) * 3 + 90

# --- DMA Signal Nuance Parameters ---
RECENT_CROSSOVER_DAYS = 5
MA_SPREAD_STRONG_THRESHOLD = 0.015
MA_SPREAD_NEUTRAL_THRESHOLD = 0.005


# --- Helper function to process financial statement DataFrames ---
def format_financial_statement(df):
    if df is None or df.empty:
        return None
    try:
        df_transposed = df.transpose().reset_index()
        if 'index' in df_transposed.columns:
            df_transposed = df_transposed.rename(columns={'index': 'Period'})
        elif df_transposed.columns[0] != 'Period':
            df_transposed = df_transposed.rename(columns={df_transposed.columns[0]: 'Period'})

        if pd.api.types.is_datetime64_any_dtype(df_transposed['Period']):
            df_transposed['Period'] = df_transposed['Period'].dt.strftime('%Y-%m-%d')
        else:
            df_transposed['Period'] = df_transposed['Period'].astype(str).str.split(' ').str[0]

        for col in df_transposed.columns:
            if col != 'Period':
                df_transposed[col] = pd.to_numeric(df_transposed[col], errors='coerce')

        df_processed = df_transposed.replace({np.nan: None, pd.NaT: None})
        return df_processed.to_dict(orient='records')
    except Exception as e:
        print(f"Error formatting financial statement: {e}")
        import traceback
        traceback.print_exc()
        return None


# --- Helper Function to Get Stock Data and DMA Signal ---
@st.cache_data(ttl=CACHE_TTL_SECONDS)
def get_stock_data_and_signal(ticker_symbol):
    print(f"Processing {ticker_symbol} for nuanced signal...")
    try:
        stock = yf.Ticker(ticker_symbol)
        hist_data_end = datetime.now()
        hist_data_start = hist_data_end - timedelta(days=HISTORY_PERIOD_DAYS + 60)
        hist_df = stock.history(start=hist_data_start.strftime('%Y-%m-%d'),
                                end=hist_data_end.strftime('%Y-%m-%d'),
                                interval="1d")

        if hist_df.empty or len(hist_df) < LONG_WINDOW:
            print(f"  WARN: Not enough historical data for {ticker_symbol} (got {len(hist_df)}, need {LONG_WINDOW}).")
            try:
                info = stock.info
                return {
                    "ticker": ticker_symbol, "name": info.get('shortName', ticker_symbol),
                    "cmp": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                    "dayChangePercent": (info.get('regularMarketChangePercent', 0)) * 100,
                    "dayChangeAbs": info.get('regularMarketChange', 0), "volume": info.get('volume', 0),
                    "dmaSignal": "N/A (Data)", "lastSignalDate": None, "smaShort": None, "smaLong": None,
                }
            except Exception:
                return None

        hist_df[f'SMA_{SHORT_WINDOW}'] = hist_df['Close'].rolling(window=SHORT_WINDOW, min_periods=1).mean()
        hist_df[f'SMA_{LONG_WINDOW}'] = hist_df['Close'].rolling(window=LONG_WINDOW, min_periods=1).mean()
        valid_ma_hist = hist_df.dropna(subset=[f'SMA_{SHORT_WINDOW}', f'SMA_{LONG_WINDOW}'])

        current_signal, date_of_signal, sma_short_latest, sma_long_latest = "N/A (Logic)", None, None, None

        if len(valid_ma_hist) < 2:
            if len(valid_ma_hist) == 1:
                sma_short_latest, sma_long_latest = valid_ma_hist.iloc[-1][f'SMA_{SHORT_WINDOW}'], \
                                                    valid_ma_hist.iloc[-1][f'SMA_{LONG_WINDOW}']
                current_signal = "INITIAL"
        else:
            sma_short_col, sma_long_col = f'SMA_{SHORT_WINDOW}', f'SMA_{LONG_WINDOW}'
            hist_with_signals = valid_ma_hist.copy()
            hist_with_signals['BuyCrossover'] = (hist_with_signals[sma_short_col] > hist_with_signals[
                sma_long_col]) & (hist_with_signals[sma_short_col].shift(1) <= hist_with_signals[
                sma_long_col].shift(1))
            hist_with_signals['SellCrossover'] = (hist_with_signals[sma_short_col] < hist_with_signals[
                sma_long_col]) & (hist_with_signals[sma_short_col].shift(1) >= hist_with_signals[
                sma_long_col].shift(1))
            last_buy_event_date = hist_with_signals[hist_with_signals['BuyCrossover']].index.max() if not \
            hist_with_signals[hist_with_signals['BuyCrossover']].empty else pd.NaT
            last_sell_event_date = hist_with_signals[hist_with_signals['SellCrossover']].index.max() if not \
            hist_with_signals[hist_with_signals['SellCrossover']].empty else pd.NaT
            sma_short_latest, sma_long_latest = valid_ma_hist.iloc[-1][sma_short_col], valid_ma_hist.iloc[-1][
                sma_long_col]
            days_since_last_buy = (date.today() - last_buy_event_date.date()).days if pd.notna(
                last_buy_event_date) else float('inf')
            days_since_last_sell = (date.today() - last_sell_event_date.date()).days if pd.notna(
                last_sell_event_date) else float('inf')
            ma_spread = (sma_short_latest - sma_long_latest) / sma_long_latest if sma_long_latest != 0 and pd.notna(
                sma_long_latest) else 0

            if pd.notna(sma_short_latest) and pd.notna(sma_long_latest):
                if sma_short_latest > sma_long_latest:
                    date_of_signal = last_buy_event_date.strftime('%Y-%m-%d') if pd.notna(last_buy_event_date) else None
                    if pd.notna(last_buy_event_date) and (
                            pd.isna(last_sell_event_date) or last_buy_event_date > last_sell_event_date):
                        if days_since_last_buy <= RECENT_CROSSOVER_DAYS and ma_spread >= MA_SPREAD_STRONG_THRESHOLD:
                            current_signal = "STRONG BUY"
                        elif days_since_last_buy <= RECENT_CROSSOVER_DAYS:
                            current_signal = "RECENT BUY"
                        else:
                            current_signal = "BUY (Uptrend)"
                    else:
                        current_signal, date_of_signal = "POTENTIAL BUY / RECOVERY", None
                elif sma_short_latest < sma_long_latest:
                    date_of_signal = last_sell_event_date.strftime('%Y-%m-%d') if pd.notna(
                        last_sell_event_date) else None
                    if pd.notna(last_sell_event_date) and (
                            pd.isna(last_buy_event_date) or last_sell_event_date > last_buy_event_date):
                        if days_since_last_sell <= RECENT_CROSSOVER_DAYS and abs(
                                ma_spread) >= MA_SPREAD_STRONG_THRESHOLD:
                            current_signal = "STRONG SELL"
                        elif days_since_last_sell <= RECENT_CROSSOVER_DAYS:
                            current_signal = "RECENT SELL"
                        else:
                            current_signal = "SELL (Downtrend)"
                    else:
                        current_signal, date_of_signal = "POTENTIAL SELL / DECLINE", None
                else:
                    current_signal = "NEUTRAL / SIDEWAYS"
                    if pd.notna(last_buy_event_date) and pd.notna(last_sell_event_date):
                        date_of_signal = max(last_buy_event_date, last_sell_event_date).strftime('%Y-%m-%d')
                    elif pd.notna(last_buy_event_date):
                        date_of_signal = last_buy_event_date.strftime('%Y-%m-%d')
                    elif pd.notna(last_sell_event_date):
                        date_of_signal = last_sell_event_date.strftime('%Y-%m-%d')
                if abs(ma_spread) < MA_SPREAD_NEUTRAL_THRESHOLD and not (
                        current_signal in ["STRONG BUY", "STRONG SELL"] and (
                        days_since_last_buy <= RECENT_CROSSOVER_DAYS or days_since_last_sell <= RECENT_CROSSOVER_DAYS)):
                    current_signal = "NEUTRAL / SIDEWAYS"
                    if pd.notna(last_buy_event_date) and pd.notna(last_sell_event_date):
                        date_of_signal = max(last_buy_event_date, last_sell_event_date).strftime('%Y-%m-%d')
                    elif pd.notna(last_buy_event_date):
                        date_of_signal = last_buy_event_date.strftime('%Y-%m-%d')
                    elif pd.notna(last_sell_event_date):
                        date_of_signal = last_sell_event_date.strftime('%Y-%m-%d')
            else:
                current_signal, date_of_signal = "N/A (Logic)", None
            if current_signal == "N/A (Logic)" and pd.notna(sma_short_latest) and pd.notna(sma_long_latest):
                if sma_short_latest > sma_long_latest:
                    current_signal = "BUY (Trend)"
                elif sma_short_latest < sma_long_latest:
                    current_signal = "SELL (Trend)"
                else:
                    current_signal = "NEUTRAL"

        latest_close_price, stock_name, cmp, day_change_abs, day_change_percent, current_volume = \
        hist_df.iloc[-1]['Close'] if not hist_df.empty else np.nan, ticker_symbol, hist_df.iloc[-1][
            'Close'] if not hist_df.empty else np.nan, 0.0, 0.0, \
        hist_df.iloc[-1]['Volume'] if not hist_df.empty and 'Volume' in hist_df.columns else 0
        try:
            info = stock.info
            stock_name, cmp, prev_close = info.get('shortName', ticker_symbol), info.get('currentPrice', info.get(
                'regularMarketPrice', latest_close_price)), info.get('previousClose')
            if pd.notna(prev_close) and pd.notna(cmp) and prev_close != 0: day_change_abs, day_change_percent = cmp - prev_close, (
                                                                                                                                     (
                                                                                                                                                 cmp - prev_close) / prev_close) * 100
            vol_info = info.get('volume', info.get('regularMarketVolume'))
            current_volume = int(vol_info) if pd.notna(vol_info) else (
                int(current_volume) if pd.notna(current_volume) else 0)
        except Exception as e_info:
            print(f"  WARN: Could not fetch detailed stock.info for {ticker_symbol}. Using historical. Error: {e_info}")
            if len(hist_df) >= 2: day_change_abs, prev_close_for_calc = hist_df.iloc[-1]['Close'] - \
                                                                        hist_df.iloc[-2]['Close'], hist_df.iloc[-2][
                                                                            'Close']; day_change_percent = ((
                                                                                                                        day_change_abs / prev_close_for_calc) * 100) if pd.notna(
                prev_close_for_calc) and prev_close_for_calc != 0 else 0.0
        return {"ticker": ticker_symbol, "name": stock_name, "cmp": round(cmp, 2) if pd.notna(cmp) else None,
                "dayChangePercent": round(day_change_percent, 2) if pd.notna(day_change_percent) else None,
                "dayChangeAbs": round(day_change_abs, 2) if pd.notna(day_change_abs) else None,
                "volume": int(current_volume) if pd.notna(current_volume) else None, "dmaSignal": current_signal,
                "lastSignalDate": date_of_signal,
                "smaShort": round(sma_short_latest, 2) if pd.notna(sma_short_latest) else None,
                "smaLong": round(sma_long_latest, 2) if pd.notna(sma_long_latest) else None}
    except Exception as e_main:
        print(f"  ERROR: Main processing in get_stock_data_and_signal for {ticker_symbol}: {str(e_main)}");
        import traceback;
        traceback.print_exc();
        return None


# --- Helper for Quick Info ---
@st.cache_data(ttl=60)
def get_stock_quick_info(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        cmp = info.get('currentPrice', info.get('regularMarketPrice'))
        prev_close = info.get('previousClose')
        day_change_abs = None
        day_change_percent = None
        if pd.notna(cmp) and pd.notna(prev_close) and prev_close != 0:
            day_change_abs = cmp - prev_close
            day_change_percent = (day_change_abs / prev_close) * 100

        volume = info.get('volume', info.get('regularMarketVolume', 0))
        return {
            "ticker": ticker_symbol,
            "name": info.get('shortName', ticker_symbol),
            "cmp": round(cmp, 2) if pd.notna(cmp) else None,
            "dayChangePercent": round(day_change_percent, 2) if pd.notna(day_change_percent) else None,
            "dayChangeAbs": round(day_change_abs, 2) if pd.notna(day_change_abs) else None,
            "volume": int(volume) if pd.notna(volume) else None
        }
    except Exception as e:
        print(f"  ERROR fetching quick info for {ticker_symbol}: {str(e)}")
        return {"ticker": ticker_symbol, "name": ticker_symbol.replace(".NS", ""), "cmp": None,
                "dayChangePercent": None, "dayChangeAbs": None, "volume": None, "error": True,
                "errorMessage": str(e)}


# --- UPDATED Stock Detail Function ---
@st.cache_data(ttl=CACHE_TTL_SECONDS)
def get_stock_detail(ticker_symbol, force_refresh=False):
    print(f"\n--- Requesting EXTENDED detail for {ticker_symbol} ---")

    base_stock_data = get_stock_data_and_signal(ticker_symbol)
    if not base_stock_data:
        try:
            stock_obj_fallback = yf.Ticker(ticker_symbol)
            info_fallback = stock_obj_fallback.info
            if info_fallback:
                print("  WARN: Base signal calc failed, returning only very basic info from fallback.")
                return {
                    "info": {"ticker": ticker_symbol, "name": info_fallback.get('shortName', ticker_symbol),
                             "error": "Signal/History Fetch Failed"},
                    "currentMarketData": {"cmp": info_fallback.get('currentPrice')},
                    "currentDma": {"signal": "N/A (Error)"},
                    "historicalData": [], "dmaSignalsHistorical": [], "financialStatements": {}, "news": []
                }
            else:
                return {"error": f"Could not fetch any data for {ticker_symbol}"}
        except Exception as fallback_e:
            print(f"  ERROR: Fallback info fetch also failed for {ticker_symbol}: {fallback_e}")
            return {"error": f"Could not fetch any data for {ticker_symbol}"}

    stock_obj = yf.Ticker(ticker_symbol)
    stock_info_obj = {}
    financials_annual, financials_quarterly, balance_sheet_annual, balance_sheet_quarterly, cash_flow_annual, cash_flow_quarterly = None, None, None, None, None, None
    news_data_list = []  # Initialize here
    historical_data_for_chart, dma_signals_historical = [], []  # Initialize here

    try:  # Main try for yfinance object data (info, financials)
        stock_info_obj = stock_obj.info
        if not stock_info_obj:
            print(f"  WARN: stock.info was empty for {ticker_symbol}.")
            stock_info_obj = {}

        # Fetch financial statements
        try:
            financials_annual = format_financial_statement(stock_obj.financials)
            financials_quarterly = format_financial_statement(stock_obj.quarterly_financials)
            balance_sheet_annual = format_financial_statement(stock_obj.balance_sheet)
            balance_sheet_quarterly = format_financial_statement(stock_obj.quarterly_balance_sheet)
            cash_flow_annual = format_financial_statement(stock_obj.cashflow)
            cash_flow_quarterly = format_financial_statement(stock_obj.quarterly_cashflow)
        except Exception as e_fin:
            print(f"  WARN: Error fetching one or more financial statements for {ticker_symbol}: {e_fin}")

    except Exception as e_yf_main:
        print(f"  ERROR: Major error fetching yfinance object data (info/financials) for {ticker_symbol}: {e_yf_main}")
        if not isinstance(stock_info_obj, dict): stock_info_obj = {}  # Ensure it's a dict

    # Fetch Historical data for chart
    try:
        hist_data_end_detail = datetime.now()
        hist_data_start_detail = hist_data_end_detail - timedelta(days=365 * 2 + 60)
        detailed_hist_df = stock_obj.history(start=hist_data_start_detail.strftime('%Y-%m-%d'),
                                             end=hist_data_end_detail.strftime('%Y-%m-%d'),
                                             interval="1d")

        if not detailed_hist_df.empty:
            detailed_hist_df[f'SMA_{SHORT_WINDOW}'] = detailed_hist_df['Close'].rolling(window=SHORT_WINDOW,
                                                                                       min_periods=1).mean()
            detailed_hist_df[f'SMA_{LONG_WINDOW}'] = detailed_hist_df['Close'].rolling(window=LONG_WINDOW,
                                                                                      min_periods=1).mean()

            for index, row in detailed_hist_df.iterrows():
                historical_data_for_chart.append({
                    "time": index.strftime('%Y-%m-%d'),
                    "open": round(row['Open'], 2) if pd.notna(row['Open']) else None,
                    "high": round(row['High'], 2) if pd.notna(row['High']) else None,
                    "low": round(row['Low'], 2) if pd.notna(row['Low']) else None,
                    "close": round(row['Close'], 2) if pd.notna(row['Close']) else None,
                    "volume": int(row['Volume']) if pd.notna(row['Volume']) else None,
                    "smaShort": round(row.get(f'SMA_{SHORT_WINDOW}'), 2) if pd.notna(
                        row.get(f'SMA_{SHORT_WINDOW}')) else None,
                    "smaLong": round(row.get(f'SMA_{LONG_WINDOW}'), 2) if pd.notna(
                        row.get(f'SMA_{LONG_WINDOW}')) else None,
                })

            if len(detailed_hist_df) > 1:
                sma_short_col_detail, sma_long_col_detail = f'SMA_{SHORT_WINDOW}', f'SMA_{LONG_WINDOW}'
                if sma_short_col_detail in detailed_hist_df.columns and sma_long_col_detail in detailed_hist_df.columns:  # Ensure columns exist
                    chart_hist_df = detailed_hist_df[[sma_short_col_detail, sma_long_col_detail, 'Close']].copy()
                    chart_hist_df = chart_hist_df.dropna(subset=[sma_short_col_detail, sma_long_col_detail])
                    if len(chart_hist_df) > 1:
                        chart_hist_df['BuyCrossover'] = (chart_hist_df[sma_short_col_detail] > chart_hist_df[
                            sma_long_col_detail]) & (chart_hist_df[sma_short_col_detail].shift(1) <=
                                                     chart_hist_df[sma_long_col_detail].shift(1))
                        chart_hist_df['SellCrossover'] = (chart_hist_df[sma_short_col_detail] < chart_hist_df[
                            sma_long_col_detail]) & (chart_hist_df[sma_short_col_detail].shift(1) >=
                                                      chart_hist_df[sma_long_col_detail].shift(1))
                        for index, row_data in chart_hist_df[chart_hist_df['BuyCrossover']].iterrows():
                            dma_signals_historical.append(
                                {"time": index.strftime('%Y-%m-%d'), "type": "BUY", "priceAtSignal": round(
                                    row_data['Close'], 2) if pd.notna(row_data['Close']) else None})
                        for index, row_data in chart_hist_df[chart_hist_df['SellCrossover']].iterrows():
                            dma_signals_historical.append(
                                {"time": index.strftime('%Y-%m-%d'), "type": "SELL", "priceAtSignal": round(
                                    row_data['Close'], 2) if pd.notna(row_data['Close']) else None})
                        dma_signals_historical.sort(key=lambda x: x['time'])
    except Exception as e_hist:
        print(f"  ERROR: Could not fetch/process historical chart data for {ticker_symbol}: {e_hist}")

    # --- Construct the Final Payload ---
    detail_payload = {
        "info": {
            "ticker": base_stock_data.get("ticker", ticker_symbol),
            "name": base_stock_data.get("name", stock_info_obj.get('shortName', ticker_symbol)),
            "sector": stock_info_obj.get('sector'), "industry": stock_info_obj.get('industry'),
            "longBusinessSummary": stock_info_obj.get('longBusinessSummary'),
            "website": stock_info_obj.get('website'), "address1": stock_info_obj.get('address1'),
            "city": stock_info_obj.get('city'), "country": stock_info_obj.get('country'),
            "fullTimeEmployees": stock_info_obj.get('fullTimeEmployees'),
            "marketCap": stock_info_obj.get('marketCap'), "enterpriseValue": stock_info_obj.get('enterpriseValue'),
            "beta": stock_info_obj.get('beta'), "trailingPE": stock_info_obj.get('trailingPE'),
            "forwardPE": stock_info_obj.get('forwardPE'), "pegRatio": stock_info_obj.get('pegRatio'),
            "priceToBook": stock_info_obj.get('priceToBook'),
            "enterpriseToRevenue": stock_info_obj.get('enterpriseToRevenue'),
            "enterpriseToEbitda": stock_info_obj.get('enterpriseToEbitda'),
            "bookValue": stock_info_obj.get('bookValue'), "dividendRate": stock_info_obj.get('dividendRate'),
            "dividendYield": stock_info_obj.get('dividendYield'),
            "payoutRatio": stock_info_obj.get('payoutRatio'),
            "fiveYearAvgDividendYield": stock_info_obj.get('fiveYearAvgDividendYield'),
            "exDividendDate": datetime.fromtimestamp(stock_info_obj['exDividendDate']).strftime(
                '%Y-%m-%d') if stock_info_obj.get('exDividendDate') else None,
            "profitMargins": stock_info_obj.get('profitMargins'),
            "grossMargins": stock_info_obj.get('grossMargins'),
            "ebitdaMargins": stock_info_obj.get('ebitdaMargins'),
            "operatingMargins": stock_info_obj.get('operatingMargins'),
            "returnOnAssets": stock_info_obj.get('returnOnAssets'),
            "returnOnEquity": stock_info_obj.get('returnOnEquity'),
            "debtToEquity": stock_info_obj.get('debtToEquity'),
            "quickRatio": stock_info_obj.get('quickRatio'), "currentRatio": stock_info_obj.get('currentRatio'),
            "totalCash": stock_info_obj.get('totalCash'), "totalDebt": stock_info_obj.get('totalDebt'),
            "revenueGrowth": stock_info_obj.get('revenueGrowth'),
            "earningsQuarterlyGrowth": stock_info_obj.get('earningsQuarterlyGrowth'),
            "sharesOutstanding": stock_info_obj.get('sharesOutstanding'),
            "floatShares": stock_info_obj.get('floatShares'),
            "heldPercentInsiders": stock_info_obj.get('heldPercentInsiders'),
            "heldPercentInstitutions": stock_info_obj.get('heldPercentInstitutions'),
            "targetMeanPrice": stock_info_obj.get('targetMeanPrice'),
            "targetHighPrice": stock_info_obj.get('targetHighPrice'),
            "targetLowPrice": stock_info_obj.get('targetLowPrice'),
            "recommendationMean": stock_info_obj.get('recommendationMean'),
            "recommendationKey": stock_info_obj.get('recommendationKey'),
            "numberOfAnalystOpinions": stock_info_obj.get('numberOfAnalystOpinions'),
            "dayHigh": stock_info_obj.get('dayHigh'), "dayLow": stock_info_obj.get('dayLow'),
            "fiftyTwoWeekHigh": stock_info_obj.get('fiftyTwoWeekHigh'),
            "fiftyTwoWeekLow": stock_info_obj.get('fiftyTwoWeekLow'),
            "averageVolume": stock_info_obj.get('averageVolume', stock_info_obj.get('averageDailyVolume10Day')),
        },
        "currentMarketData": {
            "cmp": base_stock_data.get("cmp", stock_info_obj.get('currentPrice')),
            "dayChangePercent": base_stock_data.get("dayChangePercent"),
            "dayChangeAbs": base_stock_data.get("dayChangeAbs"),
            "volume": base_stock_data.get("volume"),
            "openPrice": stock_info_obj.get('open'),
            "previousClosePrice": stock_info_obj.get('previousClose')
        },
        "historicalData": historical_data_for_chart,
        "dmaSignalsHistorical": dma_signals_historical,
        "currentDma": {
            "signal": base_stock_data.get("dmaSignal"),
            "smaShortValue": base_stock_data.get("smaShort"),
            "smaLongValue": base_stock_data.get("smaLong"),
            "lastSignalDate": base_stock_data.get("lastSignalDate")
        },
        "financialStatements": {
            "incomeStatementAnnual": financials_annual,
            "incomeStatementQuarterly": financials_quarterly,
            "balanceSheetAnnual": balance_sheet_annual,
            "balanceSheetQuarterly": balance_sheet_quarterly,
            "cashFlowAnnual": cash_flow_annual,
            "cashFlowQuarterly": cash_flow_quarterly,
        },
        "news": news_data_list
    }

    return detail_payload


def display_stock_price_chart(price_data, sma_short_data, sma_long_data, volume_data, signal_markers):
    df = pd.DataFrame(price_data)
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')

    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='Price'))

    # Volume
    colors = ['green' if row['close'] >= row['open'] else 'red' for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index, y=df['volume'], name='Volume', marker_color=colors, yaxis='y2'))

    # SMAs
    fig.add_trace(
        go.Scatter(x=df.index, y=df['smaShort'], mode='lines', name=f'SMA {SHORT_WINDOW}', line=dict(color='orange')))
    fig.add_trace(
        go.Scatter(x=df.index, y=df['smaLong'], mode='lines', name=f'SMA {LONG_WINDOW}', line=dict(color='blue')))

    # Signal Markers
    buy_signals = [s for s in signal_markers if s['type'] == 'BUY']
    sell_signals = [s for s in signal_markers if s['type'] == 'SELL']

    if buy_signals:
        buy_df = pd.DataFrame(buy_signals)
        buy_df['time'] = pd.to_datetime(buy_df['time'])
        fig.add_trace(go.Scatter(x=buy_df['time'], y=buy_df['priceAtSignal'], mode='markers', name='Buy Signal',
                                 marker=dict(color='green', size=10, symbol='triangle-up')))

    if sell_signals:
        sell_df = pd.DataFrame(sell_signals)
        sell_df['time'] = pd.to_datetime(sell_df['time'])
        fig.add_trace(go.Scatter(x=sell_df['time'], y=sell_df['priceAtSignal'], mode='markers', name='Sell Signal',
                                  marker=dict(color='red', size=10, symbol='triangle-down')))

    fig.update_layout(
        title='Stock Price, SMAs & Volume',
        yaxis_title='Price',
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right'
        ),
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(page_title="Nifty DMA Analyzer", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Stock Detail"])

    if page == "Dashboard":
        st.title("Nifty 50 Stock Overview")

        if 'stock_data' not in st.session_state or st.button("Recalculate All"):
            with st.spinner("Fetching all stock data..."):
                st.session_state.stock_data = [get_stock_data_and_signal(ticker) for ticker in NIFTY50_TICKERS]

        if st.button("Refresh Prices"):
            with st.spinner("Refreshing prices..."):
                quick_updates = [get_stock_quick_info(ticker) for ticker in NIFTY50_TICKERS]
                updates_map = {u['ticker']: u for u in quick_updates}
                for i, stock in enumerate(st.session_state.stock_data):
                    if stock and stock['ticker'] in updates_map:
                        update = updates_map[stock['ticker']]
                        st.session_state.stock_data[i]['cmp'] = update['cmp']
                        st.session_state.stock_data[i]['dayChangePercent'] = update['dayChangePercent']
                        st.session_state.stock_data[i]['dayChangeAbs'] = update['dayChangeAbs']
                        st.session_state.stock_data[i]['volume'] = update['volume']

        search_term = st.text_input("Search by Name or Ticker...")
        signal_filter = st.selectbox("Filter by Signal",
                                     ["All Signals"] + sorted(list(set(
                                         [s['dmaSignal'] for s in st.session_state.stock_data if s and s['dmaSignal']]
                                     ))))

        filtered_stocks = st.session_state.stock_data
        if search_term:
            filtered_stocks = [s for s in filtered_stocks if
                               s and (search_term.lower() in s['name'].lower() or search_term.lower() in s[
                                   'ticker'].lower())]
        if signal_filter != "All Signals":
            filtered_stocks = [s for s in filtered_stocks if s and s['dmaSignal'] == signal_filter]

        if filtered_stocks:
            df = pd.DataFrame(filtered_stocks)
            st.dataframe(df)
        else:
            st.write("No stocks to display.")

    elif page == "Stock Detail":
        st.title("Stock Detail Page")
        ticker_symbol = st.selectbox("Select a stock", NIFTY50_TICKERS)

        if ticker_symbol:
            stock_data = get_stock_detail(ticker_symbol)

            if "error" in stock_data:
                st.error(stock_data["error"])
            else:
                info = stock_data['info']
                current_market_data = stock_data['currentMarketData']
                current_dma = stock_data['currentDma']

                st.header(f"{info['name']} ({info['ticker']})")
                st.write(f"{info.get('sector', 'N/A')} - {info.get('industry', 'N/A')}")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Market Snapshot")
                    st.metric(label="CMP", value=f"₹{current_market_data['cmp']:.2f}",
                              delta=f"{current_market_data['dayChangeAbs']:.2f} ({current_market_data['dayChangePercent']:.2f}%)")
                    st.write(f"**Volume:** {current_market_data['volume']:,}")
                    st.write(f"**Open:** {current_market_data.get('openPrice', 'N/A')}")
                    st.write(f"**Previous Close:** {current_market_data.get('previousClosePrice', 'N/A')}")

                with col2:
                    st.subheader("DMA Analysis")
                    st.write(f"**Signal:** {current_dma['signal']}")
                    st.write(f"**Last Crossover:** {current_dma.get('lastSignalDate', 'N/A')}")
                    st.write(f"**SMA {SHORT_WINDOW}D:** {current_dma.get('smaShortValue', 'N/A')}")
                    st.write(f"**SMA {LONG_WINDOW}D:** {current_dma.get('smaLongValue', 'N/A')}")

                display_stock_price_chart(stock_data['historicalData'], stock_data['historicalData'],
                                           stock_data['historicalData'], stock_data['historicalData'],
                                           stock_data['dmaSignalsHistorical'])

                with st.expander("Key Metrics & Ratios"):
                    st.subheader("Valuation")
                    st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                    st.write(f"**Trailing P/E:** {info.get('trailingPE', 'N/A')}")
                    st.write(f"**Forward P/E:** {info.get('forwardPE', 'N/A')}")
                    st.write(f"**Price/Book (P/B):** {info.get('priceToBook', 'N/A')}")

                with st.expander("Financial Statements"):
                    st.subheader("Income Statement (Annual)")
                    if stock_data['financialStatements']['incomeStatementAnnual']:
                        st.dataframe(pd.DataFrame(stock_data['financialStatements']['incomeStatementAnnual']))
                    st.subheader("Balance Sheet (Annual)")
                    if stock_data['financialStatements']['balanceSheetAnnual']:
                        st.dataframe(pd.DataFrame(stock_data['financialStatements']['balanceSheetAnnual']))
                    st.subheader("Cash Flow (Annual)")
                    if stock_data['financialStatements']['cashFlowAnnual']:
                        st.dataframe(pd.DataFrame(stock_data['financialStatements']['cashFlowAnnual']))

                with st.expander("About the Company"):
                    st.write(info.get('longBusinessSummary', 'No summary available.'))


if __name__ == '__main__':
    main()