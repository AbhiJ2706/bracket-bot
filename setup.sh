#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install and enable SSH service
echo "Installing and enabling SSH service..."
sudo apt install -y ssh
sudo systemctl enable ssh
sudo systemctl start ssh

# Check SSH service status
echo "Checking SSH service status..."
sudo SYSTEMD_PAGER='' systemctl status ssh

# Install Python development packages
echo "Installing Python development packages..."
sudo apt install -y python3-dev python3-pip python3-venv

# Create a Python virtual environment in the home directory
echo "Creating a Python virtual environment..."
cd ~
python3 -m venv .venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source ~/.venv/bin/activate

# Make the virtual environment activate automatically in new terminals
echo "Configuring automatic virtual environment activation..."
echo 'source ~/.venv/bin/activate' >> ~/.bashrc

# Install RPi.GPIO and lgpio libraries inside the virtual environment
echo "Installing RPi.GPIO and lgpio libraries..."
pip install RPi.GPIO rpi-lgpio

# Install Adafruit LSM6DS library
echo "Installing Adafruit LSM6DS library..."
pip install adafruit-circuitpython-lsm6ds

# Install ODrive package
echo "Installing ODrive package..."
pip install odrive==0.5.1.post0

# Patch the ODrive package baud rate
echo "Patching the ODrive package baud rate..."
SED_PATH=$(python -c "import fibre; import os; print(os.path.join(os.path.dirname(fibre.__file__), 'serial_transport.py'))")
sed -i 's/DEFAULT_BAUDRATE = 115200/DEFAULT_BAUDRATE = 460800/' "$SED_PATH"

# Run ODrive udev setup
echo "Running ODrive udev setup..."
ODRIVE_TOOL_PATH=$(which odrivetool)
sudo "$ODRIVE_TOOL_PATH" udev-setup

# Add current user to dialout and audio groups
echo "Adding current user to 'dialout' and 'audio' groups..."
sudo usermod -a -G dialout,audio $USER

# Configure boot settings
echo "Configuring boot settings..."
sudo sh -c 'printf "\nenable_uart=1\ndtoverlay=uart1-pi5\n" >> /boot/firmware/config.txt'

# Install git
echo "Installing git..."
sudo apt install -y git

# Clone the BracketBot quickstart repository
echo "Cloning the BracketBot quickstart repository..."
cd ~
git clone https://github.com/BracketBotCapstone/quickstart
cd quickstart

# Inform the user about the calibration step
echo "Please ensure the ODrive is connected via USB before proceeding."
read -p "Press Enter to run the calibration script..."

# Install required Python packages
echo "Installing required Python packages..."
pip install numpy sympy control matplotlib pyserial

# Run the calibration script
echo "Running the ODrive calibration script..."
python calibrate_odrive.py

echo "Setup complete! You may need to reboot your system for all changes to take effect."
