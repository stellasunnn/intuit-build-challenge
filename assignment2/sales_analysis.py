import csv
import datetime
from collections import defaultdict
import os


def read_data(csv_path):
    """Load coffee shop sales data from CSV and normalize types."""
    sales = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.date.fromisoformat(row["date"])
            quantity = int(row["quantity"])
            price = float(row["price"])
            time_of_day = row["time_of_day"].strip().lower()
            is_member = row["is_member"].strip().lower() == "yes"
            member_id = row["member_id"].strip() or None

            sale = {
                "order_id": row["order_id"],
                "date": date,
                "time_of_day": time_of_day,
                "store": row["store"].strip(),
                "item_name": row["item_name"].strip(),
                "quantity": quantity,
                "price": price,
                "is_member": is_member,
                "member_id": member_id,
            }
            sales.append(sale)
    return sales


def row_revenue(sale):
    return sale["quantity"] * sale["price"]


# 1. total revenue (all rows)
def total_revenue(sales):
    return sum(map(row_revenue, sales))


# 2. revenue by store (sunnyvale / mountainview / palo alto)
def revenue_by_store(sales):
    totals = defaultdict(float)
    for s in sales:
        store = s["store"]
        totals[store] += row_revenue(s)
    return dict(totals)


# 3. revenue by time of day (morning / afternoon / night)
def revenue_by_time_of_day(sales):
    totals = defaultdict(float)
    for s in sales:
        tod = s["time_of_day"]
        totals[tod] += row_revenue(s)
    return dict(totals)


# 4. top N popular items by time of day (morning / afternoon / night)
def popular_items_by_time_of_day(sales, top_n=3):
    """
    For each time_of_day, return top N items by total quantity sold.
    Example:
      {
        "morning": [("Latte", 10), ("Espresso", 5)],
        "afternoon": [("Cheesecake", 7), ...],
        ...
      }
    """
    # time_of_day -> item_name -> total quantity
    counts = defaultdict(lambda: defaultdict(int))

    for s in sales:
        tod = s["time_of_day"]
        item = s["item_name"]
        qty = s["quantity"]
        counts[tod][item] += qty

    result = {}
    for tod, item_counts in counts.items():
        sorted_items = sorted(
            item_counts.items(),
            key=lambda kv: kv[1],  # sort by total quantity
            reverse=True,
        )
        result[tod] = sorted_items[:top_n]

    return result


# 5. member vs non-member revenue
def member_vs_non_member_revenue(sales):
    member_total = 0.0
    non_member_total = 0.0

    for s in sales:
        rev = row_revenue(s)
        if s["is_member"]:
            member_total += rev
        else:
            non_member_total += rev

    return {
        "member": member_total,
        "non_member": non_member_total,
    }


# 6. average member visits per week
def average_member_visits_per_week(sales):
    """
    Approximate average member visits per week.

    - Each row is treated as one visit from that member.
    - Group member orders by (year, ISO week).
    - For each member: visits_per_week = total_orders / number_of_weeks_active.
    - Return the average of visits_per_week across all members.
    """
    # member_id -> { (year, week) -> count_of_orders }
    member_weeks = defaultdict(lambda: defaultdict(int))

    for s in sales:
        if not s["is_member"] or not s["member_id"]:
            continue

        date = s["date"]
        year, week, _ = date.isocalendar()
        week_key = (year, week)

        member_weeks[s["member_id"]][week_key] += 1

    if not member_weeks:
        return 0

    per_member_averages = []
    for weeks_dict in member_weeks.values():
        total_orders = sum(weeks_dict.values())
        num_weeks = len(weeks_dict)
        if num_weeks > 0:
            per_member_averages.append(total_orders / num_weeks)

    if not per_member_averages:
        return 0

    return sum(per_member_averages) / len(per_member_averages)


def main():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "coffee_sales.csv")
    sales = read_data(csv_path)
    total = total_revenue(sales)
    by_store = revenue_by_store(sales)
    by_tod = revenue_by_time_of_day(sales)
    popular = popular_items_by_time_of_day(sales)
    member_split = member_vs_non_member_revenue(sales)
    avg_visits = average_member_visits_per_week(sales)

    TIME_ORDER = ["morning", "afternoon", "night"]

    print("=== Total Revenue ===")
    print(total)

    print("\n=== Revenue by Store ===")
    for store, value in by_store.items():
        print(f"{store}: {value}")

    print("\n=== Revenue by Time of Day ===")
    for tod in TIME_ORDER:
        value = by_tod.get(tod, 0)
        print(f"{tod}: {value}")

    print("\n=== Popular Items by Time of Day (top 3) ===")
    for tod in TIME_ORDER:
        print(f"{tod}:")
        for item_name, qty in popular.get(tod, []):
            print(f"  {item_name}: {qty}")

    print("\n=== Member vs Non-Member Revenue ===")
    for label, value in member_split.items():
        print(f"{label}: {value}")

    print("\n=== Average Member Visits per Week ===")
    print(avg_visits)


if __name__ == "__main__":
    main()