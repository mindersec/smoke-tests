*** Settings ***
Library    OperatingSystem
Library    BuiltIn
Library    RequestsLibrary

Library    resources.helpers
Library    resources.projects.Projects
Library    resources.providers.Providers
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.repositories_service.RepositoriesService
Library    resources.github.GitHub
Library    resources.minderlib

Suite Setup    Set Rest Base URL From Config

Test Setup    Default Setup
Test Teardown    Default Teardown

*** Keywords ***
Default Setup
    Set Provider as Environment Variable with Test Name
    Set Project as Environment Variable with Test Name
    ${MINDER_TEST_ORG}=    Get Environment Variable    MINDER_TEST_ORG
    Set Suite Variable    $MINDER_TEST_ORG

Default Teardown
    Remove Provider Environment Variable for Test
    Remove Project Environment Variable for Test

Set Rest Base URL From Config
    [Documentation]    Reads the BASE_URL from the config file and sets it for all tests.
    ${BASE_URL}=    Get Rest URL From Config
    Set Suite Variable    ${BASE_URL}

Set Provider as Environment Variable with Test Name
    [Documentation]    Set the MINDER_PROVIDER environment variable to the first github-app provider

    # We might want to make this more dynamic in the future, but for now this is good enough
    ${GITHUB_APP_PROVIDER}=    Get Github App Provider ID
    Set Environment Variable    MINDER_PROVIDER    ${GITHUB_APP_PROVIDER}

Remove Provider Environment Variable for Test
    [Documentation]    Remove the provider environment variable after the test.
    Remove Environment Variable    MINDER_PROVIDER

Set Project as Environment Variable with Test Name
    [Documentation]  Set the environment variable for the current test and log the test name.
    ${test_name}=    Create Minder Project With Test Name
    Set Environment Variable    MINDER_PROJECT    ${test_name}

Remove Project Environment Variable for Test
    [Documentation]    Remove the environment variable after the test.
    Remove Minder Project With Test Name
    Remove Environment Variable    MINDER_PROJECT

*** Test Cases ***
Test the List Repositories API
    [Documentation]    Test that we can list repositories

    When Client Lists Repositories
    Given Results Format Is Valid
    Then Results Are Empty

Test the List Repositories API with registered repo
    [Documentation]    Test that we can list repositories

    ${test_repo}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo}
    Given repo is registered    ${test_repo}

    When Client Lists Repositories
    ${results}=    Get Results
    Log    ${results}
    Given Results Format Is Valid
    Then Results length equals    1

    [Teardown]    Run Keywords    Delete repo    ${test_repo}
    ...           AND    Default Teardown

Test the List Repositories API with multiple registered repos
    [Documentation]    Test that we can list repositories

    ${test_repo1}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo2}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo3}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo4}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo5}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python

    Given a copy of repo    stacklok/demo-repo-python    ${test_repo1}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo2}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo3}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo4}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo5}

    Given repo is registered    ${test_repo1}
    Given repo is registered    ${test_repo2}
    Given repo is registered    ${test_repo3}
    Given repo is registered    ${test_repo4}
    Given repo is registered    ${test_repo5}

    When Client Lists Repositories
    ${results}=    Get Results
    Log    ${results}
    Given Results Format Is Valid
    Then Results length equals    5

    [Teardown]    Run Keywords    Cleanup Minder Repos
    ...           AND    Cleanup GitHub Repos
    ...           AND    Default Teardown
