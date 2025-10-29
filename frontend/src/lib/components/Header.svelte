<script>
  import Modal from '$lib/components/Modal.svelte';
  import AuthForm from '$lib/components/Auth.svelte';
  import { session } from '$lib/stores/session';
  import { logout } from '$lib/api';
  
  let showAuthForm = false;
  let showMenu = false;

  async function handleLogout() {
    await logout();
    session.set({ isLoggedIn: false, username: null });
    location.reload();
  }
</script>

<nav class="bg-sky-100 border-b border-gray-200 shadow-sm transition-all duration-300 ease-in-out">
  <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
    
    <!-- Logo -->
    <a href="/" class="flex items-center gap-3 transition-all duration-300 ease-in-out">
      <img src="/images/logo.png" class="h-10 w-auto" alt="Logo" />
      <span class="text-2xl font-bold text-sky-800 tracking-wide">MIỀN TÂY TRAVEL</span>
    </a>

    <!-- Toggle button -->
    <button
      on:click={() => showMenu = !showMenu}
      class="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-sky-300 transition-all duration-300 ease-in-out"
      aria-controls="navbar-default"
      aria-expanded={showMenu}
    >
      <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
  </div>

  <!-- Menu -->
  <div class={`transition-all duration-500 ease-in-out ${showMenu ? 'block' : 'hidden'} md:block bg-white border-t md:border-none shadow-md md:shadow-none`} id="navbar-default">
    <ul class="flex flex-col md:flex-row gap-3 md:gap-6 px-4 py-4 md:py-0 text-gray-800 font-medium">
      <li><a href="/" class="block hover:text-sky-600 transition duration-300">TRANG CHỦ</a></li>
      {#if $session.isLoggedIn}
        <li><span class="text-sm">Xin chào, <strong>{$session.username}</strong></span></li>
        <li><a on:click={handleLogout} href="/" class="block hover:text-red-500 transition duration-300">ĐĂNG XUẤT</a></li>
      {:else}
        <li><a href="#" on:click={() => showAuthForm = true} class="block hover:text-sky-600 transition duration-300">ĐĂNG KÝ</a></li>
      {/if}
    </ul>
  </div>
</nav>


<!-- Modal đăng ký -->
<Modal show={showAuthForm} onClose={() => showAuthForm = false}>
  <AuthForm />
</Modal>