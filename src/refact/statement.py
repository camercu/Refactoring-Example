import locale


def statement(invoice: dict, plays: dict):
    def play_for(performance):
        return plays[performance["playID"]]

    def amount_for(performance):
        result = 0

        match play_for(performance)["type"]:
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
                raise Exception(f"unknown type: ${play_for(performance)['type']}")
        return result

    def volume_credits_for(performance):
        result = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == play_for(performance)["type"]:
            result += performance["audience"] // 5
        return result

    def total_volume_credits():
        result = 0
        for perf in invoice["performances"]:
            result += volume_credits_for(perf)
        return result

    def total_amount():
        result = 0
        for perf in invoice["performances"]:
            result += amount_for(perf)
        return result

    def usd(cents):
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        return locale.currency(cents / 100, grouping=True)

    result = f"Statement for {invoice['customer']}\n"
    for perf in invoice["performances"]:
        result += f"  {play_for(perf)['name']}: {usd(amount_for(perf))} ({perf['audience']} seats)\n"
    result += f"Amount owed is {usd(total_amount())}\n"
    result += f"You earned {total_volume_credits()} credits\n"
    return result
