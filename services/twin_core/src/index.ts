import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import express from 'express';
import promBundle from 'express-prom-bundle';
import { collectDefaultMetrics } from 'prom-client';
import http from 'http';
import { createClient } from 'redis';
import { io } from 'socket.io-client';
import { typeDefs, resolvers } from './schema.js';
import { authPlugin } from './auth.js';

const WS_ENDPOINT = process.env.WS_ENDPOINT || 'ws://localhost:8010';
const REDIS_HOST = process.env.REDIS_HOST || 'localhost';

async function main() {
  const redis = createClient({ url: `redis://${REDIS_HOST}:6379` });
  redis.on('error', (err) => console.error('Redis error', err));
  await redis.connect();

  const server = new ApolloServer({
    typeDefs,
    resolvers: resolvers(redis),
    plugins: [authPlugin()],
  });
  await server.start();

  collectDefaultMetrics();
  const app = express();
  app.use(promBundle({ includeMethod: true }));
  app.use(express.json());
  app.use('/', expressMiddleware(server));

  const httpServer = http.createServer(app);
  await new Promise<void>((resolve) => httpServer.listen(8030, resolve));
  console.log('🚀 Twin-core ready at http://localhost:8030/');

  const socket = io(WS_ENDPOINT);
  socket.on('connect', () => console.log('WS connected'));
  socket.on('entity_update', async (data: any) => {
    const key = `entity:${data.id}`;
    await redis.set(key, JSON.stringify(data));
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
