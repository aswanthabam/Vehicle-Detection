# Use Node.js LTS version as the base image
FROM node:14 as builder

# Set the working directory inside the container
WORKDIR /client

# Copy package.json and package-lock.json (if present) to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project directory to the working directory
COPY . .

# Build the React app for production
RUN npm run build

# Use Nginx to serve the built React app
FROM nginx:alpine

# Copy the built React app from the builder stage to the Nginx server directory
COPY --from=builder /client/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Command to start Nginx when the container starts
