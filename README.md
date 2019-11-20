# Web Testing Utility

A **FAST** tool to start testing with selenium.


## Installation

The tester relies on a Docker image that can be built with
`docker build -t webtester:latest ./docker`

## Usage

### Create a test session
1) create a `suite.yml` file, structured as the example provided `suite_example.yml`
2) run `docker run --rm -ti -v $(pwd):/app webtester:latest python main.py`


## Validators
All validators will have a `type` field, to define which validator is used

### contains

```yml
-
    type: contains
    selector: h1
    contains: moment
```

| field | sample value | Description |
| selector | h1 | css selector to use for the search |
| contains | text | *optional* if present the DOM element must contain this text |

## Custom configuration

| parameter | sample value | Description |
| pool_size | 4 | number of parallel processes |


## Current limitations
- Only chrome webdriver is available for the moment
- Only 1 validator is available

## Next steps
1. Add more webdrivers
2. Add more validators