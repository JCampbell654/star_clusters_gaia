
# Internal dynamics of star clusters with Gaia

Internal dynamics of star clusters using the Gaia mission archive

# Documentation

## Data handler library

This library allows the user to pull data directly from Gaia archive JSON files and converts it into a usable format consisting of numpy arrays.

## select_file(path)

| Argument    | Type        | Description |
| ----------- | ----------- |-------------|
| path      | String       | The path containing the desired JSON file |

This selects a JSON file to get the data from. This must be done before attempting to extract any data using any other methods.
Note: The path starts from the location of the file.

Example:
```py
  select_file("Data/1675856164509O-result.json")
```
In this case, the script running the method would be in the same location as the folder ```Data``` containing the JSON file.
