# -*- coding: utf-8 -*-
# 
# Copyright (c) 2025~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from algo import Payment, compute_next_payment_date, datetime


def test_auto_payments():
    assert compute_next_payment_date(
        sub_start_date=datetime(2025, 1, 1),
        payments=[
            # auto payments:
            Payment(pay_date=datetime(2025, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
        ]) == datetime(2026, 1, 1)

    assert compute_next_payment_date(
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

    assert compute_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2026, 1, 1)

    # add 1 year gift card:
    payments.append(
        Payment(pay_date=datetime(2025, 2, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=False)
    )
    payments.append(
        Payment(pay_date=datetime(2025, 3, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=False)
    )
    assert compute_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2026, 1, 1)

    # add auto payments:
    payments.append(
        Payment(pay_date=datetime(2026, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True)
    )
    assert compute_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2027, 1, 1)

    # add 1 year gift card:
    payments.append(
        Payment(pay_date=datetime(2026, 4, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=False)
    )
    assert compute_next_payment_date(sub_start_date=sub_start_date, payments=payments) == datetime(2027, 1, 1)


def test_with_outdated_payments():
    sub_start_date = datetime(2025, 1, 1)

    assert compute_next_payment_date(
        sub_start_date=sub_start_date,
        payments=[
            # outdated payments:
            Payment(pay_date=datetime(2015, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
            # auto payments:
            Payment(pay_date=datetime(2025, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
        ]) == datetime(2026, 1, 1)

    # if only has gift card, should starts with `sub_start_date`:
    assert compute_next_payment_date(
        sub_start_date=sub_start_date,
        payments=[
            # outdated payments:
            Payment(pay_date=datetime(2015, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
            # gift card:
            Payment(pay_date=datetime(2024, 8, 8), sub_start_date=None, sub_duration=365, is_defer_next_billing=False),
            Payment(pay_date=datetime(2025, 4, 4), sub_start_date=None, sub_duration=365, is_defer_next_billing=False),
        ]) == sub_start_date


def test_reallive_service_1():
    next_payment_date = datetime(2027, 11, 28)

    assert compute_next_payment_date(
        sub_start_date=datetime(2025, 11, 28),
        payments=[
            # gift card with defer next billing
            Payment(pay_date=datetime(2022, 6, 14), sub_start_date=datetime(2024, 11, 28), sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2022, 7, 31), sub_start_date=datetime(2025, 11, 28), sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2024, 8, 26), sub_start_date=datetime(2026, 11, 28), sub_duration=365, is_defer_next_billing=True),
        ]) == next_payment_date

    assert compute_next_payment_date(
        sub_start_date=datetime(2025, 11, 28),
        payments=[
            # gift card with defer next billing
            Payment(pay_date=datetime(2022, 6, 14), sub_start_date=datetime(2024, 11, 28), sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2022, 7, 31), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2024, 8, 26), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
        ]) == next_payment_date

    assert compute_next_payment_date(
        sub_start_date=datetime(2025, 11, 28),
        payments=[
            # gift card with defer next billing
            Payment(pay_date=datetime(2022, 6, 14), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2022, 7, 31), sub_start_date=datetime(2025, 11, 28), sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2024, 8, 26), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
        ]) == next_payment_date


def test_reallive_service_2():
    assert compute_next_payment_date(
        sub_start_date=datetime(2000, 1, 1), # start from undefined day
        payments=[
            # gift card with defer next billing
            Payment(pay_date=datetime(2023, 11, 20), sub_start_date=datetime(2024, 2, 14), sub_duration=366, is_defer_next_billing=True),
            Payment(pay_date=datetime(2023, 11, 21), sub_start_date=datetime(2025, 2, 14), sub_duration=365, is_defer_next_billing=True),
            Payment(pay_date=datetime(2023, 11, 22), sub_start_date=datetime(2026, 2, 14), sub_duration=365, is_defer_next_billing=True),
        ]) == datetime(2027, 2, 14)
