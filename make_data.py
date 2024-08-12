import os
import csv
from docx import Document


def build_data_structure(base_path):
    data = {}

    # Iterate over each main category (e.g., al-kareum, east-kareum, ut-kareum)
    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)
        if os.path.isdir(category_path):
            data[category] = {}

            # Iterate over each subcategory (e.g., attraction, dining, entertainment, stay)
            for subcategory in os.listdir(category_path):
                subcategory_path = os.path.join(category_path, subcategory)
                if os.path.isdir(subcategory_path):
                    data[category][subcategory] = {}

                    # Iterate over each .docx file in the subcategory
                    for location_id, file_name in enumerate(sorted(os.listdir(subcategory_path))):
                        if file_name.endswith('.docx'):
                            file_path = os.path.join(subcategory_path, file_name)

                            # Read the content of the .docx file
                            document = Document(file_path)
                            content = '\n'.join([para.text for para in document.paragraphs])

                            # Extract location name from the file name
                            location_name = file_name.replace('_.docx', '').strip()

                            # Store the content in the data structure
                            data[category][subcategory][location_id] = {
                                'location_name': location_name,
                                'location_description': content
                            }

    return data


def save_to_csv(data, csv_file_path):
    # Define the CSV headers
    headers = ['location_id', 'region_name', 'category_name', 'location_name', 'location_description']

    # Write data to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        # Iterate over the data structure and write to CSV
        for category, subcategories in data.items():
            for subcategory, locations in subcategories.items():
                for location_id, location_info in locations.items():
                    row = {
                        'location_id': location_id,
                        'region_name': category,
                        'category_name': subcategory,
                        'location_name': location_info['location_name'],
                        'location_description': location_info['location_description']
                    }
                    writer.writerow(row)


# Example usage
base_path = 'kareumstay'
csv_file_path = 'data/locations.csv'

data = build_data_structure(base_path)
print(data['al-kareum']['stay'][0])

save_to_csv(data, csv_file_path)

print(f"Data has been saved to {csv_file_path}.")
