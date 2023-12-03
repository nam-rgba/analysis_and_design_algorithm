import csv
import random

def process_transaction_data(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
            reader = csv.reader(infile, delimiter=' ')
            writer = csv.writer(outfile, delimiter=',')

            for row in reader:
                # Filter out empty strings and convert each item to a dictionary with a random float value
                processed_row = {int(item): round(random.uniform(0.1, 1.0), 2) for item in row if item}
                
                # Write the processed row to the output file
                writer.writerow([processed_row])

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file_path = 'connect.txt'  
output_file_path = 'sample.csv'  

# process_transaction_data(input_file_path, output_file_path)

from collections import Counter

def generate_weight_table(input_file_path, output_file_path, delimiter=' ', lines_to_read=100):
    try:
        item_counts = Counter()

        # Read the first 100 lines from the file
        with open(input_file_path, 'r') as file:
            for _ in range(lines_to_read):
                line = file.readline()
                if not line:
                    break  # Break if end of file is reached
                items = line.strip().split(delimiter)
                item_counts.update(items)

        # Calculate the total number of transactions
        total_transactions = sum(item_counts.values())

        # Generate the weight table (dictionary)
        weight_table = {item: count / total_transactions for item, count in item_counts.items()}

        # Write the result to the output file
        with open(output_file_path, 'w') as output_file:
            for item, weight in weight_table.items():
                output_file.write(f"{item}: {weight}\n")

        return weight_table

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
input_file_path = 'connect.txt'  
output_file_path = 'weight.csv' 
lines_to_read = 100

weight_table = generate_weight_table(input_file_path, output_file_path, lines_to_read=lines_to_read)

# Print the generated weight table
print("Weight Table:")
for item, weight in weight_table.items():
    print(f"{item}: {weight}")
