````markdown
# Intuit Build Challenge

This repo contains two Python assignments:

- **Assignment 1** – Producer–Consumer concurrency pattern  
- **Assignment 2** – CSV-based coffee shop sales analysis
  

## Prerequisites

- Python 3.9+ installed  
- No external dependencies (only Python standard library)


## Setup

Clone and enter the repo:

```bash
git clone https://github.com/stellasunnn/intuit-build-challenge.git
cd intuit-build-challenge
````

---

## Assignment 1 – Producer–Consumer

**Files:**

* `assignment1/producer_consumer.py`
* `assignment1/test_producer_consumer.py`

The program implements a classic producer–consumer pattern using:

* `threading.Thread`
* `queue.Queue`
* A sentinel object to signal completion
* A shared destination container

### Run the demo

From the repo root:

```bash
python assignment1/producer_consumer.py
```

**Sample output (shape will vary slightly due to threading):**

```text
[Producer] Starting
[Consumer] Starting
[Producer] producing: 1
[Consumer] consuming: 1
[Producer] producing: 2
[Producer] producing: 3
[Consumer] consuming: 2
[Producer] producing: 4
[Producer] producing: 5
[Consumer] consuming: 3
[Producer] sending sentinel, done producing
[Producer] Ending.
[Consumer] consuming: 4
[Consumer] consuming: 5
[Consumer] received sentinel, done consuming
[Consumer] Ending.
[Main] All done. Destination data: [1, 2, 3, 4, 5]
```

### Run tests

```bash
python -m unittest assignment1.test_producer_consumer
```

---

## Assignment 2 – Coffee Shop Sales Analysis

**Files:**

* `assignment2/coffee_sales.csv` – synthetic sales data for November 2025
* `assignment2/sales_analysis.py` – analysis functions
* `assignment2/test_sales_analysis.py` – unit tests

The CSV contains:

* `order_id, date, time_of_day, store, item_name, quantity, price, is_member, member_id`
* Three stores: **Sunnyvale**, **Mountainview**, **Palo Alto**
* More morning traffic and member purchases to make the metrics interesting

The analysis demonstrates:

* Functional / stream-style operations (e.g. `sum(... for ...)`, `map`, comprehensions)
* Aggregation and grouping
* Lambda expressions for sorting

Functions:

* `total_revenue(sales)`
* `revenue_by_store(sales)`
* `revenue_by_time_of_day(sales)`
* `popular_items_by_time_of_day(sales, top_n=3)`
* `member_vs_non_member_revenue(sales)`
* `average_member_visits_per_week(sales)`

### Run the analysis

From the repo root:

```bash
python assignment2/sales_analysis.py
```

**Sample output (example for the provided `coffee_sales.csv`):**

```text
=== Total Revenue ===
424.7

=== Revenue by Store ===
Sunnyvale: 150.75
Mountainview: 137.5
Palo Alto: 136.45

=== Revenue by Time of Day ===
morning: 321.25
afternoon: 52.7
night: 50.75

=== Popular Items by Time of Day (top 3) ===
morning:
  Latte: 28
  Croissant: 7
  Americano: 6
afternoon:
  Latte: 2
  Cheesecake: 2
  Croissant: 2
night:
  Latte: 3
  Espresso: 2
  Blueberry Muffin: 2

=== Member vs Non-Member Revenue ===
member: 321.25
non_member: 103.45

=== Average Member Visits per Week ===
1.851851851851852
```

### Run tests

From the repo root:

```bash
python -m unittest assignment2.test_sales_analysis
```
