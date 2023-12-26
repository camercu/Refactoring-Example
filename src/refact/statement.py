import locale

from .statement_data import create_statement_data


def statement(invoice: dict, plays: dict):
    return render_plaintext(create_statement_data(invoice, plays))


def render_plaintext(data: dict):
    result = f"Statement for {data['customer']}\n"
    for perf in data["performances"]:
        result += f"  {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
    result += f"Amount owed is {usd(data['total_amount'])}\n"
    result += f"You earned {data['total_volume_credits']} credits\n"
    return result


def usd(cents):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return locale.currency(cents / 100, grouping=True)
