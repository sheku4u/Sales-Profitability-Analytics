# Sales & Profitability Analytics --- Phase 2: Data Architecture

## 1. Architecture Objective

The dataset should behave like a small production-style analytics
environment rather than a single flat CSV.

The model is intentionally relational so that we can practice:

-   Joins
-   Primary and foreign keys
-   Data validation
-   Dimensional analysis
-   Transaction-level calculations
-   Customer-level analysis
-   Product-level analysis
-   Time analysis
-   Target vs actual analysis
-   Return analysis

## 2. Tables

### Dimension Tables

-   `customers`
-   `products`
-   `regions`
-   `sales_channels`

### Fact / Transaction Tables

-   `orders`
-   `order_items`
-   `returns`

### Planning Table

-   `targets`

## 3. Relationship Model

``` text
customers
    │
    │ customer_id
    ▼
orders
    │
    │ order_id
    ▼
order_items ───────────────► products
    │
    │ order_id + product_id
    ▼
returns

regions ───────────────► customers
regions ───────────────► targets

sales_channels ────────► orders

targets
    │
    └── month + region_id
```

## 4. Grain of Each Table

Understanding grain is mandatory before analysis.

### customers

One row = one customer.

### products

One row = one product.

### regions

One row = one geographic region.

### sales_channels

One row = one sales channel.

### orders

One row = one customer order.

### order_items

One row = one product line within an order.

This is the main sales fact table.

### returns

One row = one return event/product return line.

### targets

One row = one region-month target.

## 5. Why Orders and Order_Items Are Separate

An order can contain multiple products.

Example:

``` text
Order ORD1001

Laptop      × 1
Mouse       × 2
Keyboard    × 1
```

`orders` stores order-level information.

`order_items` stores product-level information.

This prevents us from incorrectly repeating order-level attributes for
every product and gives us realistic SQL join practice.

## 6. Expected Initial Data Volume

The first dataset should be large enough to create realistic analytical
problems without becoming unnecessarily difficult to work with locally.

  Table                  Approx. Rows
  ---------------- ------------------
  customers                    10,000
  products                      2,000
  regions                          10
  sales_channels                    4
  orders                      120,000
  order_items        220,000--300,000
  returns                       8,000
  targets                         120

These numbers can be adjusted after generation if the resulting data
distribution is unrealistic.

## 7. Key Design

### Primary Keys

-   `customers.customer_id`
-   `products.product_id`
-   `regions.region_id`
-   `sales_channels.channel_id`
-   `orders.order_id`
-   `order_items.order_item_id`
-   `returns.return_id`

### Foreign Keys

-   `orders.customer_id → customers.customer_id`
-   `orders.region_id → regions.region_id`
-   `orders.channel_id → sales_channels.channel_id`
-   `order_items.order_id → orders.order_id`
-   `order_items.product_id → products.product_id`
-   `returns.order_id → orders.order_id`
-   `returns.product_id → products.product_id`
-   `targets.region_id → regions.region_id`

## 8. Important Modeling Decision

Profit should not simply be stored as a trusted source value.

We will derive:

``` text
Gross Sales
Discount Amount
Net Revenue
COGS
Gross Profit
Profit Margin
```

from underlying transaction fields wherever possible.

This allows us to practice validation and reconciliation.

## 9. Source-System Simulation

The raw data should simulate multiple operational systems.

For example:

``` text
Customer system → customers
Product/catalog system → products
Order management system → orders
Transaction system → order_items
Returns system → returns
Finance/planning system → targets
Master data → regions/channels
```

This is important because real-world analytics often involves
reconciling information originating from different systems.

## 10. Analytical Model

For Power BI, the preferred model will be close to a star schema:

``` text
                 Customers
                     │
                     │
Products ───── Order Items ───── Orders
                     │
                     │
                  Returns

Dimensions:
Date
Customer
Product
Region
Channel

Supporting:
Targets
```

The final Power BI model will be refined after the SQL/Python analysis
confirms the required metrics.
