from tkinter import messagebox, ttk
from datetime import datetime, UTC
import tkinter as tk
import requests


class CurrencyConverterApp:
    __INT64_MAX = 2**63 - 1
    __DEFAULT_FROM_CURRENCY = "USD"
    __DEFAULT_TO_CURRENCY = "GEL"
    __ALL_CURRENCIES_URL  = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
    __SINGLE_CURRENCY_URL = __ALL_CURRENCIES_URL.replace('.json', '') + "/{currency_code}.json"
    country_currencies = ['USD', 'CAD', 'EUR', 'AED', 'AFN', 'ALL', 'AMD', 'ARS', 'AUD', 'AZN', 'BAM', 'BDT', 'BGN', 'BHD', 'BIF', 'BND', 'BOB', 'BRL', 'BWP', 'BYN', 'BZD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EEK', 'EGP', 'ERN', 'ETB', 'GBP', 'GEL', 'GHS', 'GNF', 'GTQ', 'HKD', 'HNL', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KHR', 'KMF', 'KRW', 'KWD', 'KZT', 'LBP', 'LKR', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MOP', 'MUR', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SDG', 'SEK', 'SGD', 'SOS', 'SYP', 'THB', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VEF', 'VND', 'XAF', 'XOF', 'YER', 'ZAR', 'ZMK', 'ZWL']

    def __init__(self, width: int = 600, height: int = 400, cache_validity_seconds: int = 3600) -> None:
        """
        Initializes the CurrencyConverter object.
        არგუმენტები:
            width: ფანჯრის სიგანე. Default მნიშველობა 600.
            height: ფანჯრის სიმაღლე. Default მნიშველობა 400.
            cache_validity_seconds (int): ქეშის ვალიდურობის ხანგრძლივობა წამებში. Default მნიშველობა 3600.
        """
        
        self.width = width
        self.height = height
        
        self._cache_validity_seconds = cache_validity_seconds
        self.show_only_country_currency = False

        self.cache = {}
        self.currency_names = {}
        self.root = tk.Tk()
        self.root.title("ვალუტის კონვერტორი")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0", relief=tk.FLAT)
        style.configure("TLabel", background="#f0f0f0", font=("Sylfaen", 12))
        style.configure("TEntry", font=("Sylfaen", 12))
        style.configure("TButton", padding=8, relief=tk.RAISED, background="#4CAF50", foreground="white") 

        self.root.resizable(True, True)

    def get_max_int64(self) -> int:
        return self.__INT64_MAX

    def get_currency_names(self) -> dict:
        """
        აბრუნებს ყველა ვალუტის სახელებს API-ს გამოყენებით.
        """
        currency_names = requests.get(
            self.__ALL_CURRENCIES_URL
        )
    
        currency_names.raise_for_status()
        
        return currency_names.json()

    def create_widgets(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.rowconfigure(6, weight=1)

        # სტატიკური ელემენტები
        self.static1 = ttk.Label(self.root, text="ვალუტის კონვერტორი", anchor='center', font=("Sylfaen", 15, "bold")).grid(column=0, row=0, columnspan=3, padx=10, pady=10, sticky='ew')
        self.static2 = ttk.Label(self.root, text="თანხა:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.static3 = ttk.Label(self.root, text="საბაზისო ვალუტა:").grid(column=0, row=2, padx=10, pady=10, sticky='w')
        self.static4 = ttk.Label(self.root, text="კონვერტაციის ვალუტა:").grid(column=0, row=3, padx=10, pady=10, sticky='w')
        
        self.settings_button = ttk.Button(self.root, text="პარამეტრები", command=self.open_settings_window).grid(column=0, row=0, padx=10, pady=10, sticky='w')

        # შეყვანის ველი
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

        # ვალიდაციის Labels
        self.from_currency = tk.StringVar(value=self.__DEFAULT_FROM_CURRENCY)
        self.to_currency = tk.StringVar(value=self.__DEFAULT_TO_CURRENCY)
        self.from_currency_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.from_currency,
        )
        self.from_currency_dropdown.grid(column=1, row=2, padx=10, pady=10, sticky='ew')

        self.to_currency_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.to_currency,
        )
        self.to_currency_dropdown.grid(column=1, row=3, padx=10, pady=10, sticky='ew')
        
        # ბაინდები
        self.from_currency_dropdown.bind('<KeyRelease>', self.validate_from_currency)
        self.from_currency_dropdown.bind('<<ComboboxSelected>>', self.validate_from_currency)
        self.to_currency_dropdown.bind('<KeyRelease>', self.validate_to_currency)
        self.to_currency_dropdown.bind('<<ComboboxSelected>>', self.validate_to_currency)

        self.from_currency_validation_label = ttk.Label(self.root, text=self.currency_names.get(self.__DEFAULT_FROM_CURRENCY.lower(), 'ვალუტა ვერ მოიძებნა'), width=30, anchor='w')
        self.from_currency_validation_label.grid(column=2, row=2, padx=10, pady=10, sticky='w')
        self.from_currency_validation_label.config(wraplength=200)

        # ვალიდაციის Labels
        self.to_currency_validation_label = ttk.Label(self.root, text=self.currency_names.get(self.__DEFAULT_TO_CURRENCY.lower(), 'ვალუტა ვერ მოიძებნა'), width=30, anchor='w')
        self.to_currency_validation_label.grid(column=2, row=3, padx=10, pady=10, sticky='w')
        self.to_currency_validation_label.config(wraplength=200)
        
        # კონვერტაციის ღილაკი
        self.convert_button = ttk.Button(self.root, text="კონვერტაცია", command=self.convert_currency)
        self.convert_button.grid(column=0, row=4, padx=10, pady=10, columnspan=3, sticky='ew')

        # გასუფთავების ღილაკი
        self.clear_button = ttk.Button(self.root, text="გასუფთავება", command=self.clear_fields)
        self.clear_button.grid(column=0, row=6, padx=10, pady=10, columnspan=3, sticky='ew')

        # შედეგის ლეიბელი
        self.result_label = ttk.Label(self.root, text="კონვერტირებული თანხა:")
        self.result_label.grid(column=0, row=5, columnspan=3, padx=15, pady=10, sticky='w')

        self.replace_Combobox_values()

    def validate_from_currency(self, event: tk.Event) -> None:
        """
        ამოწმებს "from_currency" ველში შეყვანილ ტექსტს და შესაბამისად განაახლებს ვალიდაციის ლეიბლის ტექსტს.
        """

        code = self.from_currency.get().lower()
        if code in self.currency_names:
            self.from_currency_validation_label.config(text=self.currency_names[code] if self.currency_names[code].strip() else 'ვალუტა მოიძებნა')
        else:
            self.from_currency_validation_label.config(text="ვალუტა ვერ მოიძებნა")

        self.from_currency.set(self.from_currency.get().upper())

    def validate_to_currency(self, event: tk.Event) -> None:
        """
        ამოწმებს "to_currency" ველში შეყვანილ ტექსტს და შესაბამისად განაახლებს ვალიდაციის ლეიბლის ტექსტს.
        """

        code = self.to_currency.get().lower()
        if code in self.currency_names:
            self.to_currency_validation_label.config(text=self.currency_names[code] if self.currency_names[code].strip() else 'ვალუტა მოიძებნა')
        else:
            self.to_currency_validation_label.config(text="ვალუტა ვერ მოიძებნა")

        self.to_currency.set(self.to_currency.get().upper())
    
    def replace_Combobox_values(self) -> None:
        if self.show_only_country_currency:
            self.from_currency_dropdown['values'] = self.country_currencies
            self.to_currency_dropdown['values'] = self.country_currencies
        else:
            self.from_currency_dropdown['values'] = list(map(lambda x: x.upper(), self.currency_names.keys()))
            self.to_currency_dropdown['values'] = list(map(lambda x: x.upper(), self.currency_names.keys()))

    def convert_currency(self) -> None:
        """
        აკონვერტებს შეყვანილ თანხას ერთი ვალუტიდან მეორეში API-ს გამოყენებით.
        """
        self.result_label.config(text="კონვერტირებული თანხა: მუშავდება...")
        self.root.update_idletasks()
        # ამოწმებს თუ ვალიდაციის ლეიბელებში შეცდომაა
        if (n:=self.from_currency_validation_label.cget("text") == "ვალუტა ვერ მოიძებნა") or self.to_currency_validation_label.cget("text") == "ვალუტა ვერ მოიძებნა":
            self.result_label.config(text=f"არასწორი ვალუტის კოდი: {self.from_currency.get().upper() if n else self.to_currency.get().upper()}")
        else:
            try:
                result = float(self.amount_entry.get().replace(',', ''))
                assert result >= 0, "თანხა უნდა იყოს დადებითი რიცხვი"
                
                assert result < self.__INT64_MAX, "თანხა ძალიან დიდია"
                
                to_currency_code = self.to_currency.get().lower()
                
                # თუ შეყვანილი თანხაა 0 მაშინ არის საჭირო კონვერტაცია
                if result == 0:
                    self.result_label.config(text="კონვერტირებული თანხა: 0.00 " + to_currency_code.upper())
                    return
                
                from_currency_code = self.from_currency.get().lower()

                # თუ ვალუტები ერთნაირია მაშინ არარი საჭიროა კონვერტაცია
                if from_currency_code == to_currency_code:
                    self.result_label.config(text=f"კონვერტირებული თანხა: {result:,.2f} {to_currency_code.upper()}")
                    return

                # რექუესტი API სერვერზე ვალუტის კურსების მისაღებად თუ მეხსიერებაში არ გვაქვს ქეში    ან    ქეშის დრო ამოიწურა default: (1 საათი)
                if not (from_currency_cache:=self.cache.get(from_currency_code)) or (datetime.now(UTC) - from_currency_cache['fetch_time']).seconds > self._cache_validity_seconds:
                    
                    currency_rates = requests.get(
                        self.__SINGLE_CURRENCY_URL.format(
                            currency_code=from_currency_code
                        )
                    )

                    assert currency_rates.status_code == 200, "დაფიქსირდა შეცდომა"
                    
                    currency_rates = currency_rates.json()

                    rate = currency_rates[from_currency_code][to_currency_code]

                    result = result * rate
                    
                    # ქეშის განახლება
                    self.cache.update({from_currency_code: {'currency_rate': currency_rates[from_currency_code], 'fetch_time': datetime.now(UTC)}})
                    
                else:
                    result = result * self.cache[from_currency_code]['currency_rate'][to_currency_code]

                self.result_label.config(text=f"კონვერტირებული თანხა: {result:,.2f} {to_currency_code.upper()}")
            except AssertionError as e:
                self.result_label.config(text=str(e))
            except IndexError as e:
                self.result_label.config(text='კონვერტირება ვერ მოხერხდა')
            except ValueError as e:
                self.result_label.config(text="გთხოვთ, შეიყვანოთ ვალიდური თანხა")

    def clear_fields(self) -> None:
        self.amount_entry.delete(0, tk.END)
        self.from_currency.set(self.__DEFAULT_FROM_CURRENCY.lower())
        self.to_currency.set(self.__DEFAULT_TO_CURRENCY)
        
        self.result_label.config(text="კონვერტირებული თანხა:")

        self.validate_from_currency(None)
        self.validate_to_currency(None)

    def center_window(self, root, window_width: int, window_height: int) -> None:
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 4  

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def mainloop(self) -> None:
        """
            ეს არის მთავარი ფუნქცია, რომელიც გამოიძახება ფანჯრის გამოსატანად.

            raises:
                HTTPError თუ API-სთან კავშირი ვერ დამყარდა
        """
       
        self.currency_names = self.get_currency_names()

        self.center_window(self.root, self.width, self.height)

        self.create_widgets()

        self.root.attributes("-topmost", True)
        self.root.after(500, lambda: self.root.attributes("-topmost", False))

        self.root.mainloop()
    
    def open_settings_window(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("პარამეტრები")
        
        settings_window.resizable(True, True)
        settings_window.attributes("-topmost", True)

        self.center_window(settings_window, 500, 150)

        frame = ttk.Frame(settings_window)
        frame.pack(pady=10)
        
        currency_label = ttk.Label(frame, text="აჩვენოს მხოლოდ ქვეყნის კურსები:")
        currency_label.grid(row=0, column=0, padx=10, pady=5)
        
        radio_var = tk.StringVar()
        radio_var.set(self.show_only_country_currency)
        
        radio1 = ttk.Radiobutton(frame, text="კი", variable=radio_var, value=True)
        radio1.grid(row=0, column=1, padx=10, pady=5)
        
        radio2 = ttk.Radiobutton(frame, text="არა", variable=radio_var, value=False)
        radio2.grid(row=0, column=2, padx=10, pady=5)
        
        cache_label = ttk.Label(frame, text="ქეშის ვალიდურობა წამებში:")
        cache_label.grid(row=1, column=0, padx=10, pady=5)
        
        cache_entry = tk.Entry(frame)
        cache_entry.insert(0, str(self._cache_validity_seconds))
        cache_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def save_settings():
            country_currency = bool(int(radio_var.get()))
            cache_validity = cache_entry.get()
            
            if cache_validity.isdigit() and int(cache_validity) >= 0:
                self._cache_validity_seconds = int(cache_validity)
            else:
                messagebox.showerror("შეცდომა", "გთხოვთ შეიყვანოთ მხოლოდ არაუარყოფითი რიცხვი", parent=settings_window)
                return

            settings_window.destroy()
            if not self.show_only_country_currency is country_currency:
                self.show_only_country_currency = country_currency
                self.replace_Combobox_values()
        
        save_button = ttk.Button(settings_window, text="დამახსოვრება", command=save_settings)
        save_button.pack(pady=10)
        settings_window.mainloop()



if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()
