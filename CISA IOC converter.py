import json
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

IOC_Path = r"C:\...\IOC.json"
Export_Path = r"C:\...\Converted_Indicators.json"

# Load the IOC JSON data
with open(IOC_Path, 'r') as file:
    IOC_data = json.load(file)

# Function to convert an IOC object to the Indicator template format
def convert_to_indicator_template(IOC_object):
    # Set the valid_until date to 2 years from the created date
    created_date = parse(IOC_object.get("created"))
    valid_until_date = created_date + relativedelta(years=2)
    
    indicator_template = {
        "type": IOC_object.get("type"),
        "spec_version": IOC_object.get("spec_version"),
        "pattern_type": IOC_object.get("pattern_type"),
        "id": IOC_object.get("id"),
        "created": IOC_object.get("created"),
        "modified": IOC_object.get("modified"),
        "name": IOC_object.get("name"),
        "pattern": IOC_object.get("pattern"),
        "valid_from": IOC_object.get("valid_from"),
        "valid_until" : valid_until_date.isoformat(),
        "confidence" : 100
        # Include other fields from the template as needed
    }
    return indicator_template

# Convert each IOC object and store the results
converted_indicators = [convert_to_indicator_template(obj) for obj in IOC_data['objects'] if obj.get("type") == "indicator"]

# Save the converted data to a new JSON file
with open(Export_Path, 'w') as outfile:
    json.dump(converted_indicators, outfile, indent=4)
