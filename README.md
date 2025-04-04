### Bank account withdrawal code improvement

After reviewing the code, I identified several areas that could be improved for better security, maintainability,
and scalability.

Having the opportunity to rewrite this solution in a programming language Iʼm more comfortable with, Iʼve
chosen Python with Django Rest Framework (DRF). Django provides powerful features that make it a great
choice for this particular solution.

**Some of the benefits of Django**
- Built-in tools for unit testing and API testing
- Designed to handle complex business logic and large scale projects efficiently
- Follows a structured approach with reusable components
- Comes with built-in ORM and protections against SQL injection, CSRF, and XSS

#### Key Improvements

1. **Safer and More Maintainable Database Queries**
    - The original approach builds raw SQL queries as strings, which is not the most robust or secure way
    to interact with the database.
    - Writing complex SQL queries manually can be error-prone and difficult to maintain.
    - Djangoʼs ORM (Object Relational Mapping) provides a secure and optimised way to interact with the
    database while protecting against SQL injection.
    - ORM queries are also easier to read, modify, and optimise for performance.

2. **Atomic Transactions for Data Integrity**

    Django provides atomic transactions, ensuring that balance updates and event notifications are
    processed as a single unit. If any part of the transaction logic fails, all changes are rolled back,
    preventing inconsistent system states.

4. **Improved Error Handling and HTTP Responses**
   
    Instead of returning plain strings, the API should return proper HTTP response statuses. Structured error
    messages make debugging easier and improve API usability for clients.

6. **System Logging and Monitoring**
   
    Proper logging helps with support, debugging, and system monitoring. We can log important events,
    errors, and database operations to identify issues faster.

8. **Avoid Hardcoded Constants**
   
    Hardcoding values in code makes maintenance difficult. Instead, we can define constants for withdrawal
    states and error messages, ensuring consistency across the system.

10. **Use DRF Serializers for Data Validation**
    
    DRF serializers improve data integrity by validating inputs before processing. This prevents issues like
    invalid amounts, missing fields, or incorrect data formats.

#### Solution Breakdown

To improve maintainability and scalability, the solution will be modularized into separate components, each
handling a specific concern.

1. **Constants File**
    - Stores predefined status response messages. Avoids hardcoding strings inside business logic.
2. **URLs File**
    - Defines API endpoints.
    - Maps each endpoint to the corresponding view to handle the request.
3. **Serializers**
    - Handles data validation and transformation.
    - Ensures only valid requests reach the business logic.
4. **Views File**
    - Contains the business logic for handling API requests.
    - Ensures proper flow, validation, and response formatting.
    - Returns the request response.

**Assumptions**
- A BankAccount model has already been defined and migrated.
- The project settings file contains AWS_REGION and AWS_SNS_TOPIC_ARN for event notifications.


**Out of scope**
- Unit testing
- A running solution
- Authentication
- Queue System for Failed Transactions: In the future, we can implement a retry mechanism using a queue
to handle failed withdrawals.
