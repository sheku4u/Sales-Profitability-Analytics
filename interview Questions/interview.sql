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

