# stage 1: build react app using node.js
FROM node:alpine as build

# dir src: https://github.com/nodejs/docker-node/blob/main/README.md#npm-run
WORKDIR /home/node/app 
COPY ./package*.json ./
RUN npm install
COPY . .
RUN npm run build

# stage 2: set up nginx to server built app
FROM nginx:1
COPY --from=build /home/node/app/build /usr/share/nginx/html
COPY ./nginx.conf.template /etc/nginx/templates/
CMD envsubst '${BACKEND_URL}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'
