# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set the working directory inside the container
WORKDIR /app

# Update the package list and install Git and other dependencies
RUN apt-get update && apt-get install -y git

# Install the 'yes' command to simulate input
RUN apt-get install -y yes

# Clone the NullByte repository
RUN git clone https://github.com/threatcode/NullByte.git

# Change directory to NullByte
WORKDIR /app/NullByte

# Make the install script executable
RUN chmod +x install

# Use 'yes' to automatically answer 'Y' to all prompts in the install script
RUN yes Y | sh install || yes Y | ./install

# Entry point for the container (optional)
CMD ["bash"]
