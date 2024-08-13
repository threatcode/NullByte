# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set the working directory inside the container
WORKDIR /app

# Update the package list and install Git
RUN apt-get update && apt-get install -y git

# Clone the NullByte repository
RUN git clone https://github.com/threatcode/NullByte.git

# Change directory to NullByte
WORKDIR /app/NullByte

# Make the install script executable
RUN chmod +x install

# Run the install script; if 'sh install' fails, try './install'
RUN sh install || ./install

# Entry point for the container (optional)
CMD ["bash"]
