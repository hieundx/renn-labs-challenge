# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install the dependencies specified in requirements.txt
RUN pip install streamlit llama_index python-dotenv

# Copy the rest of the application code into the container at /app
COPY ./chat.py .
COPY ./.env .

# Expose the port that the application will run on
EXPOSE 8501

# Specify the command to run the application
CMD ["streamlit", "run", "chat.py"]