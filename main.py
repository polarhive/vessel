import argparse
import json
from lxml import etree

SENSITIVE_FIELDS = [ 'firstInstallTime', 'lastUpdateTime', 'signature' ]

def remove_sensitive_info(package_data):
    for field in SENSITIVE_FIELDS:
        if field in package_data:
            del package_data[field]
    return package_data

def export_to_json(packages, json_file_path, include_sensitive_info=True):
    if not include_sensitive_info:
        packages = [remove_sensitive_info(pkg) for pkg in packages]
    with open(json_file_path, "w") as json_file:
        json.dump(packages, json_file, indent=4)
    print(f"JSON data successfully saved to {json_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Process package data from an XML file.")
    parser.add_argument("xml_file", help="The XML file to process.")
    parser.add_argument("-r", "--remove", action="store_true", help="Remove private information like install times.")
    parser.add_argument("-p", "--pkgnames", action="store_true", help="Export only package names.")
    parser.add_argument("-j", "--json", help="Export to JSON file.")
    args = parser.parse_args()

    # Read XML
    try:
        with open(args.xml_file, "rb") as xml_file: xml_content = xml_file.read()
        root = etree.XML(xml_content)
    except Exception as e:
        print(f"Error reading XML file: {e}")
        return

    # Extract data
    packages = []
    for package in root.findall('package'):
        package_data = dict(package.attrib)
        packages.append(package_data)

    if args.pkgnames: packages = [{"name": pkg['name']} for pkg in packages]
    if args.json: export_to_json(packages, args.json, not args.remove)
    if not args.json:
        print(f"Total packages: {len(packages)}")
        for pkg in packages: print(f"- {pkg['name']}")

if __name__ == "__main__":
    main()
