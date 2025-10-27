<script>
  export let form;
</script>

<div class="mx-auto max-w-md bg-white border rounded-xl p-6 shadow-sm">
  <h1 class="text-2xl font-semibold mb-4">Đăng nhập</h1>

  {#if form?.message}
    <div class="mb-3 text-sm text-red-600">{form.message}</div>
  {/if}

  <form method="POST" class="space-y-3">
    <div>
      <label class="block text-sm mb-1">Email</label>
      <input name="email" type="email" required class="w-full border rounded-lg px-3 py-2"
        value={form?.fields?.email ?? ''} />
    </div>
    <div>
      <label class="block text-sm mb-1">Mật khẩu</label>
      <input name="password" type="password" required class="w-full border rounded-lg px-3 py-2" />
    </div>
    <button class="w-full bg-black text-white rounded-lg py-2 hover:opacity-90">Đăng nhập</button>
  </form>

  <p class="text-sm text-gray-600 mt-4">
    Chưa có tài khoản?
    <a href="/auth/register" class="underline">Đăng ký</a>
  </p>
</div>
