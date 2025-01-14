# Step 1: Use a Node.js base image for building the application
FROM node:18 as build

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy p    ackage.json and package-lock.json to the working directory
COPY package*.json ./

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of the application source code to the working directory
COPY . .

# Step 6: Build the Angular app for production
RUN npm run build --prod

# Step 7: Use an Nginx base image for serving the Angular app
FROM nginx:alpine

# Step 8: Copy the built files from the previous stage to the Nginx HTML directory
COPY --from=build /app/dist/matdash /usr/share/nginx/html

# Step 9: Expose port 80
EXPOSE 80

# Step 10: Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
