# Sales & Profitability Analytics --- Data Quality Rules

## 1. Purpose

The raw dataset will intentionally contain realistic quality issues.

The objective is not to make the data artificially perfect. The
objective is to practice detecting, assessing, documenting, and
resolving data problems before business analysis.

## 2. Quality Dimensions

We will assess:

-   Completeness
-   Uniqueness
-   Validity
-   Consistency
-   Accuracy
-   Timeliness
-   Referential integrity

## 3. Completeness Rules

Check missing values for important fields.

### Critical fields

These should generally not be missing:

-   customer_id
-   product_id
-   order_id
-   order_date
-   quantity
-   unit_price
-   unit_cost

### Non-critical fields

Some descriptive fields may legitimately contain NULLs:

-   customer_state
-   customer_gender
-   brand
-   acquisition_channel

We must distinguish:

> Missing because the field is optional

from:

> Missing because the data pipeline failed.

## 4. Uniqueness Rules

Check:

``` text
customer_id → unique
product_id → unique
order_id → unique
order_item_id → unique
return_id → unique
```

For `order_items`, repeated `order_id` values are expected.

Therefore:

> Never treat repeated order IDs in order_items as duplicates
> automatically.

This is an important grain-level validation exercise.

## 5. Validity Rules

### Quantity

Expected:

``` text
quantity > 0
```

### Unit price

Expected:

``` text
unit_price > 0
```

### Unit cost

Expected:

``` text
unit_cost > 0
```

### Discount

Expected:

``` text
0 <= discount_pct <= 1
```

### Age

Expected:

``` text
18 <= age <= 80
```

### Return quantity

Expected:

``` text
return_quantity > 0
```

## 6. Date Rules

Check:

-   Invalid date formats
-   Missing dates
-   Future dates
-   Return date before order date
-   Product launch date after transaction date
-   Signup date after first purchase

## 7. Referential Integrity

Every foreign key should map to a valid parent record.

Examples:

``` text
orders.customer_id → customers.customer_id

order_items.order_id → orders.order_id

order_items.product_id → products.product_id

returns.order_id → orders.order_id

returns.product_id → products.product_id

targets.region_id → regions.region_id
```

We will deliberately introduce a small number of orphan records so this
can be practiced.

## 8. Consistency Rules

Detect inconsistent categories such as:

``` text
Online
online
ONLINE
Online 
```

and:

``` text
Electronics
electronics
Electronic
Electronics 
```

The cleaning process should standardize them without destroying
legitimate categories.

## 9. Business-Logic Rules

### Rule 1

Net revenue should not exceed gross sales.

### Rule 2

Discount amount should not be negative.

### Rule 3

Gross profit should reconcile with net revenue and COGS.

### Rule 4

Return quantity should not normally exceed the quantity purchased for
the same order/product combination.

### Rule 5

A completed order should normally have at least one order item.

### Rule 6

A returned order should have a corresponding return record.

### Rule 7

A product should normally exist in the product master before it appears
in sales.

### Rule 8

Customer signup date should not be after the customer's order date.

## 10. Accuracy Checks

Where source values are available, compare stored/calculated values.

Example:

``` text
Expected Net Revenue
vs
Source Net Revenue
```

If they differ:

1.  Measure the difference.
2.  Determine how widespread it is.
3.  Determine whether the source or calculation is more trustworthy.
4.  Document the decision.

## 11. Outlier Detection

Outliers should not automatically be deleted.

Examples:

-   Extremely large order
-   Very high quantity
-   Very high discount
-   Very high order value
-   Very high customer spend

The analyst must ask:

> Is this an error or a legitimate business event?

This distinction is part of the project.

## 12. Data Quality Report

The final quality report should contain:

  Issue                      Records Severity   Decision   Reason
  ------------------------ --------- ---------- ---------- --------
  Missing customer ID            TBD High       TBD        TBD
  Duplicate order IDs            TBD High       TBD        TBD
  Invalid discount               TBD High       TBD        TBD
  Invalid quantity               TBD High       TBD        TBD
  Category inconsistency         TBD Medium     TBD        TBD
  Future order date              TBD Medium     TBD        TBD
  Orphan product IDs             TBD High       TBD        TBD

The values will be discovered by Python after the raw data is generated.

## 13. Cleaning Principle

Never silently modify data.

For every major cleaning action, document:

``` text
Problem
→ Evidence
→ Decision
→ Transformation
→ Business impact
```

## 14. Important Interview Principle

A strong answer is not:

> "I removed nulls and duplicates."

A stronger answer is:

> "I first profiled the data by table grain and business-critical
> fields, quantified the quality issues, determined which missing or
> duplicate records could affect revenue and profit metrics, then
> applied documented rules and reconciled the cleaned results against
> the raw source."
