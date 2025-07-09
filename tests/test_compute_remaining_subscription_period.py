# -*- coding: utf-8 -*-
# 
# Copyright (c) 2025~2999 - Cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

from functools import partial

from algo import Payment, compute_remaining_subscription_period, datetime


def test_auto_payments():
    get_period = partial(compute_remaining_subscription_period, payments=[
        # auto payments:
        Payment(pay_date=datetime(2025, 1, 1), sub_start_date=None, sub_duration=365, is_defer_next_billing=True),
    ])

    assert get_period(today=datetime(2025, 1, 1)) == 365
    assert get_period(today=datetime(2025, 6, 1)) == 214
    assert get_period(today=datetime(2025, 12, 31)) == 1
    assert 1 > get_period(today=datetime(2025, 12, 31, hour=6)) > 0 # expire today
    assert get_period(today=datetime(2026, 1, 1)) == 0 # expired now
    assert 0 > get_period(today=datetime(2026, 1, 1, hour=6)) > -1
    assert get_period(today=datetime(2026, 1, 2)) == -1
    assert get_period(today=datetime(2026, 6, 1)) == -151


def test_reallive_service_2():
    get_period = partial(compute_remaining_subscription_period, payments=[
        # gift card with defer next billing
        Payment(pay_date=datetime(2023, 11, 20), sub_start_date=datetime(2024, 2, 14), sub_duration=365, is_defer_next_billing=True),
        Payment(pay_date=datetime(2023, 11, 21), sub_start_date=datetime(2025, 2, 14), sub_duration=365, is_defer_next_billing=True),
        Payment(pay_date=datetime(2023, 11, 22), sub_start_date=datetime(2026, 2, 14), sub_duration=365, is_defer_next_billing=True),
    ])

    assert get_period(today=datetime(2025, 7, 3)) == 591
    assert get_period(today=datetime(2025, 7, 10)) == 584

