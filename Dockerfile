FROM python:3.9

# Add our script to the container's root directory
ADD ./src/ /src/

# Make our python file executable
RUN chmod +x /src/scan_file.py
RUN chmod +x /src/link.py

RUN pip install requests

# Run the python file
ENTRYPOINT ["/src/scan_file.py"]
