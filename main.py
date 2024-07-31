import json
from datetime import datetime, date

# Function to add a new diary entry
def add_entry(entries, text):
    # Generate the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Create a new entry with the provided text and current timestamp
    entry = {"text": text, "timestamp": timestamp, "modified": None, "tags": []}
    # Append the new entry to the entries list
    entries.append(entry)
    return entries

# Function to view diary entries
def view_entries(entries, start_date=None, end_date=None):
    # Filter entries by date range if specified
    filtered_entries = entries
    if start_date and end_date:
        filtered_entries = [
            entry for entry in entries
            if start_date <= datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").date() <= end_date
        ]
    # Display each entry with its timestamp and tags
    for i, entry in enumerate(filtered_entries, start=1):
        print(f"{i}. {entry['timestamp']} - {entry['text']} (Tags: {', '.join(entry['tags'])})")

# Function to edit an existing diary entry
def edit_entry(entries, entry_index, new_text):
    # Update the entry's text and set the modification timestamp
    entries[entry_index]["text"] = new_text
    entries[entry_index]["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return entries

# Function to delete a diary entry
def delete_entry(entries, entry_index):
    # Prompt user for confirmation before deletion
    confirm = input("Are you sure you want to delete this entry? (y/n): ")
    if confirm.lower() == 'y':
        # Remove the entry from the list
        entries.pop(entry_index)
        print("Entry deleted.")
    else:
        print("Deletion canceled.")
    return entries

# Function to filter entries by a specific date range
def filter_entries_by_date_range(entries, start_date, end_date):
    return [
        entry for entry in entries
        if start_date <= datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S").date() <= end_date
    ]

# Function to calculate the number of days between two entries
def days_between_entries(entry1, entry2):
    # Convert timestamps to datetime objects
    date1 = datetime.strptime(entry1["timestamp"], "%Y-%m-%d %H:%M:%S")
    date2 = datetime.strptime(entry2["timestamp"], "%Y-%m-%d %H:%M:%S")
    # Calculate the difference in days
    delta = date2 - date1
    return abs(delta.days)

# Function to search diary entries by keyword
def search_entries(entries, keyword):
    # Return entries where the keyword is found in the text
    results = [entry for entry in entries if keyword.lower() in entry["text"].lower()]
    return results

# Function to tag an entry with keywords
def tag_entry(entries, entry_index, tags):
    # Add the provided tags to the specified entry
    entries[entry_index]["tags"].extend(tags)
    return entries

# Function to export entries to a file
def export_entries(entries, file_format='txt'):
    filename = f"diary_entries.{file_format}"
    with open(filename, 'w') as f:
        # Write each entry to the file with its timestamp and tags
        for entry in entries:
            f.write(f"{entry['timestamp']} - {entry['text']} (Tags: {', '.join(entry['tags'])})\n")
    print(f"Entries exported to {filename}.")

# Function to save entries to a JSON file
def save_entries(entries, filename='entries.json'):
    with open(filename, 'w') as f:
        # Convert entries to a JSON format and write to the file
        json.dump(entries, f)

# Function to load entries from a JSON file
def load_entries(filename='entries.json'):
    try:
        # Read entries from the file
        with open(filename, 'r') as f:
            entries = json.load(f)
    except FileNotFoundError:
        # Return an empty list if the file does not exist
        entries = []
    return entries

# Main application loop
if __name__ == "__main__":
    entries = load_entries()  # Load existing entries from the file

    while True:
        print("\nPersonal Diary Application")
        print("1. Add Entry")
        print("2. View Entries")
        print("3. Edit Entry")
        print("4. Delete Entry")
        print("5. Filter Entries by Date Range")
        print("6. Calculate Days Between Entries")
        print("7. Search Entries")
        print("8. Tag Entry")
        print("9. Export Entries")
        print("10. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            # Add a new entry
            text = input("Enter your diary entry: ")
            entries = add_entry(entries, text)
        elif choice == '2':
            # View all or filtered entries
            view_entries(entries)
        elif choice == '3':
            # Edit an existing entry
            index = int(input("Enter the entry number to edit: ")) - 1
            new_text = input("Enter new text: ")
            entries = edit_entry(entries, index, new_text)
        elif choice == '4':
            # Delete an entry
            index = int(input("Enter the entry number to delete: ")) - 1
            entries = delete_entry(entries, index)
        elif choice == '5':
            # Filter entries by date range
            start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
            end_date = datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d").date()
            filtered_entries = filter_entries_by_date_range(entries, start_date, end_date)
            view_entries(filtered_entries)
        elif choice == '6':
            # Calculate days between two entries
            index1 = int(input("Enter the first entry number: ")) - 1
            index2 = int(input("Enter the second entry number: ")) - 1
            days = days_between_entries(entries[index1], entries[index2])
            print(f"Days between entries: {days}")
        elif choice == '7':
            # Search entries by keyword
            keyword = input("Enter keyword to search: ")
            results = search_entries(entries, keyword)
            for i, entry in enumerate(results, start=1):
                print(f"{i}. {entry['timestamp']} - {entry['text']} (Tags: {', '.join(entry['tags'])})")
        elif choice == '8':
            # Tag an entry with keywords
            index = int(input("Enter the entry number to tag: ")) - 1
            tags = input("Enter tags separated by commas: ").split(',')
            tags = [tag.strip() for tag in tags if tag.strip()]
            entries = tag_entry(entries, index, tags)
        elif choice == '9':
            # Export entries to a file
            format = input("Enter file format (txt or pdf): ")
            export_entries(entries, format)
        elif choice == '10':
            # Save entries to the file and exit
            save_entries(entries)
            break
        else:
            print("Invalid option, please try again.")