# Stage 1: Build the application
FROM node:18-alpine AS build

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Set the working directory inside the container
WORKDIR /app

# 1. Clean npm cache before installing dependencies
RUN npm cache clean --force

# 2. If you have a lock file, use `npm ci` for a clean install
# If package-lock.json exists, `npm ci` will install dependencies cleanly
RUN npm install

# 3. If using `npm install` instead of `npm ci`, force clear node_modules just in case
# RUN rm -rf node_modules && npm install --no-audit --no-fund

# Copy the rest of the application code
COPY . .

# Accept argument during build
ARG OPENAI_API_KEY

# Set environment variable
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Expose the port on which the application will run
EXPOSE 3000

# Start the application
CMD ["npm", "run", "dev"]