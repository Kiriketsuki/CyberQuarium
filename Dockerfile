# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project files to the container
COPY . .

# Build the project

RUN npm run build

EXPOSE 4173

# Set the command to start the app
CMD [ "npm", "run", "preview","--", "--host"]
