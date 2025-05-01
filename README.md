# 2025s1comp9120-a2

## Tasks

Complete the following:

1. checkLogin (for login)
2. getCarSalesSummary (for viewing car sales summary)
3. findCarSales (for finding car sales)
4. addCarSale (for adding a car sale)
5. updateCarSale (for updating a car sale)

## Constraints

### Login Page

1. Username should be **case insensitive**

### Summary Page

1. The list of car sales must be ordered by make name and model name in ascending order
   - Make: The name of the car’s brand (e.g. Toyota, Ford, BMW, etc)
   - Model: The name of a specific type of a car produces by a manufacturer. (e.g. Rav4, NX, etc)
   - Available Units: The number of units of that specific make and model that are still available for sale.
   - Sold Units: The number of units of that make and model that have been sold to customers.
   - Total Sales ($) : The total revenue generated from the sold units of that make and model.
   - Last Purchased At: The date when the last car of that make and model was sold. It needs to be display in the Australian date convention (Date-Month-Year).
     Figure

## To-Do

- [x] Setup git repo
- [ ] Delegate works

## Rubrics

| Criterion                   | No/Part Marks (0–1.5 pts unless stated)                                                   | Full Marks (2–2.5 pts unless stated)                                        |
| --------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Login                       | Can log in with user `jdoe` and validate credentials                                      | All valid users can log in; invalid users are rejected                      |
| View CarSales Summary       | Displays summary (e.g., Figure 3)                                                         | Correctly displays full summary in required order                           |
| Find CarSales               | Lists results for keyword “ro” (e.g., Figure 5)                                           | Lists correct results for all keywords in the correct order                 |
| Add CarSale                 | Can add a valid car sale record                                                           | Adds all valid records; invalid details are rejected                        |
| Update CarSale              | Can update the **status** of a car sale                                                   | Can update **all details**, ensuring updated values are valid               |
| Stored Procedure / Function | A couple of stored procedures/functions are included in SQL file                          | Procedures are also correctly called in **two of five specified functions** |
| Group Record Keeping (1 pt) | One or more issues with member contribution or missing Canvas meeting records (**0 pts**) | No issues; all members contribute and maintain Canvas diary (**1 pt**)      |
