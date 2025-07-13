FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json ./
# Install all dependencies including devDependencies for the build
RUN npm install
COPY src ./src
# Compile TypeScript sources
RUN npm run build
# Remove development dependencies after build
RUN npm prune --production
EXPOSE 8030
CMD ["node", "dist/index.js"]
