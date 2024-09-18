## Stacklok QA

This repo aims to be home to tests and automation for Stacklok in general.

Tests are written using the [Robot Framework](https://robotframework.org/) with
Python as a helper language for writing custom libraries.

### Requirements

- Docker/Podman
- [Task](https://taskfile.dev/#/installation)

### Running tests

To run the tests, you can use the following command:

```bash
task test
```

You may also pass extra arguments to the `robot` command by using
`--`. e.g. to run only the `smoke` tests:

```bash
task test -- -i smoke
```

### Writing tests

Tests are written in the `<component>-tests` directory. Each test suite should have its own
directory with the following structure:

```
<component>-tests/
├── <component>-tests.robot
```

The test suite should have the following structure:

```robot
*** Settings ***

Library  resources/<library>.py

*** Variables ***

${VARIABLE}  value

*** Test Cases ***
Test case name
    [Documentation]  Description of the test case
    [Tags]  smoke
    Keyword  ${VARIABLE}
```

We're aiming to use a BDD approach to writing tests, so the test cases should be written in a
Gherkin-like syntax. The test cases should be written in the `<component>-tests.robot` file.

```robot
*** Test Cases ***
Valid user login
    [Documentation]  A user exists
    [Tags]  smoke
    Given a user exists
    When the user logs in
    Then the user is logged in
```


### Writing custom libraries

Custom libraries are written in the `resources` directory. Each library should have its own
file or directory with the following structure:

```
resources/
├── <library>.py
```
