import { gql } from 'graphql-tag';
import { RedisClientType } from 'redis';

export const typeDefs = gql`
  type Query {
    portAreas: [PortArea]
    sensors(type: String): [Sensor]
    energyAssets: [EnergyAsset]
    bathyProfile(id: ID!): [BathyPoint]
  }

  type Subscription {
    entityUpdated: EntityUpdate
  }

  type PortArea { id: ID! name: String geometry: String }
  type Sensor   { id: ID! measuredProperty: String value: Float unit: String ts: String }
  type EnergyAsset { id: ID! soc: Float power_kw: Float ts: String }
  type BathyPoint  { id: ID! depth_m: Float lon: Float lat: Float ts: String }

  union EntityUpdate = Sensor | EnergyAsset | BathyPoint
`;

export function resolvers(redis: RedisClientType) {
  return {
    Query: {
      portAreas: async () => [],
      sensors: async (_: unknown, args: { type?: string }) => [],
      energyAssets: async () => [],
      bathyProfile: async (_: unknown, args: { id: string }) => [],
    },
    Subscription: {
      entityUpdated: {
        subscribe: async function* () {
          // placeholder async iterator
          while (true) {
            await new Promise((r) => setTimeout(r, 10000));
          }
        },
      },
    },
  };
}
