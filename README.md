
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

This returns the index in the metadata of the JSON file corresponding to the provided key.

#### Returns: integer

Example:
```py
  metadata_key = "ra"
  index = get_metadata_index(metadata_key)
```

This will get the metadata index for the right ascension column.

## get_star_data(index)

| Argument    | Type        | Description |
| ----------- | ----------- |-------------|
| index      | Integer       | The index of the star to get data for |

This will get the data for a specific star in the JSON file.

#### Returns: numpy array

Example:
```py
  data = get_star_data(0)
```

This will return all the available data for the first star in the JSON file.

## get_dec():

This will return an array of all declination within the data

#### Returns: numpy array

## get_ra():

This will return an array of all right-ascensions within the data

#### Returns: numpy array

## get_pmra():

This will return an array of all right-ascension proper motions within the data

#### Returns: numpy array

## get_pmdec():

This will return an array of all declination proper motions within the data

#### Returns: numpy array

## get_parallax():

This will return an array of all parallaxes within the data

#### Returns: numpy array

