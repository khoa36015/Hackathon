<script>
  let email = '';
  let password = '';
  let error = '';
  let success = '';
  let loading = false;

  async function handleRegister() {
    loading = true;
    error = '';
    success = '';
    const res = await fetch('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      headers: { 'Content-Type': 'application/json' }
    });

    const result = await res.json();
    loading = false;

    if (!res.ok) {
      error = result.message || 'Đăng ký thất bại';
    } else {
      success = 'Đăng ký thành công! Bạn có thể đăng nhập.';
    }
  }
</script>

<form on:submit|preventDefault={handleRegister} class="space-y-4">
  <h2 class="text-xl font-bold">Đăng ký</h2>
  {#if error}<p class="text-red-500">{error}</p>{/if}
  {#if success}<p class="text-green-600">{success}</p>{/if}
  <input type="email" bind:value={email} placeholder="Email" class="w-full p-2 border rounded" required />
  <input type="password" bind:value={password} placeholder="Mật khẩu" class="w-full p-2 border rounded" required />
  <button type="submit" class="bg-violet-600 text-white px-4 py-2 rounded w-full" disabled={loading}>
    {loading ? 'Đang xử lý...' : 'Đăng ký'}
  </button>
</form>
