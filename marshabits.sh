#!/bin/bash

# Get the current repository path
REPO_PATH=$(pwd)

# Create the executable file marsplaner
echo '#!/bin/bash
/usr/bin/python3 '"$REPO_PATH"'/marshabits.py' > ~/marshabits

# Make the file executable
chmod +x ~/marshabits

# Move the file to /usr/local/bin
sudo mv ~/marshabits /usr/local/bin/

# Output a message about successful installation
echo "marshabits installed. You can now run the program with the command 'marshabits'."
