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