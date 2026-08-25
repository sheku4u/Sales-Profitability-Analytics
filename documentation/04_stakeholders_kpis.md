# Sales & Profitability Analytics --- Stakeholders and KPI Framework

## 1. Stakeholders

### Chief Executive / Business Leadership

Primary questions:

-   Are we growing?
-   Is growth profitable?
-   Where are the biggest risks?
-   Where should management focus?

### Sales Leadership

Primary questions:

-   Which regions are performing?
-   Which products are selling?
-   Which channels are effective?
-   Are targets being achieved?

### Finance

Primary questions:

-   What is gross profit?
-   What is margin?
-   Where is profitability declining?
-   How much do discounts and returns affect profit?

### Marketing

Primary questions:

-   Which customers and products are valuable?
-   Which segments should be targeted?
-   Are promotions generating profitable growth?

### Operations / Product Teams

Primary questions:

-   Which products have high returns?
-   Which products have poor economics?
-   Are there regional or product-specific issues?

## 2. KPI Definitions

### Revenue

``` text
Revenue = Quantity × Unit Price
```

If discounts are applied:

``` text
Gross Sales = Quantity × Unit Price

Discount Amount = Gross Sales × Discount %

Net Revenue = Gross Sales - Discount Amount
```

The project will explicitly distinguish gross sales from net revenue.

### Gross Profit

``` text
Gross Profit = Net Revenue - COGS
```

### Profit Margin

``` text
Profit Margin = Gross Profit / Net Revenue
```

### Units Sold

``` text
Units Sold = SUM(Quantity)
```

### Orders

``` text
Orders = COUNT(DISTINCT Order ID)
```

### Average Order Value

``` text
AOV = Net Revenue / Distinct Orders
```

### Discount Rate

``` text
Discount Rate = Discount Amount / Gross Sales
```

### Return Rate

Version 1 definition:

``` text
Return Rate = Returned Units / Sold Units
```

We will document the exact definition used before building the
dashboard.

### MoM Growth

``` text
MoM Growth =
(Current Month Revenue - Previous Month Revenue)
/
Previous Month Revenue
```

### YoY Growth

``` text
YoY Growth =
(Current Period Revenue - Prior-Year Revenue)
/
Prior-Year Revenue
```

## 3. KPI Design Principle

Every KPI must answer a business question.

We will avoid adding metrics simply because they are easy to calculate.

For each KPI we will document:

-   Definition
-   Formula
-   Business purpose
-   Data source
-   Granularity
-   Known limitations

## 4. Primary KPI Set

The initial executive KPI set will be:

1.  Net Revenue
2.  Gross Profit
3.  Profit Margin
4.  Orders
5.  Units Sold
6.  Average Order Value
7.  Discount Rate
8.  Return Rate
9.  MoM Revenue Growth
10. YoY Revenue Growth

## 5. Important Analytical Dimensions

The KPIs should be analyzed across:

-   Date
-   Product
-   Category
-   Customer
-   Customer segment
-   Region
-   State
-   Sales channel
-   Return reason
-   Promotion/discount level

## 6. Metric Governance

Before finalizing the dashboard, we will test whether the same KPI
produces consistent results across:

-   Python
-   SQL
-   Power BI

If the numbers disagree, we investigate the metric definition or data
model before presenting the result.

This is intentional: **metric reconciliation is part of the project.**
