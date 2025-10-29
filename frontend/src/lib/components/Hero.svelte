<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  let searchText = '';

  function handleSearch() {
    if (searchText.trim()) {
      dispatch('search', { keyword: searchText.trim().toLowerCase() });
    }
  }
</script>

<div class="relative h-[600px] bg-[url(/images/bg.jpg)] bg-cover bg-bottom flex items-center justify-center">
  <!-- Lớp phủ nhẹ để tăng độ tương phản -->
  <div class="absolute inset-0 bg-black/20"></div>

  <!-- Nội dung chính -->
  <div class="relative z-10 flex flex-col gap-6 justify-center items-center w-full h-full px-4 md:px-0">
    
    <h1 class="text-5xl md:text-6xl lg:text-7xl font-extrabold text-white drop-shadow-md tracking-wide">
      MIỀN TÂY
    </h1>
    
    <p class="text-lg md:text-xl text-white/90 font-light tracking-wider">
      KHÁM PHÁ VẺ ĐẸP SÔNG NƯỚC
    </p>

    <div class="relative w-full max-w-xl">
      <input
        type="text"
        bind:value={searchText}
        placeholder="Tìm tỉnh..."
        class="w-full rounded-lg py-3 pl-5 pr-12 text-gray-900 bg-white/90 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-lg"
        on:keydown={(e) => e.key === 'Enter' && handleSearch()}
      />
      <button
        type="button"
        class="absolute top-1/2 right-4 -translate-y-1/2 text-gray-600 hover:text-blue-600 transition"
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

