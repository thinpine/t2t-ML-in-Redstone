import json

def process_weights_by_class(json_filename):
    # Read the JSON file
    with open(json_filename, 'r') as f:
        data = json.load(f)

    # Extract the 2D array of weights
    weights_2d = data['weight_rom']['data']
    
    # Define the class names based on their indices
    class_names = ['inform', 'question', 'directive', 'commissive']

    # Process each class separately
    for i, class_name in enumerate(class_names):
        # Ensure we don't go out of bounds if data has fewer classes
        if i >= len(weights_2d):
            break
            
        class_weights = weights_2d[i]
        
        # Define output file names
        high_file = f'{class_name}_high_hex.hex'
        low_file = f'{class_name}_low_hex.hex'
        
        # Open output files
        with open(high_file, 'w') as f_high, open(low_file, 'w') as f_low:
            # Write the required header for both files
            f_high.write('v2.0 raw\n')
            f_low.write('v2.0 raw\n')
            
            # Process each weight in the current class
            for w in class_weights:
                # Get the 8-bit representation (handles negative numbers)
                val_8bit = w & 0xFF
                
                # Extract the high and low 4 bits (nibbles)
                high_nibble = (val_8bit >> 4) & 0xF
                low_nibble = val_8bit & 0xF
                
                # Write to files as hexadecimal strings
                f_high.write(f'{high_nibble:x}\n')
                f_low.write(f'{low_nibble:x}\n')
                
        print(f"Successfully generated {high_file} and {low_file}")

if __name__ == '__main__':
    process_weights_by_class('nb_weights_8bit.json')