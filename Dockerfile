FROM python:3.9

# Add our script to the container's root directory
ADD ./src/ /src/

# Make our python file executable
RUN chmod +x /src/scan_file.py
RUN chmod +x /src/link.py

# Run the python file
ENTRYPOINT ["/src/scan_file.py"]
