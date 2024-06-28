# mobile_app_react/Dockerfile
FROM node:18.20-slim

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Start the React Native application
CMD ["npm", "start"]
