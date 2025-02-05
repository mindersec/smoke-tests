*** Settings ***
Documentation       Test suite for the Minder data sources REST API

Resource   resources/keywords.robot
Library    resources.datasources.DataSources

Suite Setup    Load Config

Test Setup    Default Setup
Test Teardown    Default Teardown

*** Keywords ***
Default Setup
    Set Project as Environment Variable with Test Name

Default Teardown
    Remove Project Environment Variable for Test

*** Test Cases ***
Test the List Data Sources API
    [Documentation]    Test that we can list data sources

    ${data_sources}=    When Client lists data sources
    Then data sources are empty    ${data_sources}

    [Teardown]    Run Keywords   Default Teardown

Test the Create Data Source API
    [Documentation]    Test that we can create a data source

    Given Client adds a data source    test-data-source
    ${data_sources}=    When Client lists data sources
    Then data sources are not empty    ${data_sources}

    [Teardown]    Run Keywords    Cleanup Minder Data Sources
    ...           AND    Default Teardown

Test the Update Data Source API
    [Documentation]    Test that we can modify an existing data source

    Given Client adds a data source    test-data-source
    Given Client updates a data source    test-data-source
    ${data_sources}=    When Client lists data sources
    Then data sources are not empty    ${data_sources}

    [Teardown]    Run Keywords    Cleanup Minder Data Sources
    ...           AND    Default Teardown