# Use Nginx image to serve static files
FROM nginx:alpine

# Copy frontend files to Nginx public directory
COPY frontend/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Command to run Nginx
CMD ["nginx", "-g", "daemon off;"]
