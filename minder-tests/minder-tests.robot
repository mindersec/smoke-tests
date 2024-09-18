*** Settings ***

Library    resources/minderlib.py

*** Variables ***

${server}    api.stacklok.com:443
${provider_class}   github-app

*** Test Cases ***

Valid login
    [Tags]    login   smoke
    Given I am logged into minder
    When I get the user profile
    Then the minder server should be    ${server}


Provider enrolled
    [Tags]    smoke
    Given I am logged into minder
    When I list my providers
    Then I should have at least one provider of class    ${provider_class}


Project created
    [Tags]    smoke
    Given I am logged into minder
    When I list my projects
    Then I should have at least one project