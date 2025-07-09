import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { createClient } from 'redis';
import { io } from 'socket.io-client';
import { typeDefs, resolvers } from './schema.js';

const WS_ENDPOINT = process.env.WS_ENDPOINT || 'ws://localhost:8010';
const REDIS_HOST = process.env.REDIS_HOST || 'localhost';

async function main() {
  const redis = createClient({ url: `redis://${REDIS_HOST}:6379` });
  redis.on('error', (err) => console.error('Redis error', err));
  await redis.connect();

  const server = new ApolloServer({ typeDefs, resolvers: resolvers(redis) });
  const { url } = await startStandaloneServer(server, { listen: { port: 8030 } });
  console.log(`🚀 Twin-core ready at ${url}`);

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
