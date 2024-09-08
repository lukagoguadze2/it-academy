import os
import requests

from PyQt5 import uic
from PyQt5.QtCore import Qt
from datetime import datetime, UTC

from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedWidget, QLineEdit, QPushButton,
                             QWidget, QLabel, QComboBox, QMessageBox)


CACHE_FILE = 'cache.txt'


class LoginWindow(QWidget):
    __USERNAME = "admin"
    __PASSWORD = "admin"

    def __init__(self, switch_to_currency_converter):
        super().__init__()
        self.switch_to_currency_converter = switch_to_currency_converter

        self.login_field: QLineEdit | None = None
        self.password_field: QLineEdit | None = None
        self.login_button: QPushButton | None = None

        self.load_ui()

    def load_ui(self):
        # Load login UI from the .ui file
        uic.loadUi('ui/login.ui', self)

        self.login_field = self.findChild(QLineEdit, 'login_field')
        self.password_field = self.findChild(QLineEdit, 'password_field')
        self.login_button = self.findChild(QPushButton, 'login_button')

        self.password_field.setEchoMode(QLineEdit.Password)
        self.login_button.clicked.connect(self.handle_login)
        self.login_field.installEventFilter(self)
        self.password_field.installEventFilter(self)

    def handle_login(self):
        username = self.login_field.text()
        password = self.password_field.text()
        if username == self.__USERNAME and password == self.__PASSWORD:
            self.cache_user_login()
            self.switch_to_currency_converter()
            self.login_field.clear()
            self.password_field.clear()
        else:
            QMessageBox.warning(self, 'Login Error', 'ემაილი ან პაროლი არასწორია')

    @staticmethod
    def cache_user_login():
        with open(CACHE_FILE, 'w') as file:
            file.write('logged_in')

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress and event.key() == Qt.Key_Return:
            if source == self.login_field:
                self.password_field.setFocus()
                return True
            elif source == self.password_field:
                self.handle_login()
                return True
        return super().eventFilter(source, event)


class CurrencyConverter(QWidget):
    __INT64_MAX = 2**63 - 1
    __DEFAULT_FROM_CURRENCY = "USD"
    __DEFAULT_TO_CURRENCY = "GEL"
    __ALL_CURRENCIES_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
    __SINGLE_CURRENCY_URL = __ALL_CURRENCIES_URL.replace('.json', '') + "/{currency_code}.json"
    custom_html = '<html><head/><body><p><span style="font-size:12pt; font-weight:600;">{}</span></p></body></html>'
    currencies = [
                'USD', 'CAD', 'EUR', 'AED', 'AFN', 'ALL', 'AMD', 'ARS', 'AUD', 'AZN', 'BAM', 'BDT', 'BGN',
                'BHD', 'BIF', 'BND', 'BOB', 'BRL', 'BWP', 'BYN', 'BZD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP',
                'CRC', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EEK', 'EGP', 'ERN', 'ETB', 'GBP', 'GEL',
                'GHS', 'GNF', 'GTQ', 'HKD', 'HNL', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK',
                'JMD', 'JOD', 'JPY', 'KES', 'KHR', 'KMF', 'KRW', 'KWD', 'KZT', 'LBP', 'LKR', 'LTL', 'LVL',
                'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MOP', 'MUR', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN',
                'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON',
                'RSD', 'RUB', 'RWF', 'SAR', 'SDG', 'SEK', 'SGD', 'SOS', 'SYP', 'THB', 'TND', 'TOP', 'TRY',
                'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VEF', 'VND', 'XAF', 'XOF', 'YER', 'ZAR',
                'ZMK', 'ZWL'
            ]

    def __init__(self):
        super().__init__()

        self.currency_names = self.get_currency_names()
        self.cache = {}

        self.show_only_country_currency: bool = False

        self.amount_entry: QLineEdit | None = None
        self.from_currency_dropdown: QComboBox | None = None
        self.to_currency_dropdown: QComboBox | None = None
        self.from_currency_validation_label: QLabel | None = None
        self.to_currency_validation_label: QLabel | None = None
        self.result_label: QLabel | None = None
        self.convert_button: QPushButton | None = None
        self.clear_button: QPushButton | None = None

        self.load_ui()
        self.replace_combobox_values()

    def load_ui(self):
        self.setWindowTitle("Currency Converter")
        self.setGeometry(100, 100, 600, 400)

        uic.loadUi('ui/currency.ui', self)

        self.amount_entry = self.findChild(QLineEdit, 'amount_entry')
        self.from_currency_dropdown = self.findChild(QComboBox, 'from_currency_dropdown')
        self.to_currency_dropdown = self.findChild(QComboBox, 'to_currency_dropdown')
        self.from_currency_validation_label = self.findChild(QLabel, 'from_currency_validation_label')
        self.to_currency_validation_label = self.findChild(QLabel, 'to_currency_validation_label')
        self.result_label = self.findChild(QLabel, 'result_label')
        self.convert_button = self.findChild(QPushButton, 'convert_button')
        self.clear_button = self.findChild(QPushButton, 'clear_button')

        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_fields)
        self.from_currency_dropdown.currentTextChanged.connect(self.validate_from_currency)
        self.to_currency_dropdown.currentTextChanged.connect(self.validate_to_currency)

        self.show()

    def get_currency_names(self):
        response = requests.get(self.__ALL_CURRENCIES_URL)
        response.raise_for_status()
        return response.json()

    def validate_from_currency(self):
        code = self.from_currency_dropdown.currentText().lower()
        if code in self.currency_names:
            self.from_currency_validation_label.setText(self.currency_names.get(code, 'ვალუტა ვერ მოიძებნა'))
        else:
            self.from_currency_validation_label.setText("ვალუტა ვერ მოიძებნა")

        self.from_currency_dropdown.setCurrentText(code.upper())

    def validate_to_currency(self):
        code = self.to_currency_dropdown.currentText().lower()
        if code in self.currency_names:
            self.to_currency_validation_label.setText(self.currency_names.get(code, 'ვალუტა მოიძებნა'))
        else:
            self.to_currency_validation_label.setText("ვალუტა ვერ მოიძებნა")

        self.to_currency_dropdown.setCurrentText(code.upper())

    def replace_combobox_values(self):
        if self.show_only_country_currency:
            self.from_currency_dropdown.addItems(self.currencies)
            self.to_currency_dropdown.addItems(self.currencies)
        else:
            self.from_currency_dropdown.addItems(list(map(lambda x: x.upper(), self.currency_names.keys())))
            self.to_currency_dropdown.addItems(list(map(lambda x: x.upper(), self.currency_names.keys())))

        self.from_currency_dropdown.setCurrentText(self.__DEFAULT_FROM_CURRENCY)
        self.to_currency_dropdown.setCurrentText(self.__DEFAULT_TO_CURRENCY)

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.text().replace(',', ''))
            assert amount >= 0, "თანხა უნდა იყოს დადებითი რიცხვი"
            assert amount < self.__INT64_MAX, "თანხა ძალიან დიდია"

            from_currency_code = self.from_currency_dropdown.currentText().lower()
            to_currency_code = self.to_currency_dropdown.currentText().lower()

            if from_currency_code == to_currency_code:
                self.result_label.setText(
                    self.custom_html.format(f"კონვერტირებული თანხა: {amount:,.2f} {to_currency_code.upper()}")
                )
                return

            if (from_currency_code not in self.cache or (datetime.now(UTC) -
                                                         self.cache[from_currency_code]['fetch_time']).seconds > 3600):
                response = requests.get(
                    self.__SINGLE_CURRENCY_URL.format(
                        currency_code=from_currency_code
                    )
                )

                assert response.status_code == 200, "დაფიქსირდა შეცდომა"

                currency_rates = response.json()
                rate = currency_rates[from_currency_code][to_currency_code]
                self.cache[from_currency_code] = {'currency_rate': currency_rates[from_currency_code],
                                                  'fetch_time': datetime.now(UTC)}
            else:
                rate = self.cache[from_currency_code]['currency_rate'][to_currency_code]

            result = amount * rate
            self.result_label.setText(self.custom_html.format(
                f"კონვერტირებული თანხა: {result:,.2f} {to_currency_code.upper()}")
            )

        except AssertionError as e:
            self.result_label.setText(self.custom_html.format(str(e)))
        except IndexError:
            self.result_label.setText(self.custom_html.format('კონვერტირება ვერ მოხერხდა'))
        except ValueError:
            self.result_label.setText(self.custom_html.format("გთხოვთ, შეიყვანოთ ვალიდური თანხა"))

    def clear_fields(self):
        self.amount_entry.clear()
        self.from_currency_dropdown.setCurrentText(self.__DEFAULT_FROM_CURRENCY)
        self.to_currency_dropdown.setCurrentText(self.__DEFAULT_TO_CURRENCY)
        self.result_label.setText(self.custom_html.format("კონვერტირებული თანხა:"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.stacked_widget: QStackedWidget = self.findChild(QStackedWidget, 'stacked_widget')

        self.log_out = self.findChild(QPushButton, 'logout')
        self.log_out.clicked.connect(self.clear_user_login_cache)

        self.login_page: QWidget = LoginWindow(self.show_currency_converter)
        self.currency_converter_page: QWidget = CurrencyConverter()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.currency_converter_page)

        if os.path.exists(CACHE_FILE):
            self.show_currency_converter()
        else:
            self.show_login_page()

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.log_out.hide()

    def show_currency_converter(self):
        self.stacked_widget.setCurrentWidget(self.currency_converter_page)
        self.log_out.show()

    def clear_user_login_cache(self):
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)

        self.show_login_page()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
