FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json ./
RUN npm install --production
COPY src ./src
RUN npm run build
EXPOSE 8030
CMD ["node", "dist/index.js"]
