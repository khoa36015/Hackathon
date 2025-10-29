import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ fetch }) => {
  await fetch('http://localhost:3000/api/check-session', {
    method: 'GET',
    credentials: 'include'
  });
  return new Response(null, {
    status: 302,
    headers: { Location: '/' }
  });
};
