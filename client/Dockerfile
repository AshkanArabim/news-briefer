FROM node:alpine

# dir src: https://github.com/nodejs/docker-node/blob/main/README.md#npm-run
WORKDIR /home/node/app 

COPY . .

RUN npm install

CMD ["npm", "start"]
