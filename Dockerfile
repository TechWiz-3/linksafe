FROM python:latest

# Add our script to the container's root directory
ADD ./src /src

# Make our python file executable
RUN chmod +x /src/scan_file.py

# Run the python file
ENTRYPOINT ["/src/scan_file.py"]
