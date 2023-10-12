# Use an official Node.js runtime as the base image
FROM node:14

# Install the PostgreSQL client library
RUN apt-get update && apt-get install -y libpq-dev

# Set the working directory in the container
WORKDIR /app

# Copy your application files into the container
COPY package.json package-lock.json /app/
RUN npm install

# Copy the rest of your application code
COPY . /app

# Expose the port your application runs on
EXPOSE 5002

# Command to run your application
CMD ["node", "index.js"]
