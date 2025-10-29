<script>
  import { register } from '$lib/api';
  import { login } from '$lib/api';
  import { goto } from '$app/navigation';

  let showLogin = false;

  let error = '';
  let success = '';
  let loading = false;

  let username = '';
  let password = '';
  let message = '';

  async function handleRegister() {
    const res = await register(username, password);
    message = res.message;
    loading = false;
    if (res.message === 'Registered successfully!') {
        success = "Đăng ký thành công";
        showLogin = true;
    }
    else {
        error = "Đăng ký thất bại";
    }
  }

  async function handleLogin() {
    const res = await login(username, password);
    message = res.message;
    if (res.isLoggedIn) {
      location.reload();
    }
    else {
      error = "Sai tài khoản hoặc mật khẩu";
    }
  }
</script>

{#if !showLogin}
  <form  on:submit|preventDefault={handleRegister} class="space-y-4">
    <h2 class="text-xl font-bold">Đăng ký</h2>
    {#if error}<p class="text-red-500">{error}</p>{/if}
    {#if success}<p class="text-green-600">{success}</p>{/if}
    <input type="text" bind:value={username} placeholder="Tên đăng nhập" class="w-full p-2 border rounded" required />
    <input type="password" bind:value={password} placeholder="Mật khẩu" class="w-full p-2 border rounded" required />
    <button type="submit" class="bg-violet-600 text-white px-4 py-2 rounded w-full cursor-pointer" disabled={loading}>
      {loading ? 'Đang xử lý...' : 'Đăng ký'}
    </button>
  </form>
  <button on:click={() => (showLogin = true)} class="bg-indigo-600 text-white my-2 px-4 py-2 rounded cursor-pointer">Đăng nhập</button>
{:else}
  <form on:submit|preventDefault={handleLogin} class="space-y-4">
    <h2 class="text-xl font-bold">Đăng nhập</h2>
    {#if error}<p class="text-red-500">{error}</p>{/if}
    <input type="text" bind:value={username} placeholder="Tên đăng nhập" class="w-full p-2 border rounded" required />
    <input type="password" bind:value={password} placeholder="Mật khẩu" class="w-full p-2 border rounded" required />
    <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded w-full cursor-pointer" disabled={loading}>
      {loading ? 'Đang xử lý...' : 'Đăng nhập'}
    </button>
  </form>
  <button on:click={() => (showLogin = false)} class="bg-violet-600 text-white my-2 px-4 py-2 rounded cursor-pointer">Đăng ký</button>
{/if}