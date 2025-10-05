"""
Cryptocurrency Tracker
A Python application to track cryptocurrency prices in real-time - Jetur Gavli
"""

import requests
import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Dict, List, Optional


class CryptoTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cryptocurrency Tracker - JETRock Program")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        self.api_url = "https://api.coingecko.com/api/v3"
        self.coins_list_url = f"{self.api_url}/coins/list"
        self.price_url = f"{self.api_url}/simple/price"
        
        self.tracked_coins = [
            "bitcoin", "ethereum", "binancecoin", "cardano", 
            "solana", "polkadot", "dogecoin", "chainlink"
        ]
        
        self.price_data = {}
        self.update_interval = 30  
        
        self.setup_ui()
        self.load_initial_data()
        
    def setup_ui(self):
        """Setup the user interface"""
        title_label = tk.Label(
            self.root, 
            text="🚀 Cryptocurrency Tracker (USD & INR) - JETRock Program", 
            font=("Arial", 20, "bold"),
            fg="#00ff88",
            bg='#1e1e1e'
        )
        title_label.pack(pady=10)
        
        control_frame = tk.Frame(self.root, bg='#1e1e1e')
        control_frame.pack(pady=10)
        
        self.add_coin_frame = tk.Frame(control_frame, bg='#1e1e1e')
        self.add_coin_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(self.add_coin_frame, text="Add Coin:", fg="white", bg='#1e1e1e').pack(side=tk.LEFT)
        self.coin_entry = tk.Entry(self.add_coin_frame, width=15)
        self.coin_entry.pack(side=tk.LEFT, padx=5)
        
        add_btn = tk.Button(
            self.add_coin_frame, 
            text="Add", 
            command=self.add_coin,
            bg="#00ff88",
            fg="black",
            font=("Arial", 10, "bold")
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            control_frame, 
            text="🔄 Refresh", 
            command=self.refresh_prices,
            bg="#ff6b35",
            fg="white",
            font=("Arial", 10, "bold")
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        self.auto_refresh_var = tk.BooleanVar()
        auto_refresh_cb = tk.Checkbutton(
            control_frame,
            text="Auto Refresh (30s)",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh,
            fg="white",
            bg='#1e1e1e',
            selectcolor='#00ff88'
        )
        auto_refresh_cb.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(
            self.root, 
            text="Ready to track cryptocurrencies", 
            fg="#ffd700",
            bg='#1e1e1e',
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)
        
        price_frame = tk.Frame(self.root, bg='#1e1e1e')
        price_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("Coin", "Symbol", "Price (USD)", "Price (INR)", "24h Change", "Market Cap", "Last Updated")
        self.price_tree = ttk.Treeview(price_frame, columns=columns, show="headings", height=15)
        
        self.price_tree.heading("Coin", text="Cryptocurrency")
        self.price_tree.heading("Symbol", text="Symbol")
        self.price_tree.heading("Price (USD)", text="Price (USD)")
        self.price_tree.heading("Price (INR)", text="Price (INR)")
        self.price_tree.heading("24h Change", text="24h Change")
        self.price_tree.heading("Market Cap", text="Market Cap")
        self.price_tree.heading("Last Updated", text="Last Updated")
        
        self.price_tree.column("Coin", width=120)
        self.price_tree.column("Symbol", width=80)
        self.price_tree.column("Price (USD)", width=120)
        self.price_tree.column("Price (INR)", width=120)
        self.price_tree.column("24h Change", width=100)
        self.price_tree.column("Market Cap", width=150)
        self.price_tree.column("Last Updated", width=120)
        
        scrollbar = ttk.Scrollbar(price_frame, orient=tk.VERTICAL, command=self.price_tree.yview)
        self.price_tree.configure(yscrollcommand=scrollbar.set)
        
        self.price_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        bottom_frame = tk.Frame(self.root, bg='#1e1e1e')
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            bottom_frame, 
            text="💼 Portfolio Value", 
            font=("Arial", 12, "bold"),
            fg="#00ff88",
            bg='#1e1e1e'
        ).pack()
        
        self.portfolio_label = tk.Label(
            bottom_frame, 
            text="Portfolio: $0.00", 
            fg="white",
            bg='#1e1e1e',
            font=("Arial", 10)
        )
        self.portfolio_label.pack()
        
    def get_coin_data(self, coin_id: str) -> Optional[Dict]:
        try:
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd,inr',
                'include_market_cap': 'true',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(self.price_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if coin_id in data:
                return data[coin_id]
            return None
            
        except requests.exceptions.RequestException as e:
            self.status_label.config(text=f"Error fetching data: {str(e)}")
            return None
        except Exception as e:
            self.status_label.config(text=f"Unexpected error: {str(e)}")
            return None
    
    def get_coin_info(self, coin_id: str) -> Optional[Dict]:
        try:
            url = f"{self.api_url}/coins/{coin_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return None
    
    def format_price(self, price: float, currency: str = "USD") -> str:
        if currency == "USD":
            if price >= 1:
                return f"${price:,.2f}"
            else:
                return f"${price:.6f}"
        elif currency == "INR":
            if price >= 1:
                return f"₹{price:,.2f}"
            else:
                return f"₹{price:.6f}"
        return f"{price:,.2f}"
    
    def format_market_cap(self, market_cap: float) -> str:
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.2f}M"
        else:
            return f"${market_cap:,.0f}"
    
    def format_change(self, change: float) -> str:
        if change >= 0:
            return f"+{change:.2f}%"
        else:
            return f"{change:.2f}%"
    
    def update_price_display(self):
        for item in self.price_tree.get_children():
            self.price_tree.delete(item)
        
        for coin_id in self.tracked_coins:
            price_data = self.get_coin_data(coin_id)
            if price_data:
                coin_info = self.get_coin_info(coin_id)
                symbol = coin_info.get('symbol', coin_id.upper()) if coin_info else coin_id.upper()
                name = coin_info.get('name', coin_id.title()) if coin_info else coin_id.title()
                
                usd_price = price_data.get('usd', 0)
                inr_price = price_data.get('inr', 0)
                change = price_data.get('usd_24h_change', 0)
                market_cap = price_data.get('usd_market_cap', 0)
                
                item_id = self.price_tree.insert("", tk.END, values=(
                    name,
                    symbol.upper(),
                    self.format_price(usd_price, "USD"),
                    self.format_price(inr_price, "INR"),
                    self.format_change(change),
                    self.format_market_cap(market_cap),
                    datetime.now().strftime("%H:%M:%S")
                ))
                
                if change >= 0:
                    self.price_tree.set(item_id, "24h Change", f"🟢 +{change:.2f}%")
                else:
                    self.price_tree.set(item_id, "24h Change", f"🔴 {change:.2f}%")
        
        self.status_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def load_initial_data(self):
        self.status_label.config(text="Loading cryptocurrency data...")
        self.update_price_display()
        self.status_label.config(text="Data loaded successfully!")
    
    def refresh_prices(self):
        def refresh_thread():
            self.status_label.config(text="Refreshing prices...")
            self.update_price_display()
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def add_coin(self):
        coin_id = self.coin_entry.get().strip().lower()
        if not coin_id:
            messagebox.showerror("Error", "Please enter a cryptocurrency ID")
            return
        
        coin_data = self.get_coin_data(coin_id)
        if coin_data:
            if coin_id not in self.tracked_coins:
                self.tracked_coins.append(coin_id)
                self.coin_entry.delete(0, tk.END)
                self.update_price_display()
                messagebox.showinfo("Success", f"Added {coin_id} to tracking list")
            else:
                messagebox.showwarning("Warning", f"{coin_id} is already being tracked")
        else:
            messagebox.showerror("Error", f"Could not find cryptocurrency: {coin_id}")
    
    def toggle_auto_refresh(self):
        if self.auto_refresh_var.get():
            self.start_auto_refresh()
        else:
            self.stop_auto_refresh()
    
    def start_auto_refresh(self):
        def auto_refresh():
            while self.auto_refresh_var.get():
                time.sleep(self.update_interval)
                if self.auto_refresh_var.get():
                    self.refresh_prices()
        
        self.auto_refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
        self.auto_refresh_thread.start()
    
    def stop_auto_refresh(self):
        pass
    
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application closed by user")


def main():
    print("🚀 Starting JETRock Cryptocurrency Tracker...")
    print("Features:")
    print("  - Real-time cryptocurrency prices")
    print("  - 24-hour price changes")
    print("  - Market cap information")
    print("  - Add custom cryptocurrencies")
    print("  - Auto-refresh functionality")
    print("  - Modern dark theme UI")
    print("\nPress Ctrl+C to exit")
    
    try:
        app = CryptoTracker()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Make sure you have an internet connection and required packages installed.")


if __name__ == "__main__":
    main()
