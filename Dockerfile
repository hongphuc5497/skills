FROM python:3.12-slim

WORKDIR /app

# Copy the website directory
COPY website/ /app/

# Expose port
EXPOSE 4321

# Serve with Python's built-in HTTP server
CMD ["python3", "-m", "http.server", "4321", "--directory", "/app"]
