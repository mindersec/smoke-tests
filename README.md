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

Since the tests run in a container, they need a `minder` Linux binary in the path.
If you're runninng on a non-Linux machine, you need to provide one with an environment variable:
```bash
MINDER_BINARY_PATH=/path/to/minder task test
```

### Authentication and environment selection

The `task test` command will authenticate using an offline token, by default using the `offline.token` file in the current directory. If you want to test against a different environment, you need to provide a configuration file that contains the endpoints and credentials for the environments you want to test against.

For example, to run the tests against the staging environment, you can use the following command:
```bash
MINDER_CONFIG=$(pwd)/staging-config.yaml MINDER_OFFLINE_TOKEN_PATH=$(pwd)/staging-offline.token task test
```

### Running against a local Minder instance

Similar to the previous section, you can run the tests against a local Minder instance by providing a configuration file and offline token. One catch is that if you run the tests from a container, you need to use `host.docker.internal` as the hostname to access the local Minder instance from inside the container.

```yaml
http_server:
  host: host.docker.internal
  port: 8080
grpc_server:
  host: host.docker.internal
  port: 8090
  insecure: true

identity:
  cli:
    issuer_url: http://localhost:8081
    realm: stacklok
    client_id: minder-cli
```

Confusingly, the `issuer_url` needs to be `localhost` as that corresponds to the hostname of the Keycloak instance inside the container.

### Extra arguments

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
