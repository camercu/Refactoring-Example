import locale
from copy import copy


def statement(invoice: dict, plays: dict):
    def play_for(performance):
        return plays[performance["playID"]]

    def amount_for(performance):
        result = 0

        match performance["play"]["type"]:
            case "tragedy":
                result = 40000
                if performance["audience"] > 30:
                    result += 1000 * (performance["audience"] - 30)
            case "comedy":
                result = 30000
                if performance["audience"] > 20:
                    result += 10000 + 500 * (performance["audience"] - 20)
                result += 300 * performance["audience"]
            case _:
                raise Exception(f"unknown type: ${performance['play']['type']}")
        return result

    def volume_credits_for(performance):
        result = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == performance["play"]["type"]:
            result += performance["audience"] // 5
        return result

    def total_volume_credits(data):
        result = 0
        for perf in data["performances"]:
            result += perf["volume_credits"]
        return result

    def total_amount(data):
        return sum(p["amount"] for p in data["performances"])

    def enrich_performance(performance):
        result = copy(performance)
        result["play"] = play_for(result)
        result["amount"] = amount_for(result)
        result["volume_credits"] = volume_credits_for(result)
        return result

    statement_data = {}
    statement_data["customer"] = invoice["customer"]
    statement_data["performances"] = [
        enrich_performance(p) for p in invoice["performances"]
    ]
    statement_data["total_volume_credits"] = total_volume_credits(statement_data)
    statement_data["total_amount"] = total_amount(statement_data)
    return render_plaintext(statement_data)


def render_plaintext(data: dict):
    def usd(cents):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.currency(cents / 100, grouping=True)

    result = f"Statement for {data['customer']}\n"
    for perf in data["performances"]:
        result += f"  {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
    result += f"Amount owed is {usd(data['total_amount'])}\n"
    result += f"You earned {data['total_volume_credits']} credits\n"
    return result
