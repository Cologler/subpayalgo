# -*- coding: utf-8 -*-
# 
# Copyright (c) 2025~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from algo import Payment, calc_next_payment_date, datetime


def test_auto_payments():
    assert calc_next_payment_date(
        sub_start_date=datetime(2025, 1, 1),
        payments=[
            # auto payments:
            Payment(pay_date=datetime(2025, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
        ]) == datetime(2026, 1, 1)

    assert calc_next_payment_date(
        sub_start_date=datetime(2025, 1, 1),
        payments=[
            # auto payments:
            Payment(pay_date=datetime(2025, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2026, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2027, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
        ]) == datetime(2028, 1, 1)


def test_gift_cards():
    sub_start_date = datetime(2025, 1, 1)
    payments = [
        # auto payments:
        Payment(pay_date=datetime(2025, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
    ]

    assert calc_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2026, 1, 1)

    # add 1 year gift card:
    payments.append(
        Payment(pay_date=datetime(2025, 2, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=False)
    )
    payments.append(
        Payment(pay_date=datetime(2025, 3, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=False)
    )
    assert calc_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2026, 1, 1)

    # add auto payments:
    payments.append(
        Payment(pay_date=datetime(2026, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True)
    )
    assert calc_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2027, 1, 1)

    # add 1 year gift card:
    payments.append(
        Payment(pay_date=datetime(2026, 4, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=False)
    )
    assert calc_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2027, 1, 1)
