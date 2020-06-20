import os
import json
import csv
import xmltodict


def has_all(dictionary, attributes):
    """ Return true if the given dictionary contains non-None values for all of the attributes. """
    for attribute in attributes:
        if dictionary.get(attribute, None) is None:
            return False
    return True


def load_json_files(json_folder_pathname):
    """ Return an array containing all JSONs dictionaries from all JSON files in a given folder """
    if json_folder_pathname is None:
        raise ValueError("Path to folder is required to count all JSONs in a folder!")

    # this finds our JSON files in the given folder
    json_filepaths = [pos_json for pos_json in os.listdir(json_folder_pathname) if pos_json.endswith('.json')]

    if len(json_filepaths) < 1:
        raise FileNotFoundError(f"No JSON files found in '{json_folder_pathname}'")

    json_files = []

    # iterate over JSON files and load all JSON
    for js in json_filepaths:
        json_files.append(load_json_file(os.path.join(json_folder_pathname, js)))

    return json_files


def load_json_file(json_file_pathname, encoding="utf-8"):
    """ Return a dict representing the JSON in the given filepath """
    with open(json_file_pathname, encoding=encoding) as json_file:
        return json.load(json_file)


def save_json_file(data, filename, encoding="utf-8"):
    """ Save the given dictionary as the filename """
    with open(filename, "w", encoding=encoding) as f:
        try:
            json.dump(data, f, indent=4, sort_keys=True, default=str)
        except TypeError as e:
            if str(e) == "'<' not supported between instances of 'NoneType' and 'str'":
                raise KeyError("Can't serialize the key 'None' into a JSON file!")
            else:
                raise e
        f.close()


def flatten_json(json, collect_name=False, delim="_"):
    """ Turn a nested JSON into a flat JSON.
    - json : the input JSON
    - collect_name : collect the nested structure in the output field name
        - for example, flatten_json({"outer":{"inner": 3}}, collect_name=True) => {"outer_inner": 3}
        - by default, it is just {"inner": 3}
    - delim : the delimiter for collecting names, by default is an underscore
        - for example, flatten_json({"outer":{"inner": 3}}, collect_name=True, delim=".") => {"outer.inner": 3}"""
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], (name if collect_name else "") + str(a) + delim)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, (name if collect_name else "") + str(i) + delim)
                i += 1
        else:
            out[name[:-1]] = x

    flatten(json)
    return out


def load_json_from_csv(csv_filename, encoding="utf-8"):
    """Load a list of JSON objects from a CSV file.

    The keys of the JSON are the column headers and each
    object represents one row of the CSV.

    Args:
        csv_filename (str): The path to the CSV file.

    Returns:
        list: The list of JSON objects.

    Examples:
        >>> load_json_from_csv("spend_sheet.csv")
        [
            {"spend": 2310, "month": "January"},
            {"spend": 3500, "month": "February"},
        ]
    """
    csv_rows = []
    with open(csv_filename, encoding=encoding) as csv_file:
        # read CSV file
        all_rows = csv.DictReader(csv_file)
        row_headers = all_rows.fieldnames

        # for all rows, build a json object
        for row in all_rows:
            row_object = {}

            # iterate over the headers
            for key in row_headers:
                if key:
                    value = row[key]
                    row_object[key] = value
            csv_rows.append(row_object)
        return csv_rows


def save_json_to_csv(json_list, output_filename, columns=None, required_attributes=None, encoding="utf-8"):
    """Saves an array of json objects as a CSV file.

    The JSON object is flattened, and all keys are used as the column headers.
    Each row represents the data in a given JSON.

    Args:
        json_list (list of dict):
            The array of json objects to save.
            Each object corresponds to a row in the CSV.

        output_filename (str):
            The filename to save the CSV under.
            Must be suffixed with ".csv".

        columns (list of str, optional):
            Only these keys are saved as columns.
            Defaults to empty list.

        required_attributes (list of str, optional):
            Only save the json objects that contain ALL of these attributes.
            Defaults to empty list.
    """
    # initialize default mutable variables
    if columns is None:
        columns = []
    if required_attributes is None:
        required_attributes = []

    # flatten all json in array
    flattened = list(map(lambda x: flatten_json(x), json_list))

    # filter out records that don't contain our required attributes
    if len(required_attributes) > 0:
        flattened = list(filter(lambda x: has_all(x, required_attributes), flattened))

    # get all unique key names as the names for the columns
    # unless the columns are provided for us
    if len(columns) == 0:
        columns = [x for row in flattened for x in row.keys()]
        columns = list(set(columns))

    with open(output_filename, "w", newline="", encoding=encoding) as out_file:
        csv_w = csv.writer(out_file)
        csv_w.writerow(columns)
        # TODO - this messes up with special (non-ascii) characters

        # write all data for each row to file
        for input_row in flattened:
            row_data = map(lambda key: input_row.get(key, ""), columns)
            csv_w.writerow(row_data)


def xml_to_json(xml_data):
    try:
        return xmltodict.parse(xml_data, dict_constructor=dict)
    except Exception:
        raise