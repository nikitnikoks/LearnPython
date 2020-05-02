import argparse
import math


class CreditCalculator:
    def __init__(self):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("--type")
        self.ap.add_argument("--payment", type=float)
        self.ap.add_argument("--principal", type=float)
        self.ap.add_argument("--periods", type=int)
        self.ap.add_argument("--interest", type=float)
        args = self.ap.parse_args()
        self.formula = args.type
        self.principal = args.principal
        self.payment = args.payment
        self.periods = args.periods
        self.interest = args.interest
        self.total = 0

    def validate_parameters(self):
        indata = [self.formula, self.principal, self.interest, self.payment, self.periods]
        element_num = sum(1 for i in indata if i is not None)
        if element_num < 4:
            print('Incorrect parameters')
            exit()
        elif self.interest is None or self.interest < 0:
            print('Incorrect parameters')
            exit()
        elif self.formula is None or self.formula not in ('diff', 'annuity'):
            print('Incorrect parameters')
            exit()
        elif self.formula == 'diff' and self.payment is not None:
            print('Incorrect parameters')
            exit()
        elif self.principal is not None and self.principal < 0 \
                or self.payment is not None and self.payment < 0 \
                or self.periods is not None and self.periods < 0:
            print('Incorrect parameters')
            exit()

    def calc_diff_payment(self):
        for x in range(1, self.periods + 1):
            diff_payment = math.ceil(self.principal
                                     / self.periods
                                          + self.interest / 1200
                                          * (self.principal - self.principal * (x - 1)
                                             / self.periods))
            self.total += diff_payment
            print(f'Month {x}: paid out {diff_payment}')
        print()

    def calc_periods(self):
        self.periods = math.ceil(math.log(self.payment
                                          / (self.payment - self.interest / 1200 * self.principal),
                                          1 + self.interest / 1200))
        print(f'You need {self.months_to_years()} to repay this credit!')

    def calc_payment(self):
        self.payment = math.ceil(self.principal
                                 * (self.interest / 1200
                                    * math.pow(1 + self.interest / 1200, self.periods)
                                    / (math.pow(1 + self.interest / 1200, self.periods) - 1)))
        print(f'Your annuity payment = {self.payment}!')

    def calc_principal(self):
        self.principal = math.floor(self.payment
                                    / (self.interest / 1200
                                          * math.pow(1 + self.interest / 1200, self.periods)
                                          / (math.pow(1 + self.interest / 1200, self.periods) - 1)))
        print(f'Your credit principal = {self.principal}!')

    def calc_overpayment(self):
        if self.total == 0:
            self.total = self.payment * self.periods
        print('Overpayment =', int(self.total - self.principal))

    def months_to_years(self):
        years = self.periods // 12
        months = self.periods % 12
        if years > 0 and months > 0:
            result = f'{years} years and {months} months'
        elif years == 0 and months > 0:
            result = f'{months} months'
        else:
            result = f'{years} years'
        return result

    def calc(self):
        if self.formula == 'diff':
            self.calc_diff_payment()
        elif self.formula == 'annuity' and self.periods is None:
            self.calc_periods()
        elif self.formula == 'annuity' and self.payment is None:
            self.calc_payment()
        elif self.formula == 'annuity' and self.principal is None:
            self.calc_principal()

    def run(self):
        self.validate_parameters()
        self.calc()
        self.calc_overpayment()


calculator = CreditCalculator()
calculator.run()

