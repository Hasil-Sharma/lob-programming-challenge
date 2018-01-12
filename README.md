# lob-programming-challenge

Command Line Interface to send a letter to your legislator with Lob.

## Getting Started:
Start with installing project requirements as specified in `requirement.txt` 
```shell
pip install -r requirement.txt
```
For running application use the following format.
```shell
python lob-letter-driver.py [options]
```

Possible options are as follow:
```shell
python lob-letter-driver.py -h
Usage: lob-letter-driver.py [options]

Options:
  -h, --help            show this help message and exit
  -c CONFIG, --config=CONFIG
                        YAML configuration file containing API key(s) and
                        other configurations
  -g CIVIC_KEY, --civic-key=CIVIC_KEY
                        Google Civic API Key (Overrides --config value)
                        (Required in either --config or here)
  -l LOB_KEY, --lob-key=LOB_KEY
                        Lob API Key, (Overrides --config value) (Required in
                        either --config or here)
  -f INPUT_FILE, --file=INPUT_FILE
                        Json file to read input (Mandatory)
  -i HTML_ID, --html-id=HTML_ID
                        ID of saved HTML template (Overrides --config
                        specified).Defaults to default template of single
                        variables {{message}}
  -v, --verbose         Print verbose messages


```

Note: 
- Specifying an input file along with api authentication key(s) in either configuration file or via command 
line options is mandatory
- In case `--html-id` or `-i` is not specified, the script defaults to:
    ```html
    <html style="padding-top: 3in; margin: .5in;">{{message}}</html>
    ``` 
- In case of default html template it is mandatory to include ``{{message}}`` variable in input json. Can be specified under ``html_variables`` as well

### Configuration file
YAML based configuration file with structure as follows:
```yaml
auth:
  lob-key: <specify lob-key>
  civic-key: <specify civic-key>
civic-api:
  url: https://www.googleapis.com/civicinfo/v2/representatives
  roles:
    - legislatorLowerBody
    - judge
  .
  .
  .
  Any paramater supported by Google Civic API
lob-api:
  description: Coding Test
  color: false
  file: <html template id>: if not specified defaults to basic template 
  html_variables:
    - var1
    - var2
    .
    .
    .
    Variables as specified in html template (should be same as specified in "html_variables" in input
  .
  .
  .
  Any paramter supported by Lob API
```
#### auth
- lob-key : Specify lob api key (Required either here or via command line `lob-key`)
- civic-key : Specify google civic api key (Required either here via command line `civic-key`)
#### civic-api
- url: URL to use for google civic api (Optional: Defaults to https://www.googleapis.com/civicinfo/v2/representatives)
- Any other parameter and values as supported by Google Civic API. All the parameter with corresponding values will be
used to make request
- Please do not change `field` parameter to anything else. Script might not work as expected
#### lob-api
- html_variables: list of variables to sent to assign `merge_variables`. Values of `var1`, `var2` are taken from `html_variables` 
in input json
- Any other parameter and values as supported by Lob API. All the parameter with corresponding values will be
used to make request

### Input file
Input Json file with following schema:
```json
{
  "name": <name> (Required),
  "address_line1": <Addr1> (Required),
  "address_line2": <Addr2> (Optional),
  "address_city": <City> (Required),
  "address_zip": <Zip> (Required),
  "address_state": <State> (Required),
  "html_variables": {
      "var1": <var1>,
      "var2": <var2>,
      .
      .
      .
      Should have atleast all the variables as mentiond in ``html_variables`` in configuration
  }
}
```
Note: 
- In case of default html template only ``message`` variable is needed and it can be passed a direct key or subkey 
of ``html_variables`` in input json
- In case extra variables are mentioned in ``html_variables`` in json they are simply ignored and only keys specified 
in ``html_variables`` in configuration are passed to lob api 