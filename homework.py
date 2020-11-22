import datetime as dt

class Record:
    def __init__(self, amount, comment, date=None):
        if date is None:
            date = dt.date.today()
        else:
            date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.amount = amount
        self.date = date
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats_old(self):
        result = 0
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                result += record.amount
        return result

    def get_today_stats(self):
        today = dt.date.today()
        result = [record.amount for record in self.records if record.date == today]
        return sum(result)

    def get_week_stats(self):
        result = 0
        week = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if week < record.date <= dt.date.today():
                result += record.amount
        return result

    def get_remained(self):
        result = self.limit - self.get_today_stats()
        return result


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        result = self.get_remained()
        if result > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                   f' но с общей калорийностью не более {result} кКал')
        return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(76.23)
    EURO_RATE = float(90.27)

    def get_today_cash_remained(self, currency):
        money = self.get_remained()
        if money == 0:
            return ('Денег нет, держись')
        currencies = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
        }
        rate = currencies[currency][0]
        rate_name = currencies[currency][1]
        money = round(money / rate, 2)
        if money > 0:
            return (f'На сегодня осталось {money} {rate_name}')
        money = abs(money)
        return (f'Денег нет, держись: твой долг - {money} {rate_name}')
