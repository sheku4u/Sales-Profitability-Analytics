# Sales & Profitability Analytics --- Data Generation Specification

## 1. Purpose

This document defines how the practice dataset should be generated.

The data should look realistic enough to support genuine business
analysis while intentionally containing controlled quality problems.

## 2. Analysis Period

Initial version:

``` text
2024-01-01 through 2026-06-30
```

This gives us:

-   Multiple years
-   Year-over-year analysis
-   Monthly trends
-   Seasonal patterns
-   Enough history for customer behavior analysis

## 3. Customer Population

Target:

``` text
10,000 customers
```

Expected distributions should not be perfectly uniform.

Examples:

-   Some cities have more customers.
-   Some segments are larger.
-   Some acquisition channels perform better.
-   Customer signup activity varies over time.

## 4. Product Population

Target:

``` text
2,000 products
```

Products should have realistic variation in:

-   Category
-   Subcategory
-   Price
-   Cost
-   Margin
-   Demand
-   Return rate

We should intentionally create different product archetypes:

### High-volume / high-margin

Strong performers.

### High-volume / low-margin

Potential profitability problem.

### Low-volume / high-margin

Potential growth opportunity.

### Low-volume / low-margin

Potential discontinuation candidates.

### High-return products

Operational/product-quality concern.

## 5. Orders

Target:

``` text
~120,000 orders
```

Order frequency should vary by:

-   Customer
-   Month
-   Region
-   Channel
-   Segment

We should create realistic seasonality rather than random uniform sales.

Potential seasonal periods:

-   Festive periods
-   End-of-year
-   Promotional periods
-   Month-end effects

## 6. Order Items

Target:

``` text
~220,000–300,000 rows
```

Most orders should contain 1--3 products.

A smaller percentage should contain larger baskets.

This will create realistic AOV and basket-size distributions.

## 7. Price and Cost Design

Products should have different gross margins.

Example conceptual distribution:

``` text
Low margin: 5–15%
Medium margin: 15–30%
High margin: 30–50%
```

Do not make every product fit perfectly into these ranges. Some
legitimate negative-margin transactions should exist due to discounting.

## 8. Discount Design

Most transactions should have low or no discounts.

A smaller proportion should have moderate discounts.

A small number should have unusually high discounts.

Example:

``` text
0%
5%
10%
15%
20%
25%
30%
40%
50%
```

A very small number of deliberately invalid values may be generated:

``` text
-5%
110%
150%
```

These are quality-test records, not normal business behavior.

## 9. Profitability Pattern

The generated data should contain real business patterns.

For example:

``` text
Category A:
High sales + high margin

Category B:
High sales + low margin

Category C:
Low sales + high margin

Category D:
High returns + weak margin
```

The analyst should discover these patterns rather than being given the
answers.

## 10. Regional Pattern

Regions should have different characteristics.

Example:

``` text
Region A:
High revenue + strong margin

Region B:
High revenue + weak margin

Region C:
Low revenue + strong margin

Region D:
High return rate
```

Again, these should be detectable through analysis rather than hardcoded
into documentation as known answers.

## 11. Channel Pattern

Channels should have different economics.

For example:

``` text
Online:
High volume
Moderate AOV
Higher returns

Retail:
Lower volume
Higher AOV
Lower returns

Marketplace:
High discounting
Lower margin

Corporate:
Low order count
High order value
```

These are generation targets, not final conclusions.

## 12. Return Generation

Target:

``` text
~8,000 return records
```

Return probability should vary by:

-   Product
-   Category
-   Region
-   Channel
-   Return reason

Some products should naturally have higher return rates.

## 13. Target Generation

Create monthly sales and profit targets for each region.

Targets should be close enough to actual performance to create:

-   Above-target regions
-   Below-target regions
-   Seasonal target gaps

## 14. Intentional Data-Quality Injection

The generator should inject controlled problems after generating the
base data.

Suggested initial problem rates:

  Issue                        Approx. Rate
  -------------------------- --------------
  Missing optional fields             1--5%
  Missing critical fields            \<0.5%
  Duplicate-like records          0.2--0.5%
  Invalid numeric values             \<0.2%
  Category inconsistencies            1--2%
  Orphan foreign keys                \<0.1%
  Date anomalies                     \<0.1%
  Extreme outliers                   \<0.2%

These rates should be adjusted after profiling the generated dataset.

## 15. Important Constraint

Do not inject so many errors that the dataset becomes unrealistic.

The objective is:

> **Messy enough to investigate, clean enough to remain believable.**

## 16. Reproducibility

The Python generator must use a fixed random seed.

This ensures:

-   Same dataset can be regenerated.
-   Bugs can be reproduced.
-   Analysis can be audited.
-   Interview demonstrations are repeatable.

## 17. Generation Pipeline

The eventual Python process should be:

``` text
1. Generate master data
        ↓
2. Generate customers
        ↓
3. Generate products
        ↓
4. Generate regions/channels
        ↓
5. Generate orders
        ↓
6. Generate order items
        ↓
7. Generate returns
        ↓
8. Generate targets
        ↓
9. Inject controlled quality issues
        ↓
10. Save raw CSVs
        ↓
11. Generate a data-generation log
```

## 18. Important Rule

The generator must not create a dataset that already contains the final
analytical answers in obvious ways.

For example, we should not simply make one region bad in every possible
metric.

Realistic data should contain:

-   Trade-offs
-   Noise
-   Exceptions
-   Seasonal variation
-   Legitimate outliers
-   Conflicting signals

This forces genuine analytical reasoning.
