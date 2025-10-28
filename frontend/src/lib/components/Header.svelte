<script>
  import Modal from '$lib/components/Modal.svelte';
  import LoginForm from '$lib/components/LoginForm.svelte';
  import RegisterForm from '$lib/components/RegisterForm.svelte';

  let showLogin = false;
  let showRegister = false;

  export let token;
  let isLoggedIn = !!token;
  const logout = async () => {
    await fetch('/auth/logout', { method: 'POST' });
    location.reload(); // hoặc chuyển hướng về trang chủ
  }
</script>

<nav class="bg-gray-300 border-gray-200">
  <div class="max-w-7xl flex flex-wrap items-center justify-between mx-auto p-4">
    <a href="/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <img src="/" class="h-8" alt="Logo" />
        <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">MIỀN TÂY TRAVEL</span>
    </a>
    <button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false">
        <span class="sr-only">Menu</span>
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
        </svg>
    </button>
    <div class="hidden w-full md:block md:w-auto" id="navbar-default">
      <ul class="font-medium flex flex-col p-4 md:p-0 mt-4 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0">
        <li>
          <a href="/" class="block py-2 px-3 text-white bg-blue-700 md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500" aria-current="page">TRANG CHỦ</a>
        </li>
        {#if !isLoggedIn}
          <li>
            <a href="#" on:click={() => showLogin = true} class="block py-2 px-3 text-gray-900 hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-black md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">ĐĂNG NHẬP</a>
          </li>
          <li>
            <a href="#" on:click={() => showRegister = true} class="block py-2 px-3 text-gray-900 hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-black md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">ĐĂNG KÝ</a>
          </li>
        {:else}
            <a href="#" on:click={logout} class="block py-2 px-3 text-gray-900 hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-black md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">ĐĂNG XUẤT</a>
        {/if}
        
      </ul>
    </div>
  </div>
</nav>

<!-- Modal đăng nhập -->
<Modal show={showLogin} onClose={() => showLogin = false}>
  <LoginForm />
</Modal>

<!-- Modal đăng ký -->
<Modal show={showRegister} onClose={() => showRegister = false}>
  <RegisterForm />
</Modal>