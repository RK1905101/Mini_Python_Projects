# **Nifty DMA Analyzer (Streamlit Version)**

## **Project Overview**

This is a Streamlit web application designed to analyze stocks from the Nifty 50 index using a Dual Moving Average (DMA) crossover strategy. It provides users with buy/sell/hold signals, detailed stock information, interactive historical price charts, and financial statements, all within a single, easy-to-run app.

This project is a conversion of the original full-stack React and Flask application into a unified Streamlit application.

## **Features**

* **Dashboard View:**  
  * An overview of all Nifty 50 stocks with current market price, day's change, volume, and the current DMA signal.  
  * Search and filter stocks by name/ticker or by the calculated DMA signal.  
  * Buttons to perform a full data recalculation or a quick price-only refresh.  
* **Stock Detail View:**  
  * Comprehensive, detailed information for any selected Nifty 50 stock.  
  * A market snapshot showing the current price, day's range, and volume.  
  * In-depth DMA analysis including the current signal, last crossover date, and SMA values.  
  * An interactive price chart displaying OHLC data, SMAs (20-day & 50-day), volume, and historical Buy/Sell crossover markers.  
  * Expandable sections for Key Financial Metrics, Financial Statements (Income, Balance Sheet, Cash Flow), and the company's business summary.

## **Tech Stack**

* **Python**  
* **Streamlit:** For building the interactive web application.  
* **yfinance:** For fetching stock market data from Yahoo Finance.  
* **Pandas:** For data manipulation and analysis.  
* **Plotly:** For creating interactive charts.  
* **Numpy:** For numerical operations.

## **Setup and Running the Project**

### **Prerequisites**

* Python 3.8+ and Pip installed on your system.  
* Git (optional, for cloning).

### **Instructions**

1. Get the code:  
   Clone the repository or download the streamlit\_app.py and requirements.txt files into a new directory on your local machine.  
2. Create a Virtual Environment:  
   Open your terminal or command prompt, navigate to the project directory, and create a Python virtual environment. This is recommended to keep dependencies isolated.  
   \# For macOS/Linux  
   python3 \-m venv venv

   \# For Windows  
   python \-m venv venv

3. **Activate the Virtual Environment:**  
   \# For macOS/Linux  
   source venv/bin/activate

   \# For Windows  
   .\\venv\\Scripts\\activate

4. Install Dependencies:  
   With your virtual environment active, install all the required Python packages using the requirements.txt file.  
   pip install \-r requirements.txt

5. Run the Streamlit App:  
   Now, you can start the application by running the following command in your terminal:  
   streamlit run streamlit\_app.py

   The application will open automatically in your default web browser. You can navigate between the "Dashboard" and "Stock Detail" pages using the sidebar.