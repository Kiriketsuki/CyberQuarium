# Set the base image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y unixodbc-dev

# RUN apt-get update && apt-get install -y curl
# RUN apt-get update && apt-get install -y gnupg


# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
# RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
# RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# RUN apt-get update && apt-get install -y msodbcsql17
# RUN echo "[ODBC Driver 17 for SQL Server]" >> /etc/odbcinst.ini
# RUN echo "Description=Microsoft ODBC Driver 17 for SQL Server" >> /etc/odbcinst.ini
# RUN echo "Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1" >> /etc/odbcinst.ini



# Copy the Flask app code
COPY . .

# Set the environment variables 
ENV FLASK_APP=run.py

# Expose the Flask app port
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
