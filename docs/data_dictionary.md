# 📖 Data Dictionary

## File: data/expenses.csv

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| Date | string / datetime | Date of expense (YYYY-MM-DD) | 2024-03-15 |
| Category | string | Expense type/category | Food, Rent, Transport |
| Amount | float | Expense amount in Indian Rupees (₹) | 450.00 |
| Payment_Method | string | How the payment was made | UPI, Cash, Credit Card |
| Note | string | Short description of the expense | Lunch at canteen |

## Derived Columns (added during cleaning)

| Column | Derived From | Description |
|--------|-------------|-------------|
| Month | Date | Period string e.g. "2024-03" for grouping |
| Day | Date | Python date object for daily aggregation |

## Category Reference

| Category | Amount Range (₹) | Examples |
|----------|-----------------|---------|
| Food | 80 – 600 | Groceries, dining, coffee |
| Transport | 30 – 400 | Auto, cab, bus, petrol |
| Utilities | 200 – 1,200 | Electricity, internet, mobile |
| Entertainment | 100 – 800 | Movies, OTT, gaming |
| Healthcare | 50 – 1,500 | Medicine, doctor, gym |
| Shopping | 200 – 3,000 | Clothes, electronics, footwear |
| Education | 500 – 3,000 | Courses, books, exam fees |
| Rent | 3,000 – 6,000 | PG, hostel, monthly rent |

## Payment Method Reference

| Method | Typical Use |
|--------|------------|
| Cash | Small offline purchases |
| UPI | Digital peer-to-peer (PhonePe, GPay) |
| Credit Card | Large purchases, online shopping |
| Debit Card | ATM withdrawals, offline stores |

## Output Files

| File | Format | Description |
|------|--------|-------------|
| outputs/category_summary.csv | CSV | Total, average, count per category |
| outputs/monthly_summary.csv | CSV | Monthly totals |
| outputs/payment_summary.csv | CSV | Payment method totals |
| reports/expense_report_2024.txt | Text | Human-readable annual summary |
| images/category_bar.png | PNG | Category bar chart |
| images/monthly_line.png | PNG | Monthly trend line chart |
| images/payment_pie.png | PNG | Payment method pie chart |
| images/daily_trend.png | PNG | Daily spending area chart |
