-- 1. Customer Revenue Growth — Window Functions

-- For every customer who has placed orders in at least 2 different months, calculate:

-- Customer ID
-- Month
-- Monthly revenue
-- Previous month's revenue
-- MoM revenue growth %
-- Flag whether revenue increased or decreased

-- Rules:

-- Missing months should be treated as 0 revenue.
-- Don't calculate growth when previous-month revenue is 0.
-- Return only customers with at least 2 months of activity.



-- 1. What is the grain?
-- it represents the particular customer order and it details about order , when order placed, what is order amount, who placed that order , and what is order all about

-- 2. Which tables do I need?
-- i need orders table which contain order details for particular customer

-- 3. What joins are required?
-- i dont think the joins required in this case if we need additional detail about customer then i will join orders table with customer table 

-- 4. What needs aggregation?
-- revenue, and orders data is requiered to affregation where revenue for sum() and order date should be group by as order month 

-- 5. Where do I need a window function?
-- row_number() when i need to check the month of each customers are different or not or exceed the alteast 2+ and lag() when i ned to get and compare the previous monthly data with current monthly data

-- 6. What edge cases exist?
-- customer could make only 1 order, might be customer returning the order 

with monthly_orders_details as (
    SELECT
        customer_id,
        date_format(order_date, "%Y-%m") as order_month,
        date_format(order_date, "%m") as monthly_num
        sum(sales_amount) as revenue
    from orders_table
    GROUP BY customer_id, date_format(order_date, "%Y-%m"), date_format(order_date, "%m")
),

unique_monthly_data as (
    SELECT
        customer_id,
        order_month,
        revenue,
       count(*) over(PARTITION BY customer_id) as monthly_rnk,
       (case
        when monthly_num not in (1 and 12) then 0
        else monthly_num end) as checking_num
    from monthly_orders_details 
),
previous_calculation_data as (
    SELECT
        *,
        lag(revenue) over(PARTITION BY customer_id ORDER BY order_month ASC) as prev_value
    from unique_monthly_data
),

main_calculation as (
    SELECT
        *,
        
        round((revenue-prev_value/prev_value )*100,2) as revenue_growth_pct,
        (case
            when revenue > prev_value then "Increased"
            when revenue < prev_value then "Decreased"
            else "No Growth"
            end) as revenue_status
    from unique_monthly_data
    
)
SELECT
* from previous_calculation_data ; 


-- Find the top 5 customers by total revenue
SELECT
    c.customer_id,
    sum(coalesce(o.amount,0)) as total_revenue
from customers c left join orders o 
on c.customer_id = o.customer_id
group by c.customer_id
order by total_revenue desc
limit 5;

-- Find customers who have placed at least 5 orders.
SELECT
    c.customer_id,
    count(distinct o.order_id) as total_orders
from customers c left join orders o 
on c.customer_id = o.customer_id
group by c.customer_id
having count(distinct o.order_id) > 5;

-- Find the second-highest revenue-generating customer.
with customer_revenue as (
    SELECT
        c.customer_id,
        sum(coalesce(o.amount,0)) as total_revenue
    from customers c left join orders o 
    on c.customer_id = o.customer_id
    group by c.customer_id
),
customer_ranked as (
    SELECT  
        *,
        dense_rank() over(order by total_revenue desc) as rnk
    from customer_revenue
)
SELECT
    customer_id,
    total_revenue
from customer_ranked
where rnk = 2;

-- Calculate monthly revenue and month-over-month revenue growth %
with monthly_rev as (
    SELECT
        date_format(order_date,"%Y-%m") as order_month,
        sum(amount) as total_revenue
    from orders
    group by date_format(order_date,"%Y-%m")
    order by order_month
),
previous_data as (
    SELECT
        *,
        lag(total_revenue) over(order by order_month) as prev_value
    from monthly_rev
)
SELECT
    order_month,
    total_revenue,
    prev_value,
    (total_revenue - prev_value) as month_over_month_growth,
    round(((total_revenue - prev_value )/prev_value)*100,2) as month_over_month_growth_pct
from previous_data;


-- revenue is above average but profit margin is below average.
WITH product_data AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(o.sales) AS total_sales,
        SUM(o.discount) AS total_discount,
        SUM(o.cogs) AS total_cogs,
        SUM(o.quantity) AS total_quantity
    FROM products p
    LEFT JOIN orders o
        ON p.product_id = o.product_id
    GROUP BY
        p.product_id,
        p.product_name
),

product_kpis AS (
    SELECT
        product_id,
        product_name,
        total_sales,
        total_discount,
        total_cogs,
        total_quantity,

        total_sales - total_discount AS revenue,

        total_sales - total_discount - total_cogs AS profit
    FROM product_data
),

product_metrics AS (
    SELECT
        *,
        profit / NULLIF(revenue, 0) AS profit_margin,

        AVG(revenue) OVER () AS avg_product_revenue,

        AVG(
            profit / NULLIF(revenue, 0)
        ) OVER () AS avg_profit_margin

    FROM product_kpis
)

SELECT
    product_id,
    product_name,
    revenue,
    profit,
    ROUND(profit_margin * 100, 2) AS profit_margin_pct,
    ROUND(avg_product_revenue, 2) AS avg_product_revenue,
    ROUND(avg_profit_margin * 100, 2) AS avg_profit_margin_pct
FROM product_metrics
WHERE revenue > avg_product_revenue
  AND profit_margin < avg_profit_margin
ORDER BY revenue DESC;

-- Find the top 3 products by revenue within each category.
with product_data as (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        sum(o.sales) as total_sales
    from products p left join orders o on p.product_id = o.product_id
    group by p.product_id,p.product_name, p.category 
),
ranked_data as (
    SELECT
        *,
        dense_rank() over(PARTITION by category order by total_sales desc) as rnk
    from product_data
)
SELECT
    *
from ranked_data
where rnk <= 3;

-- placed an order in January 2026 and placed another order in February 2026.
with customer_order_data as (
    SELECT
        date_format(order_date,"%Y-%m") as order_month,
        customer_id,
        count(distinct order_id) as total_orders
    from orders
    where year(order_date) = 2026 and month(order_date) in (1,2)
    group by date_format(order_date,"%Y-%m"), customer_id
),

