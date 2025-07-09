# -*- coding: utf-8 -*-
# 
# Copyright (c) 2025~2999 - Cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(kw_only=True)
class Payment:
    # payment date
    pay_date: datetime
    # subscription start date, None if not applicable
    sub_start_date: datetime | None
    # subscription duration in days
    sub_duration: int
    # whether the next billing is deferred
    # (e.g., if the user has a free trial or has paused their subscription)
    is_defer_next_billing: bool

    def get_sub_start_date(self, previous_payments: list['Payment']):
        if self.sub_start_date:
            return self.sub_start_date

        if previous_payments:
            previous_sub_end_date = previous_payments[-1].get_sub_end_date(previous_payments[:-1])
            if previous_sub_end_date:
                return max(previous_sub_end_date, self.pay_date)

        return self.pay_date

    def get_sub_end_date(self, previous_payments: list['Payment']):
        sub_start_date = self.get_sub_start_date(previous_payments)
        return sub_start_date + timedelta(days=self.sub_duration)


def calc_next_payment_date(sub_start_date: datetime, payments: list[Payment]) -> datetime:
    if payments:
        # ensure sorted by pay_date
        payments = sorted(payments, key=lambda p: p.pay_date)
        if payments_defered := [p for p in payments if p.is_defer_next_billing]:
            return payments_defered[-1].get_sub_end_date(payments_defered[:-1])

    return sub_start_date
