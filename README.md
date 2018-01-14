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
lob-api:
  description: Coding Test
  color: false
  file: <html template id>: if not specified defaults to basic template 
  html_variables:
    - var1
    - var2
```
#### auth
- lob-key : Specify lob api key (Required either here or via command line `lob-key`)
- civic-key : Specify google civic api key (Required either here via command line `civic-key`)
#### civic-api
- url: URL to use for google civic api (Optional: Defaults to https://www.googleapis.com/civicinfo/v2/representatives)
- Any other parameter and values as supported by Google Civic API can be added. All the parameter with corresponding values will be
used to make request
- Please do not change `field` parameter to anything else. Script might not work as expected
#### lob-api
- html_variables: list of variables in html template. Values of `var1`, `var2` are taken from json corresponding to `html_variables` 
in input json. If not specified value corresponding to key `message` is used from input json.
- Any other parameter and values as supported by Lob API can be added. All the parameter with corresponding values will be
used to make request

### Input file
Input Json file with following schema:
```json
{
  "name": "name",
  "address_line1": "addr1",
  "address_line2": "addr2",
  "address_city": "city",
  "address_zip": "zip",
  "address_state": "state",
  "html_variables": {
      "var1": "val1",
      "var2": "val2"
  }
}
```
Note:
- Required keys: name, address_line1, address_city, address_zip, address_state
- Mention all the variables that you want to merge with your template in `html_variables`, any variable mentioned which isn't
a part of html template will be silently ignored
- In case of default html template only ``message`` variable is needed and it can be passed a directly or as a part of  
of ``html_variables`` in input json