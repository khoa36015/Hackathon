<script>
  export let form;
</script>

<div class="mx-auto max-w-md bg-white border rounded-xl p-6 shadow-sm">
  <h1 class="text-2xl font-semibold mb-4">Tạo tài khoản</h1>

  {#if form?.message}
    <div class="mb-3 text-sm text-red-600">{form.message}</div>
  {/if}

  <form method="POST" class="space-y-3">
    <div>
      <label class="block text-sm mb-1">Họ tên</label>
      <input name="name" required class="w-full border rounded-lg px-3 py-2"
        value={form?.fields?.name ?? ''} />
    </div>
    <div>
      <label class="block text-sm mb-1">Email</label>
      <input name="email" type="email" required class="w-full border rounded-lg px-3 py-2"
        value={form?.fields?.email ?? ''} />
    </div>
    <div>
      <label class="block text-sm mb-1">Mật khẩu</label>
      <input name="password" type="password" minlength="6" required class="w-full border rounded-lg px-3 py-2" />
    </div>
    <button class="w-full bg-black text-white rounded-lg py-2 hover:opacity-90">Đăng ký</button>
  </form>

  <p class="text-sm text-gray-600 mt-4">
    Đã có tài khoản?
    <a href="/auth/login" class="underline">Đăng nhập</a>
  </p>
</div>
