<script>
  import Modal from '$lib/components/Modal.svelte';
  import AuthForm from '$lib/components/Auth.svelte';
  import { session } from '$lib/stores/session';
  import { logout } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  let searchText = '';
  let showAuthForm = false;
  let showMenu = false;

  function handleSearch() {
    if (searchText.trim()) {
      dispatch('search', { keyword: searchText.trim().toLowerCase() });
    }
  }

  async function handleLogout() {
    await logout();
    session.set({ isLoggedIn: false, username: null });
    location.reload();
  }
</script>

<div class="relative h-[600px] bg-[url(/images/bg_official.png)] bg-cover bg-center bg-no-repeat flex items-center justify-center">
  <!-- Lớp phủ nhẹ để tăng độ tương phản -->
  <div class="absolute inset-0 bg-black/20">
    <nav class="backdrop-blur-md bg-white/40 border-gray-200 shadow-sm transition-all duration-300 ease-in-out fixed top-0 left-0 w-full z-20">
      <div class="max-w-7xl mx-auto px-4 py-6 flex items-center justify-between">
        
        <!-- Logo -->
        <a href="/" class="flex items-center gap-3 transition-all duration-300 ease-in-out">
          <img src="/images/logo.png" class="h-10 w-auto" alt="Logo" />
          <span class="text-2xl font-bold text-sky-800 tracking-wide">MIỀN TÂY TRAVEL</span>
        </a>

        <!-- Toggle button -->
        <button
          on:click={() => showMenu = !showMenu}
          class="p-2 rounded-lg text-gray-600 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-sky-300 transition-all duration-300 ease-in-out"
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
      <div class={`transition-all duration-500 ease-in-out ${showMenu ? 'relative' : 'hidden'} `} id="navbar-default">
        <ul class="flex flex-row md:flex-col gap-3 md:gap-6 px-4 py-4 md:py-0 z-10 text-gray-800 font-medium ">
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

  <!-- Nội dung chính -->
  <div class="relative z-10 flex flex-col gap-6 justify-center items-center w-full h-full px-4 md:px-0">
    
    <h1 class="text-5xl md:text-6xl lg:text-7xl font-display text-white drop-shadow-md tracking-wide">
      Miền Tây
    </h1>
    
    <p class="text-lg md:text-xl text-white/90 font-light tracking-wider">
      KHÁM PHÁ VẺ ĐẸP SÔNG NƯỚC
    </p>

    <div class="relative w-full max-w-xl opacity-50">
      <input
        type="text"
        bind:value={searchText}
        placeholder="Tìm tỉnh..."
        class="w-full rounded-4xl py-3 pl-5 pr-12 text-neutral-950 font-normal hover:font-black bg-white/90 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-lg"
        on:keydown={(e) => e.key === 'Enter' && handleSearch()}
      />
      <button
        type="button"
        class="absolute top-1/2 right-4 -translate-y-1/2 text-neutral-950 hover:text-blue-600 transition"
        on:click={handleSearch}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M21 21l-5.2-5.2m0 0A7.5 7.5 0 105.2 5.2a7.5 7.5 0 0010.6 10.6z" />
        </svg>
      </button>
    </div>
  </div>
  </div>
</div>

