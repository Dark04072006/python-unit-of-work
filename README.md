## Unit of Work Example in Python

This is an example implementation of the "Unit of Work" pattern.

Please note that this code is not optimal and has known limitations. It should be considered only as educational material, not as production-ready code.

In this example, you will see:

* **Unit of Work**, which has its own copy of the mapper registry and tracks affected models.
* **A fake data mapper implementation** to show when it is called.
* **A dataclass used as an anemic domain model**.
* **An example of some business logic and a database gateway for it**.

### Detailed Description

1. **Unit of Work**:
    - The Unit of Work component is responsible for managing transactions and tracking changes in models. It ensures that all operations within a business transaction are executed or none are.
    - It keeps its own copy of the mapper registry and maintains lists of new, changed, and removed objects.
    - At the end of a business transaction, it uses these lists to execute all the necessary database operations in a single transaction.

2. **Data Mapper**:
    - A fake implementation of the DataMapperProtocol interface that shows when insert, update, and delete methods are called. This allows us to see how the Unit of Work interacts with the mappers.
    - The data mapper is responsible for transferring data between the application and the database. It abstracts the database interactions from the rest of the application.

3. **Anemic Domain Model**:
    - Using dataclass to define the user model (User). This model represents the domain entity and contains the data and methods to manage its state, such as adding and removing posts.
    - The model itself is "anemic" because it lacks business logic, which is instead managed by services or use cases.

4. **Business Logic and Database Gateway**:
    - An example of business logic that includes creating, saving, and deleting users. This logic is encapsulated in a service or a gateway, which coordinates operations between the domain models and the data mappers.
    - A database gateway that uses the Unit of Work and data mapper to perform operations on users. The gateway provides an interface for the application to interact with the database in a transactional way.
