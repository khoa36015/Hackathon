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

<div class="relative h-[400px] bg-gradient-to-tr from-indigo-600 via-indigo-700 to-violet-800">
  <div class="flex flex-col gap-4 justify-center items-center w-full h-full px-3 md:px-0">
    <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white">MIỀN TÂY</h1>
    <p class="text-gray-300">KHÁM PHÁ VẺ ĐẸP SÔNG NƯỚC</p>

    <div class="relative p-3 border border-gray-200 rounded-lg w-full max-w-lg">
      <input
        type="text"
        bind:value={searchText}
        class="rounded-md w-full p-3"
        placeholder="Tìm tỉnh"
        on:keydown={(e) => e.key === 'Enter' && handleSearch()}
      />

      <button type="button" class="absolute right-6 top-6" on:click={handleSearch}>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
          stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
        </svg>
      </button>
    </div>
  </div>
</div>
