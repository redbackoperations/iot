# ==== CONFIGURE =====

# Use a Node 18 base image
FROM node:18-alpine

# Set the working directory to /app inside the container
WORKDIR /app

# Copy app files
COPY . .

# ==== BUILD =====

# Install dependencies (npm ci makes sure the exact versions in the lockfile gets installed)
RUN npm install

# Build the app
RUN npm run build

# ==== RUN =======

# Set the env to "production"
ENV NODE_ENV production

EXPOSE 3000

# Start the app
CMD [ "npm", "start"]
