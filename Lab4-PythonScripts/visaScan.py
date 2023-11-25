import pyvisa as visa

# Create a VISA resource manager object.
rm = visa.ResourceManager()

# List all available VISA resources.
available_resources = rm.list_resources()

if not available_resources:
    print("No VISA instruments found.")
else:
    print("Available VISA instruments:")
    for resource in available_resources:
        print(resource)

# Close the resource manager (optional, as it will be automatically closed when the script exits).
rm.close()