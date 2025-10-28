// src/routes/auth/login/+server.js
import { json } from '@sveltejs/kit';

export async function POST({ request, cookies }) {
  const { email, password } = await request.json();

  // Giả lập xác thực
  if (email === 'test@example.com' && password === '123456') {
    cookies.set('token', 'fake-token', {
      path: '/',
      httpOnly: true,
      sameSite: 'strict',
      secure: false, // dùng false nếu đang chạy localhost
      maxAge: 60 * 60 * 24 * 7
    });

    return json({ message: 'Đăng nhập thành công!' });
  }

  return json({ message: 'Sai thông tin đăng nhập' }, { status: 401 });
}
