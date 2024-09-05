# staffnet

## Why do a refactor?

The current StaffNet was done using Flask, which is a microframework. It was a good choice for the initial development, but as the project grew, it became harder to maintain and add new features. The main reasons for the refactor are:

- **Code organization**: Flask doesn't enforce any structure, which makes it hard to maintain as the project grows. Django has a well-defined structure that makes it easier to organize the code.

- **ORM**: Flask doesn't have an ORM, which makes it harder to work with the database. Django has a built-in ORM that makes it easier to work with the database.

- **Authentication and Authorization**: Flask doesn't have built-in support for authentication and authorization. Django has built-in support for authentication and authorization.

- **Admin interface**: Flask doesn't have a built-in admin interface. Django has a built-in admin interface that makes it easier to manage the application data.

- **Testing**: Flask doesn't have built-in support for testing. Django has built-in support for testing.

- **Integration with other Django apps**: We are planning to integrate StaffNet with other Django projects, so it makes sense to use Django for StaffNet as well.
