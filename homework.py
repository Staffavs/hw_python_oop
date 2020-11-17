import datetime as dt

today = dt.datetime.date(dt.datetime.now())

class Record:
    def __init__(self, amount, comment, date=None):

        if date is None:
            date = today

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

    def get_today_stats(self):
        result = 0
        for record in self.records:
            if record.date == today:
                result += record.amount
        return result

    def get_week_stats(self):
        result = 0
        week = today - dt.timedelta(days=7)
        for record in self.records:
            if week < record.date <= today:
                result += record.amount
        return result



class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_today_stats(self):
        stats = (super().get_today_stats())
        return(f'Сегодня уже наели на: {stats} кКал')

    def get_week_stats(self):
        week_stats = (super().get_week_stats())
        return(f'За последние 7 дней получено: {week_stats} кКал')

    def get_calories_remained(self):
        result = (super().get_today_stats())
        result = self.limit - result
        if result > 0:
            return(f'Сегодня можно съесть что-нибудь ещё,'
                   f' но с общей калорийностью не более {result} кКал')
        else:
            return(f'Хватит есть!')



class CashCalculator(Calculator):
    USD_RATE = float(76.23)
    EURO_RATE = float(90.27)

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_stats(self):
        today_stats = (super().get_today_stats())
        return(f'Сегодня потрачено: {today_stats} руб')

    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': [1, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
        }
        rate = currencies[currency]
        money = self.limit - float(super().get_today_stats())
        money = round(money / rate[0], 2)
        if money > 0:
            return (f'На сегодня осталось {money} {rate[1]}')
        elif money == 0:
            return (f'Денег нет, держись')
        else:
            money = money * -1
            return (f'Денег нет, держись: твой долг - {money} {rate[1]}')

    def get_week_stats(self):
        week_stats = (super().get_week_stats())
        return(f'За последние 7 дней потрачено: {week_stats} руб')



