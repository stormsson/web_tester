# Web Testing Utility

A **FAST** tool to start testing with selenium.


## Installation

The tester relies on a Docker image that can be built with
`docker build -t webtester:latest .`

## Usage

Run `docker run --rm -ti -v $(pwd):/app webtester:latest python main.py -h` in order to see all available options

### Fetching urls with basic authentication
All test urls can share a common basic auth configuration.
In order to use it, 2 env variables are checked: `BASIC_AUTH_USER` and `BASIC_AUTH_PWD`.
It is not necessary to add the basic auth in the urls provided in the yml file.

This allows the test file to be pushed in a repo without worrying about the credentials.

Example:

`docker run --rm -ti -v $(pwd):/app -e BASIC_AUTH_USER=myusername -e BASIC_AUTH_PWD=mypassword webtester:latest`


### Create a test session
1) create a `suite.yml` file, structured as the example provided `suite_example.yml`
2) run `docker run --rm -ti -v $(pwd):/app webtester:latest` from your project dir

by default the run only checks request validators, if you need to enable selenium testing run
2) run `docker run --rm -ti -v $(pwd):/app webtester:latest python main.py --selenium`


## Validators
All validators will have a `type` field, to define which validator is used.
In the `suite.yml` you can define two different types of validators:

**validators** will use Selenium as a driver for testing.
They are currently defined in `tester/selenium_validators.py`

**request_validators** will use python requests library in order to fetch the url
They are currently defined in `tester/request_validators.py`

### contains

```yml
-
    type: contains
    selector: h1
    contains: moment
```

| field | sample value | Description |
|-------|--------------|-------------|
| selector | h1 | css selector to use for the search |
| contains | text | **optional** if present the DOM element must contain this text |

### header

```yml
-
    type: header
    name: content-type
    contains: json
```

| field | sample value | Description |
|-------|--------------|-------------|
| name | content-type | name of the header to check |
| contains | text | **optional** if present the header must contain this text |

### http_status

When an url is provided, by default, the tester checks for an HTTP 200 response

```yml
-
    type: http_status
    is: 204
```

| field | sample value | Description |
|-------|--------------|-------------|
| is | 204 | http status to check |




## Custom configuration

| parameter | sample value | Description |
|-----------|--------------|-------------|
| pool_size | 4 | number of parallel processes |


## Current limitations
- Only chrome webdriver is available for the moment
- Only 1 validator is available

## Next steps
1. Add more webdrivers
2. Add more validators
3. add array to http_status validator
4. add tests