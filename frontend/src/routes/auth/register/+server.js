import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  const { email, password } = await request.json();

  // Giả lập lưu tài khoản
  if (!email || !password) {
    return json({ message: 'Thiếu thông tin' }, { status: 400 });
  }

  return json({ message: 'Đăng ký thành công' });
}
