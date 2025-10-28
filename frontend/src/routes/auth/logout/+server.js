import { json } from '@sveltejs/kit';

export async function POST({ cookies }) {
  cookies.delete('token', {
    path: '/',
    httpOnly: true,
    sameSite: 'strict',
    secure: true
  });

  return new Response(null, { status: 204 });
}
