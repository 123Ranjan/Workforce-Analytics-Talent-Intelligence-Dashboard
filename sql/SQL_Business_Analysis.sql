-- ==========================================================
-- AI Workforce Intelligence Dashboard
-- Phase 8 : SQL Business Analysis
-- Database : PostgreSQL
-- ==========================================================

-- ==========================================================
-- SECTION 1 : Basic SQL
-- ==========================================================


-- Query 1
-- Business Question:

-- How many employees are there in the organization?

SELECT COUNT(*) AS total_employees
FROM employee_featured;

-- Query 2
-- Business Question:

-- Display the first 10 employee records.

SELECT *
FROM employee_featured
LIMIT 10;

-- Query 3
-- Business Question:

-- What departments exist in the organization?

SELECT DISTINCT department
FROM employee_featured;

-- Query 4
-- Business Question:

-- What job roles are available?


SELECT DISTINCT job_role
FROM employee_featured
ORDER BY job_role;


-- Query 5
-- Business Question:

-- Show all employees whose monthly income is greater than ₹10,000.


SELECT employee_id,
       department,
       job_role,
       monthly_income
FROM employee_featured
WHERE monthly_income > 10000;

-- Query 6
-- Business Question:

-- Show employees who work overtime.

SELECT employee_id,
       department,
       job_role,
       over_time
FROM employee_featured
WHERE over_time = 'Yes';

-- Query 7
-- Business Question:

-- Show employees who have left the company.

SELECT employee_id,
       age,
       department,
       job_role,
       attrition_status
FROM employee_featured
WHERE attrition_status = 'Yes';

-- Query 8
-- Business Question:

-- Show employees from the Sales department.

SELECT employee_id,
       job_role,
       monthly_income
FROM employee_featured
WHERE department = 'Sales';


-- Query 9
-- Business Question:

-- Display employees ordered by highest salary.

SELECT employee_id,
        job_role,
        monthly_income
from employee_featured
ORDER BY monthly_income DESC;

-- Query 10
-- Business Question:

-- Show the top 10 highest-paid employees.


SELECT employee_id,
        job_role,
        monthly_income
from employee_featured
ORDER BY monthly_income DESC LIMIT 10;


-- ==========================================================
-- SECTION 2 : Aggregate Functions
-- ==========================================================


-- Query 11
-- Business Question:

-- What is the average monthly income of employees?

SELECT Avg(monthly_income) as average_monthly_income
FROM employee_featured;

-- if you want to round value


SELECT Round(Avg(monthly_income),2) as average_monthly_income
FROM employee_featured;

-- Query 12
-- Business Question:

-- What is the highest monthly income in the organization?

Select Max(monthly_income) as highest_monthly_income
FROM employee_featured;

-- Query 13
-- Business Question:

-- What is the lowest monthly income?


Select Min(monthly_income) as lowest_monthly_income
FROM employee_featured;

-- Query 14
-- Business Question:

-- What is the total monthly payroll?

SELECT SUM(monthly_income) AS total_monthly_payroll
FROM employee_featured;


-- Query 15
-- Business Question:

-- What is the average age of employees?

SELECT ROUND(AVG(age),2) AS average_age
FROM employee_featured;

-- Query 16
-- Business Question:

-- How many employees work overtime?

SELECT COUNT(*) AS overtime_employees
FROM employee_featured
WHERE over_time='Yes';


-- Query 17
-- Business Question:

-- How many employees have left the company?

SELECT COUNT(*) AS attrition_count
FROM employee_featured
WHERE attrition_status='Yes';


-- Query 17
-- Business Question:

-- How many employees have left the company?

SELECT COUNT(*) AS attrition_count
FROM employee_featured
WHERE attrition_status='Yes';


-- Query 18
-- Business Question:

-- What is the average years of experience of employees?

SELECT ROUND(AVG(total_working_years),2) AS average_experience
FROM employee_featured;


-- Query 19
-- Business Question:

-- What is the average salary hike percentage?

SELECT ROUND(AVG(salary_hike_percent),2) AS average_salary_hike
FROM employee_featured;

-- Query 20
-- Business Question:

-- What is the average distance employees travel from home to work?

SELECT ROUND(AVG(distance_from_home),2) AS average_distance
FROM employee_featured;


-- ==========================================================
-- SECTION 3 : GROUP BY Analysis
-- ==========================================================


-- ==========================================================
-- Query 21
-- Business Question:
-- How many employees are there in each department?
-- ==========================================================

SELECT
    department,
    COUNT(*) AS employee_count
FROM employee_featured
GROUP BY department
ORDER BY employee_count DESC;


-- ==========================================================
-- Query 22
-- Business Question:
-- What is the average monthly income in each department?
-- ==========================================================

SELECT
    department,
    ROUND(AVG(monthly_income),2) AS average_salary
FROM employee_featured
GROUP BY department
ORDER BY average_salary DESC;


-- ==========================================================
-- Query 23
-- Business Question:
-- What is the total monthly payroll for each department?
-- ==========================================================

SELECT
    department,
    SUM(monthly_income) AS total_department_payroll
FROM employee_featured
GROUP BY department
ORDER BY total_department_payroll DESC;


-- ==========================================================
-- Query 24
-- Business Question:
-- How many employees belong to each job role?
-- ==========================================================

-- ==========================================================
-- Query 24
-- Business Question:
-- How many employees belong to each job role?
-- ==========================================================

SELECT
    job_role,
    COUNT(*) AS employee_count
FROM employee_featured
GROUP BY job_role
ORDER BY employee_count DESC;


-- ==========================================================
-- Query 25
-- Business Question:
-- What is the average monthly income for each job role?
-- ==========================================================

SELECT
    job_role,
    ROUND(AVG(monthly_income),2) AS average_salary
FROM employee_featured
GROUP BY job_role
ORDER BY average_salary DESC;


-- ==========================================================
-- Query 26
-- Business Question:
-- How many employees are there in each salary band?
-- ==========================================================

SELECT
    salary_band,
    COUNT(*) AS employee_count
FROM employee_featured
GROUP BY salary_band
ORDER BY employee_count DESC;


-- ==========================================================
-- Query 27
-- Business Question:
-- How many employees belong to each experience level?
-- ==========================================================

SELECT
    experience_level,
    COUNT(*) AS employee_count
FROM employee_featured
GROUP BY experience_level
ORDER BY employee_count DESC;

-- ==========================================================
-- Query 28
-- Business Question:
-- What is the average performance rating for each department?
-- ==========================================================

SELECT
    department,
    ROUND(AVG(performance_rating),2) AS average_performance
FROM employee_featured
GROUP BY department
ORDER BY average_performance DESC;


-- ==========================================================
-- Query 29
-- Business Question:
-- How many employees work overtime in each department?
-- ==========================================================

SELECT
    department,
    COUNT(*) AS overtime_employee_count
FROM employee_featured
WHERE over_time = 'Yes'
GROUP BY department
ORDER BY overtime_employee_count DESC;


-- ==========================================================
-- Query 30
-- Business Question:
-- What is the average work-life balance score in each department?
-- ==========================================================

SELECT
    department,
    ROUND(AVG(work_life_balance),2) AS average_work_life_balance
FROM employee_featured
GROUP BY department
ORDER BY average_work_life_balance DESC;


-- ==========================================================
-- SECTION 4 : HAVING Clause
-- ==========================================================


-- ==========================================================
-- Query 31
-- Business Question:
-- Which departments have more than 200 employees?
-- ==========================================================

SELECT
    department,
    COUNT(*) AS employee_count
FROM employee_featured
GROUP BY department
HAVING COUNT(*) > 200
ORDER BY employee_count DESC;

-- ==========================================================
-- Query 32
-- Business Question:
-- Which job roles have an average monthly income greater than 8000?
-- ==========================================================


SELECT
    job_role,
    ROUND(AVG(monthly_income),2) AS average_salary
FROM employee_featured
GROUP BY job_role
HAVING AVG(monthly_income) > 8000
ORDER BY average_salary DESC;

-- ==========================================================
-- Query 33
-- Business Question:
-- Which departments have an average work-life balance greater than 2.7?
-- ==========================================================

SELECT
    department,
    ROUND(AVG(work_life_balance),2) AS average_work_life_balance
FROM employee_featured
GROUP BY department
HAVING AVG(work_life_balance) > 2.7
ORDER BY average_work_life_balance DESC;


-- ==========================================================
-- Query 34
-- Business Question:
-- Which experience levels have more than 300 employees?
-- ==========================================================

SELECT
    experience_level,
    COUNT(*) AS employee_count
FROM employee_featured
GROUP BY experience_level
HAVING COUNT(*) > 300
ORDER BY employee_count DESC;

-- ==========================================================
-- Query 35
-- Business Question:
-- Which salary bands have an average monthly income greater than 7000?
-- ==========================================================

SELECT
    salary_band,
    ROUND(AVG(monthly_income),2) AS average_salary
FROM employee_featured
GROUP BY salary_band
HAVING AVG(monthly_income) > 7000
ORDER BY average_salary DESC;

-- ==========================================================
-- Query 36
-- Business Question:
-- Which departments have a total monthly payroll greater than 2,000,000?
-- ==========================================================

SELECT
    department,
    SUM(monthly_income) AS total_payroll
FROM employee_featured
GROUP BY department
HAVING SUM(monthly_income) > 2000000
ORDER BY total_payroll DESC;


-- ==========================================================
-- Query 37
-- Business Question:
-- Which job roles have an average performance rating greater than 3?
-- ==========================================================

SELECT
    job_role,
    ROUND(AVG(performance_rating),2) AS average_performance
FROM employee_featured
GROUP BY job_role
HAVING AVG(performance_rating) > 3
ORDER BY average_performance DESC;


-- ==========================================================
-- Query 38
-- Business Question:
-- Which education fields have more than 100 employees?
-- ==========================================================

SELECT
    education_field,
    COUNT(*) AS employee_count
FROM employee_featured
GROUP BY education_field
HAVING COUNT(*) > 100
ORDER BY employee_count DESC;


-- ==========================================================
-- Query 39
-- Business Question:
-- Which departments have more than 50 employees working overtime?
-- ==========================================================

SELECT
    department,
    COUNT(*) AS overtime_employee_count
FROM employee_featured
WHERE over_time = 'Yes'
GROUP BY department
HAVING COUNT(*) > 50
ORDER BY overtime_employee_count DESC;



-- ==========================================================
-- Query 40
-- Business Question:
-- Which age groups have an average monthly income greater than 6000?
-- ==========================================================

SELECT
    age_group,
    ROUND(AVG(monthly_income),2) AS average_salary
FROM employee_featured
GROUP BY age_group
HAVING AVG(monthly_income) > 6000
ORDER BY average_salary DESC;


-- ==========================================================
-- SECTION 5 : CASE Statement
-- ==========================================================

-- ==========================================================
-- Query 41
-- Business Question:
-- Categorize employees into Low, Medium, and High salary groups.
-- ==========================================================

SELECT
    employee_id,
    monthly_income,
    CASE
        WHEN monthly_income < 5000 THEN 'Low Salary'
        WHEN monthly_income BETWEEN 5000 AND 10000 THEN 'Medium Salary'
        ELSE 'High Salary'
    END AS salary_category
FROM employee_featured;


-- ==========================================================
-- Query 42
-- Business Question:
-- Classify employees based on age.
-- ==========================================================

SELECT
    employee_id,
    age,
    CASE
        WHEN age < 30 THEN 'Young'
        WHEN age BETWEEN 30 AND 45 THEN 'Middle Age'
        ELSE 'Senior'
    END AS age_category
FROM employee_featured;


-- ==========================================================
-- Query 43
-- Business Question:
-- Classify employees based on years of experience.
-- ==========================================================

SELECT
    employee_id,
    total_working_years,
    CASE
        WHEN total_working_years < 5 THEN 'Junior'
        WHEN total_working_years BETWEEN 5 AND 15 THEN 'Mid-Level'
        ELSE 'Senior'
    END AS experience_category
FROM employee_featured;


-- ==========================================================
-- Query 44
-- Business Question:
-- Identify employees eligible for promotion.
-- ==========================================================

SELECT
    employee_id,
    years_since_last_promotion,
    CASE
        WHEN years_since_last_promotion >= 5 THEN 'Promotion Due'
        ELSE 'Recently Promoted'
    END AS promotion_status
FROM employee_featured;


-- ==========================================================
-- Query 45
-- Business Question:
-- Classify employees based on work-life balance.
-- ==========================================================

SELECT
    employee_id,
    work_life_balance,
    CASE
        WHEN work_life_balance <= 2 THEN 'Needs Improvement'
        WHEN work_life_balance = 3 THEN 'Good'
        ELSE 'Excellent'
    END AS work_life_category
FROM employee_featured;


-- ==========================================================
-- SECTION 6 : Subqueries
-- ==========================================================


-- ==========================================================
-- Query 46
-- Business Question:
-- Find employees whose monthly income is greater than the
-- average monthly income of all employees.
-- ==========================================================

SELECT
    employee_id,
    job_role,
    department,
    monthly_income
FROM employee_featured
WHERE monthly_income >
(
    SELECT AVG(monthly_income)
    FROM employee_featured
)
ORDER BY monthly_income DESC;


-- ==========================================================
-- Query 47
-- Business Question:
-- Find employees with the highest monthly income.
-- ==========================================================

SELECT
    employee_id,
    job_role,
    department,
    monthly_income
FROM employee_featured
WHERE monthly_income =
(
    SELECT MAX(monthly_income)
    FROM employee_featured
);


-- ==========================================================
-- Query 48
-- Business Question:
-- Find employees who have more working years than the
-- average experience.
-- ==========================================================

SELECT
    employee_id,
    total_working_years,
    department
FROM employee_featured
WHERE total_working_years >
(
    SELECT AVG(total_working_years)
    FROM employee_featured
)
ORDER BY total_working_years DESC;


-- ==========================================================
-- Query 49
-- Business Question:
-- Find employees whose salary is higher than the average
-- salary of their department.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income
FROM employee_featured e
WHERE monthly_income >
(
    SELECT AVG(monthly_income)
    FROM employee_featured
    WHERE department = e.department
)
ORDER BY department, monthly_income DESC;


-- ==========================================================
-- Query 50
-- Business Question:
-- Find departments whose average salary is greater than
-- the overall company average salary.
-- ==========================================================

SELECT
    department,
    ROUND(AVG(monthly_income),2) AS average_salary
FROM employee_featured
GROUP BY department
HAVING AVG(monthly_income) >
(
    SELECT AVG(monthly_income)
    FROM employee_featured
)
ORDER BY average_salary DESC;


-- ==========================================================
-- SECTION 7 : Common Table Expressions (CTEs)
-- ==========================================================

-- ==========================================================
-- Query 51
-- Business Question:
-- Find employees earning more than the company average salary
-- using a CTE.
-- ==========================================================

WITH company_average AS
(
    SELECT AVG(monthly_income) AS avg_salary
    FROM employee_featured
)

SELECT
    employee_id,
    department,
    job_role,
    monthly_income
FROM employee_featured, company_average
WHERE monthly_income > avg_salary
ORDER BY monthly_income DESC;

-- ==========================================================
-- Query 52
-- Business Question:
-- Display the average salary for each department using a CTE.
-- ==========================================================

WITH department_salary AS
(
    SELECT
        department,
        ROUND(AVG(monthly_income),2) AS average_salary
    FROM employee_featured
    GROUP BY department
)

SELECT *
FROM department_salary
ORDER BY average_salary DESC;

-- ==========================================================
-- Query 53
-- Business Question:
-- Find departments where the average salary is greater than
-- ₹7,000 using a CTE.
-- ==========================================================

WITH department_salary AS
(
    SELECT
        department,
        ROUND(AVG(monthly_income),2) AS average_salary
    FROM employee_featured
    GROUP BY department
)

SELECT *
FROM department_salary
WHERE average_salary > 7000
ORDER BY average_salary DESC;


-- ==========================================================
-- Query 54
-- Business Question:
-- Calculate employee count and average salary for each
-- department using a CTE.
-- ==========================================================

WITH department_summary AS
(
    SELECT
        department,
        COUNT(*) AS employee_count,
        ROUND(AVG(monthly_income),2) AS average_salary
    FROM employee_featured
    GROUP BY department
)

SELECT *
FROM department_summary
ORDER BY employee_count DESC;


-- ==========================================================
-- Query 55
-- Business Question:
-- Find departments with more than 200 employees using a CTE.
-- ==========================================================

WITH department_summary AS
(
    SELECT
        department,
        COUNT(*) AS employee_count
    FROM employee_featured
    GROUP BY department
)

SELECT *
FROM department_summary
WHERE employee_count > 200;


-- ==========================================================
-- SECTION 8 : Window Functions
-- ==========================================================



-- ==========================================================
-- Query 56
-- Business Question:
-- Assign a unique row number to every employee based on
-- monthly income (highest to lowest).
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    ROW_NUMBER() OVER(ORDER BY monthly_income DESC) AS row_num
FROM employee_featured;


-- ==========================================================
-- Query 57
-- Business Question:
-- Rank employees by monthly income.
-- Employees with the same salary receive the same rank.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    RANK() OVER(ORDER BY monthly_income DESC) AS salary_rank
FROM employee_featured;

-- ==========================================================
-- Query 58
-- Business Question:
-- Assign dense ranks to employees by salary.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    DENSE_RANK() OVER(ORDER BY monthly_income DESC) AS dense_salary_rank
FROM employee_featured;

-- ==========================================================
-- Query 59
-- Business Question:
-- Rank employees within each department based on salary.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    ROW_NUMBER() OVER(
        PARTITION BY department
        ORDER BY monthly_income DESC
    ) AS department_rank
FROM employee_featured;


-- ==========================================================
-- Query 60
-- Business Question:
-- Find the previous employee salary within each department.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    LAG(monthly_income) OVER(
        PARTITION BY department
        ORDER BY monthly_income
    ) AS previous_salary
FROM employee_featured;

-- ==========================================================
-- Query 61
-- Business Question:
-- Find the next employee salary within each department.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    LEAD(monthly_income) OVER(
        PARTITION BY department
        ORDER BY monthly_income
    ) AS next_salary
FROM employee_featured;


-- ==========================================================
-- Query 62
-- Business Question:
-- Calculate the cumulative payroll within each department.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    SUM(monthly_income) OVER(
        PARTITION BY department
        ORDER BY monthly_income
    ) AS running_payroll
FROM employee_featured;


-- ==========================================================
-- Query 63
-- Business Question:
-- Calculate the cumulative average salary.
-- ==========================================================

SELECT
    employee_id,
    monthly_income,
    ROUND(
        AVG(monthly_income) OVER(
            ORDER BY monthly_income
        ),
        2
    ) AS cumulative_average_salary
FROM employee_featured;

-- ==========================================================
-- Query 64
-- Business Question:
-- Display each employee's salary along with the department's
-- average salary.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    ROUND(
        AVG(monthly_income) OVER(
            PARTITION BY department
        ),
        2
    ) AS department_average_salary
FROM employee_featured;


-- ==========================================================
-- Query 65
-- Business Question:
-- Compare each employee's salary with the highest salary in
-- their department.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    MAX(monthly_income) OVER(
        PARTITION BY department
    ) AS highest_department_salary
FROM employee_featured;


-- ==========================================================
-- SECTION 9 : HR Business KPIs
-- ==========================================================

-- ==========================================================
-- Query 66
-- Business Question:
-- What is the overall employee attrition rate?
-- ==========================================================

SELECT
    ROUND(
        (COUNT(*) FILTER (WHERE attrition_status = 'Yes') * 100.0)
        / COUNT(*),
        2
    ) AS attrition_rate_percentage
FROM employee_featured;

-- ==========================================================
-- Query 67
-- Business Question:
-- What is the attrition rate for each department?
-- ==========================================================

SELECT
    department,
    COUNT(*) AS total_employees,
    COUNT(*) FILTER (WHERE attrition_status = 'Yes') AS attrition_count,
    ROUND(
        COUNT(*) FILTER (WHERE attrition_status = 'Yes') * 100.0
        / COUNT(*),
        2
    ) AS attrition_rate_percentage
FROM employee_featured
GROUP BY department
ORDER BY attrition_rate_percentage DESC;

-- ==========================================================
-- Query 68
-- Business Question:
-- What percentage of employees work overtime?
-- ==========================================================

SELECT
    ROUND(
        COUNT(*) FILTER (WHERE over_time='Yes') * 100.0
        / COUNT(*),
        2
    ) AS overtime_percentage
FROM employee_featured;

-- ==========================================================
-- Query 69
-- Business Question:
-- What is the gender distribution percentage?
-- ==========================================================

SELECT
    gender,
    COUNT(*) AS employee_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM employee_featured),
        2
    ) AS percentage
FROM employee_featured
GROUP BY gender
ORDER BY percentage DESC;

-- ==========================================================
-- Query 70
-- Business Question:
-- Which department contributes the highest percentage of the
-- total monthly payroll?
-- ==========================================================

SELECT
    department,
    SUM(monthly_income) AS department_payroll,
    ROUND(
        SUM(monthly_income) * 100.0 /
        (SELECT SUM(monthly_income) FROM employee_featured),
        2
    ) AS payroll_percentage
FROM employee_featured
GROUP BY department
ORDER BY payroll_percentage DESC;

-- ==========================================================
-- Query 71
-- Business Question:
-- What is the average employee tenure in each department?
-- ==========================================================

SELECT
    department,
    ROUND(AVG(years_at_company),2) AS average_tenure
FROM employee_featured
GROUP BY department
ORDER BY average_tenure DESC;

-- ==========================================================
-- Query 72
-- Business Question:
-- Which department has the highest average job satisfaction?
-- ==========================================================

SELECT
    department,
    ROUND(AVG(job_satisfaction),2) AS average_job_satisfaction
FROM employee_featured
GROUP BY department
ORDER BY average_job_satisfaction DESC;

-- ==========================================================
-- Query 73
-- Business Question:
-- Which salary band has the highest attrition count?
-- ==========================================================

SELECT
    salary_band,
    COUNT(*) FILTER (WHERE attrition_status='Yes') AS attrition_count
FROM employee_featured
GROUP BY salary_band
ORDER BY attrition_count DESC;

-- ==========================================================
-- Query 74
-- Business Question:
-- Which experience level receives the highest average salary?
-- ==========================================================

SELECT
    experience_level,
    ROUND(AVG(monthly_income),2) AS average_salary
FROM employee_featured
GROUP BY experience_level
ORDER BY average_salary DESC;

-- ==========================================================
-- Query 75
-- Business Question:
-- Which department has the highest average performance rating?
-- ==========================================================

SELECT
    department,
    ROUND(AVG(performance_rating),2) AS average_performance
FROM employee_featured
GROUP BY department
ORDER BY average_performance DESC;

-- ==========================================================
-- SECTION 10 : Advanced Interview SQL
-- ==========================================================

-- ==========================================================
-- Query 76
-- Business Question:
-- Find the top 3 highest-paid employees in each department.
-- ==========================================================

WITH salary_rank AS
(
    SELECT
        employee_id,
        department,
        job_role,
        monthly_income,
        ROW_NUMBER() OVER
        (
            PARTITION BY department
            ORDER BY monthly_income DESC
        ) AS rank_no
    FROM employee_featured
)

SELECT *
FROM salary_rank
WHERE rank_no <= 3
ORDER BY department, rank_no;

-- ==========================================================
-- Query 77
-- Business Question:
-- Find employees earning more than the average salary of
-- their experience level.
-- ==========================================================

SELECT
    employee_id,
    experience_level,
    monthly_income
FROM employee_featured e
WHERE monthly_income >
(
    SELECT AVG(monthly_income)
    FROM employee_featured
    WHERE experience_level = e.experience_level
);

-- ==========================================================
-- Query 78
-- Business Question:
-- Identify the highest-paid employee in each department.
-- ==========================================================

WITH ranked_salary AS
(
    SELECT
        employee_id,
        department,
        job_role,
        monthly_income,
        RANK() OVER
        (
            PARTITION BY department
            ORDER BY monthly_income DESC
        ) AS salary_rank
    FROM employee_featured
)

SELECT *
FROM ranked_salary
WHERE salary_rank = 1;

-- ==========================================================
-- Query 79
-- Business Question:
-- Compare each employee's salary with the company average.
-- ==========================================================

SELECT
    employee_id,
    monthly_income,
    ROUND(AVG(monthly_income) OVER (),2) AS company_average_salary,
    monthly_income -
    ROUND(AVG(monthly_income) OVER (),2) AS salary_difference
FROM employee_featured;

-- ==========================================================
-- Query 80
-- Business Question:
-- Find departments with above-average attrition.
-- ==========================================================

WITH department_attrition AS
(
    SELECT
        department,
        COUNT(*) FILTER (WHERE attrition_status='Yes') * 100.0 /
        COUNT(*) AS attrition_rate
    FROM employee_featured
    GROUP BY department
)

SELECT *
FROM department_attrition
WHERE attrition_rate >
(
    SELECT AVG(attrition_rate)
    FROM department_attrition
);


-- ==========================================================
-- Query 81
-- Business Question:
-- Display employees whose salary falls in the top 10%
-- of the company.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income,
    NTILE(10) OVER
    (
        ORDER BY monthly_income DESC
    ) AS salary_decile
FROM employee_featured
ORDER BY monthly_income DESC;

-- ==========================================================
-- Query 82
-- Business Question:
-- Find employees who have worked longer than the average
-- tenure of their department.
-- ==========================================================

SELECT
    employee_id,
    department,
    years_at_company
FROM employee_featured e
WHERE years_at_company >
(
    SELECT AVG(years_at_company)
    FROM employee_featured
    WHERE department = e.department
);

-- ==========================================================
-- Query 83
-- Business Question:
-- Rank departments based on total payroll.
-- ==========================================================

SELECT
    department,
    SUM(monthly_income) AS total_payroll,
    RANK() OVER
    (
        ORDER BY SUM(monthly_income) DESC
    ) AS payroll_rank
FROM employee_featured
GROUP BY department;


-- ==========================================================
-- Query 84
-- Business Question:
-- Identify employees whose salary is above their department
-- average and who work overtime.
-- ==========================================================

SELECT
    employee_id,
    department,
    monthly_income
FROM employee_featured e
WHERE monthly_income >
(
    SELECT AVG(monthly_income)
    FROM employee_featured
    WHERE department = e.department
)
AND over_time='Yes';

-- ==========================================================
-- Query 85
-- Business Question:
-- List the top-performing employee(s) based on
-- performance rating and monthly income.
-- ==========================================================

SELECT
    employee_id,
    department,
    performance_rating,
    monthly_income
FROM employee_featured
WHERE performance_rating =
(
    SELECT MAX(performance_rating)
    FROM employee_featured
)
ORDER BY monthly_income DESC;




SELECT DISTINCT attrition_status
FROM employee_featured;