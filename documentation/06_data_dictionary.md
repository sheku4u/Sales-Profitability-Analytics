# Sales & Profitability Analytics --- Data Dictionary

## 1. Customers

  ------------------------------------------------------------------------------------------------------
  Column                Type           Description    NULL?          Validation
  --------------------- -------------- -------------- -------------- -----------------------------------
  customer_id           string         Unique         No             Must be unique
                                       customer                      
                                       identifier                    

  customer_name         string         Customer name  No             Non-empty

  gender                category       Customer       Yes            Controlled categories
                                       gender                        

  age                   integer        Customer age   Yes            18--80 expected

  city                  string         Customer city  Yes            Standardized

  state                 string         Customer state Yes            Valid Indian state/UT

  region_id             string         Region         No             Must exist in regions
                                       identifier                    

  customer_segment      category       Business       No             Consumer/Corporate/SMB/Enterprise
                                       segment                       

  signup_date           date           Customer       No             Cannot be future-dated
                                       registration                  
                                       date                          

  acquisition_channel   category       How customer   Yes            Controlled categories
                                       was acquired                  
  ------------------------------------------------------------------------------------------------------

### Potential data-quality issues

-   Missing state
-   Invalid age
-   Duplicate customer IDs
-   Inconsistent city spelling
-   Inconsistent segment capitalization
-   Future signup dates
-   Invalid region IDs

------------------------------------------------------------------------

## 2. Products

  ----------------------------------------------------------------------------
  Column           Type           Description    NULL?          Validation
  ---------------- -------------- -------------- -------------- --------------
  product_id       string         Unique product No             Must be unique
                                  identifier                    

  product_name     string         Product name   No             Non-empty

  category         category       Main product   No             Controlled
                                  category                      categories

  subcategory      category       Product        Yes            Valid for
                                  subcategory                   category

  brand            string         Product brand  Yes            Standardized

  unit_cost        decimal        Cost per unit  No             \> 0

  standard_price   decimal        Standard       No             \> unit_cost
                                  selling price                 in most cases

  supplier_id      string         Supplier       Yes            Valid format
                                  identifier                    

  launch_date      date           Product launch No             Valid date
                                  date                          
  ----------------------------------------------------------------------------

### Potential data-quality issues

-   Negative unit cost
-   Zero price
-   Price below cost
-   Missing category
-   Inconsistent category names
-   Invalid launch dates
-   Duplicate product IDs

------------------------------------------------------------------------

## 3. Regions

  Column        Type      Description
  ------------- --------- ----------------------------------
  region_id     string    Unique region identifier
  region_name   string    Region name
  state_count   integer   Number of states/UTs represented

Initial regions:

-   North
-   South
-   East
-   West
-   Central
-   North-East
-   NCR
-   Metro
-   Tier-2
-   Tier-3

The exact geographic mapping will be documented before generation.

------------------------------------------------------------------------

## 4. Sales Channels

  Column         Type       Description
  -------------- ---------- ---------------------------
  channel_id     string     Unique channel identifier
  channel_name   category   Sales channel
  channel_type   category   Broad channel grouping

Initial channels:

-   Online
-   Retail Store
-   Marketplace
-   Corporate Sales

------------------------------------------------------------------------

## 5. Orders

One row represents one customer order.

  Column           Type       Description                    NULL?
  ---------------- ---------- ------------------------------ -------
  order_id         string     Unique order ID                No
  order_date       date       Order date                     No
  customer_id      string     Customer placing order         No
  region_id        string     Region associated with order   No
  channel_id       string     Sales channel                  No
  payment_method   category   Payment method                 Yes
  order_status     category   Order status                   No

### Initial order statuses

-   Completed
-   Cancelled
-   Pending
-   Returned
-   Partially Returned

### Initial payment methods

-   UPI
-   Credit Card
-   Debit Card
-   Net Banking
-   Cash
-   Wallet
-   COD

### Potential data-quality issues

-   Duplicate order IDs
-   Missing customer IDs
-   Invalid customer IDs
-   Future order dates
-   Invalid channel IDs
-   Inconsistent status values
-   Invalid payment categories

------------------------------------------------------------------------

## 6. Order_Items

This is the primary analytical fact table.

One row represents one product line inside an order.

  Column          Type      Description                            NULL?
  --------------- --------- -------------------------------------- -------
  order_item_id   string    Unique line-item ID                    No
  order_id        string    Parent order                           No
  product_id      string    Product sold                           No
  quantity        integer   Units sold                             No
  unit_price      decimal   Actual selling price before discount   No
  discount_pct    decimal   Discount percentage                    Yes
  unit_cost       decimal   Cost per unit at transaction time      No

### Derived fields

These should be calculated during analysis:

``` text
Gross Sales
Discount Amount
Net Revenue
COGS
Gross Profit
Profit Margin
```

### Recommended formulas

``` text
Gross Sales =
quantity × unit_price

Discount Amount =
Gross Sales × discount_pct

Net Revenue =
Gross Sales - Discount Amount

COGS =
quantity × unit_cost

Gross Profit =
Net Revenue - COGS

Profit Margin =
Gross Profit / Net Revenue
```

### Potential data-quality issues

-   Negative quantity
-   Zero quantity
-   Negative price
-   Discount below 0%
-   Discount above 100%
-   Invalid order ID
-   Invalid product ID
-   Unit cost greater than selling price
-   Duplicate line items
-   Mismatch between product master cost and transaction cost

------------------------------------------------------------------------

## 7. Returns

One row represents a return event.

  Column            Type       Description                NULL?
  ----------------- ---------- -------------------------- -------
  return_id         string     Unique return ID           No
  order_id          string     Related order              No
  product_id        string     Returned product           No
  return_date       date       Return date                No
  return_quantity   integer    Units returned             No
  return_reason     category   Reason for return          No
  return_status     category   Return processing status   No

### Return reasons

-   Damaged
-   Wrong Product
-   Customer Changed Mind
-   Late Delivery
-   Quality Issue
-   Incorrect Size

### Potential data-quality issues

-   Return quantity \> purchased quantity
-   Return before order date
-   Invalid order ID
-   Invalid product ID
-   Duplicate return records
-   Missing reason
-   Invalid status

------------------------------------------------------------------------

## 8. Targets

One row represents a target for one region for one month.

  Column          Type      Description
  --------------- --------- ---------------------------
  target_month    date      First day of target month
  region_id       string    Region
  sales_target    decimal   Monthly sales target
  profit_target   decimal   Monthly profit target

### Validation rules

-   One target per region per month
-   Target values must be positive
-   Target month must fall within analysis period
-   Region must exist in master data

------------------------------------------------------------------------

## 9. Date Dimension

A Date dimension will be created later for Power BI and time analysis.

Expected fields:

``` text
date
year
quarter
month
month_number
month_name
week
day
day_name
is_weekend
```

This table will support:

-   MoM analysis
-   YoY analysis
-   Monthly trends
-   Quarterly trends
-   Weekday/weekend analysis

## 10. Derived Metrics

The following should not be blindly copied from raw data:

  Metric            Calculation
  ----------------- -------------------------------
  Gross Sales       Quantity × Unit Price
  Discount Amount   Gross Sales × Discount %
  Net Revenue       Gross Sales − Discount Amount
  COGS              Quantity × Unit Cost
  Gross Profit      Net Revenue − COGS
  Profit Margin     Gross Profit / Net Revenue
  AOV               Net Revenue / Distinct Orders
  Return Rate       Returned Units / Sold Units
  MoM Growth        Current vs Previous Month
  YoY Growth        Current vs Prior Year

## 11. Metric Reconciliation

The same important metrics will eventually be calculated independently
in:

1.  Python
2.  SQL
3.  Power BI

Any mismatch must be investigated before the final result is considered
reliable.

## 12. Data Lineage Principle

For important metrics we should be able to answer:

> Where did this number come from?

Example:

``` text
Power BI Profit
    ↓
DAX measure
    ↓
Clean order_items
    ↓
Validated quantity, price, discount and cost
    ↓
Raw transaction data
```
