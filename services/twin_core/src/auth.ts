import { createRemoteJWKSet, jwtVerify } from 'jose';
import type {
  ApolloServerPlugin,
  BaseContext,
  GraphQLRequestContextDidResolveOperation,
} from '@apollo/server';

const issuer = process.env.KEYCLOAK_URL?.replace(/\/$/, '') + '/realms/' + (process.env.KEYCLOAK_REALM || 'smartport');
const JWKS = createRemoteJWKSet(new URL(`${issuer}/protocol/openid-connect/certs`));

export async function verify(token: string) {
  await jwtVerify(token, JWKS, { issuer });
}

export function authPlugin(): ApolloServerPlugin<BaseContext> {
  return {
    async requestDidStart() {
      return {
        async didResolveOperation(
          requestContext: GraphQLRequestContextDidResolveOperation<BaseContext>,
        ) {
          const auth = requestContext.request.http?.headers.get('authorization');
          if (!auth || !auth.startsWith('Bearer ')) {
            throw new Error('Unauthorized');
          }
          const token = auth.slice(7);
          await verify(token);
        },
      };
    },
  };
}
