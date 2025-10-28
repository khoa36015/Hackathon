<script>
  import { invalidate } from '$app/navigation';
  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleLogin() {
    loading = true;
    error = '';
    const res = await fetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      headers: { 'Content-Type': 'application/json' }
    });

    let result;
    try {
      result = await res.json();
    } catch (err) {
      error = 'Máy chủ trả về phản hồi không hợp lệ (không phải JSON)';
      loading = false;
      return;
    }

    if (!res.ok) {
      error = result.message || 'Đăng nhập thất bại';
    } else {
      invalidate(); // reload dữ liệu nếu cần
    }
  }
</script>

<form on:submit|preventDefault={handleLogin} class="space-y-4">
  <h2 class="text-xl font-bold">Đăng nhập</h2>
  {#if error}<p class="text-red-500">{error}</p>{/if}
  <input type="email" bind:value={email} placeholder="Email" class="w-full p-2 border rounded" required />
  <input type="password" bind:value={password} placeholder="Mật khẩu" class="w-full p-2 border rounded" required />
  <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded w-full" disabled={loading}>
    {loading ? 'Đang xử lý...' : 'Đăng nhập'}
  </button>
</form>
