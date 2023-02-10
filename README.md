
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

## get_metadata_index(key)

| Argument    | Type        | Description |
| ----------- | ----------- |-------------|
| key      | String       | The name of the column listed in the JSON files, e.g. "pmra" for proper motion right ascension |

This returns the index in the metadata of the JSON file corresponding to the provided key

#### Returns: integer

Example:
```py
  metadata_key = "ra"
  index = get_metadata_index(metadata_key)
```

This will get the metadata index for the right ascension column
