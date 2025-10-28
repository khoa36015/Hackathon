import { redirect } from '@sveltejs/kit';
import { dev } from '$app/environment';

export async function handle({ event, resolve }) {
	const token = event.cookies.get('token');
	event.locals.token = token;

	// Kiểm tra xem người dùng đã đăng nhập chưa
	if (!token && event.url.pathname !== '/') {
		return redirect(302, '/');
	}

	return resolve(event);
}

export async function handleDevTools({ event, resolve }) {
	// Block Chrome DevTools requests in development mode
	if (dev && event.url.pathname === '/.well-known/appspecific/com.chrome.devtools.json') {
		return new Response(undefined, { status: 404 });
	}

	return resolve(event);
}
