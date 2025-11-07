<script>
  import { onMount } from 'svelte';
  import { getProvinces } from '$lib/api';
  import { searchQuery } from '$lib/stores/search.js';

  let allProvinces = null;
  let randomProvinces = [];
  let selectedProvince = null;
  let showPopup = false;
  let error = null;

  // Lấy dữ liệu
  async function fetchProvinces() {
    try {
      const data = await getProvinces();
      allProvinces = data;
      saveProvinces(data);
      randomProvinces = getRandomProvinces(data);
    } catch (err) {
      error = err.message;
    }
  }

  function saveProvinces(data) {
    const now = Date.now();
    const item = {
      value: data,
      expiry: now + 3600 * 4000 // 4 giờ
    };
    localStorage.setItem('provinces', JSON.stringify(item));
  }

  function loadProvinces() {
    const itemStr = localStorage.getItem('provinces');
    if (!itemStr) return null;

    const item = JSON.parse(itemStr);
    const now = Date.now();

    if (now > item.expiry) {
      localStorage.removeItem('provinces');
      return null;
    }
    return item.value;
  }

  onMount(async () => {
    const saved = loadProvinces();
    if (saved) {
      allProvinces = saved;
      randomProvinces = getRandomProvinces(allProvinces);
    } else {
      await fetchProvinces();
    }
  });

  function getRandomProvinces(data, count = 6) {
    return data ? data.sort(() => 0.5 - Math.random()).slice(0, count) : [];
  }

  // Reactive: khi keyword thay đổi → tìm tỉnh và mở popup
  $: {
    if ($searchQuery && allProvinces?.length) {
      const lower = $searchQuery.toLowerCase();
      const found = allProvinces.find(
        (p) =>
          (p.id && p.id.toLowerCase().includes(lower)) ||
          (p.ten && p.ten.toLowerCase().includes(lower)) ||
          (p.mo_ta && p.mo_ta.toLowerCase().includes(lower))
      );
      if (found) {
        openPopup(found);
      } else {
        closePopup();
      }
    }
  }

  function openPopup(province) {
    selectedProvince = province;
    showPopup = true;
  }

  function closePopup() {
    showPopup = false;
    selectedProvince = null;
  }
</script>

<style>
  /* Fade In */
  .fade-in {
    animation: fadeIn 0.8s ease-in-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Slide Up */
  .slide-up {
    animation: slideUp 0.8s ease-out;
  }
  @keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  /* Bounce nhẹ khi hover */
  .bounce:hover {
    animation: bounce 0.6s ease;
  }
  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
  }

  /* Zoom khi hover ảnh */
  .zoom:hover {
    transform: scale(1.05);
    transition: transform 0.4s ease;
  }

  /* Popup animation */
  .popup-enter {
    animation: fadeIn 0.5s ease, zoomIn 0.5s ease;
  }
  @keyframes zoomIn {
    from { transform: scale(0.95); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
</style>

<main class="fade-in">
  {#if error}
    <p class="text-red-500">{error}</p>
  {:else if !allProvinces}
    <p class="text-gray-500 slide-up">Đang tải dữ liệu...</p>
  {:else}
    <section class="px-6 py-10 bg-linear-to-b from-sky-50 to-white fade-in">
      <h2 class="text-3xl font-bold text-center text-sky-800 mb-8 slide-up">
        Tỉnh thành nổi bật
      </h2>

      {#if randomProvinces && randomProvinces.length > 0}
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {#each randomProvinces as province, i}
            <div
              class="bg-white rounded-2xl shadow-lg overflow-hidden transition transform hover:scale-105 slide-up"
              style="animation-delay: {i * 0.1}s;"
            >
              <button on:click={() => openPopup(province)} class="cursor-pointer bounce">
                <img
                  src={province?.anh_dai_dien?.url || '/fallback.jpg'}
                  alt={province.ten}
                  class="h-48 w-full object-cover zoom"
                />
                <div class="p-5 space-y-3">
                  <h3 class="text-xl font-bold text-sky-700">{province.ten}</h3>
                  <p class="text-gray-700 text-sm leading-relaxed line-clamp-3">{province.mo_ta}</p>
                </div>
              </button>
            </div>
          {/each}
        </div>
      {:else}
        <p class="text-center text-gray-500 slide-up">Không có dữ liệu tỉnh thành.</p>
      {/if}
    </section>

    {#if showPopup && selectedProvince}
      <div
        class="fixed inset-0 backdrop-blur-md bg-white/50 bg-opacity-50 flex items-center justify-center z-50 transition-opacity duration-300 popup-enter"
      >
        <div
          class="relative bg-white rounded-2xl shadow-2xl max-w-4xl w-full p-8 overflow-y-auto max-h-[90vh] transform transition-all duration-300"
        >
          <button
            class="absolute top-4 right-4 text-gray-500 hover:text-red-500 transition cursor-pointer"
            on:click={() => { closePopup(); searchQuery.set(''); }}
          >
            ✖
          </button>

          <h1 class="text-4xl font-extrabold text-sky-700 mb-6 text-center fade-in">
            {selectedProvince.ten}
          </h1>
          <img
            src={selectedProvince?.anh_dai_dien?.url || '/fallback.jpg'}
            alt="Ảnh tỉnh"
            class="w-full rounded-xl mb-6 shadow-md zoom"
          />
          <p class="mb-8 text-lg text-gray-700 leading-relaxed fade-in">
            {selectedProvince.mo_ta}
          </p>

          <h2 class="text-2xl font-semibold mb-4 text-sky-600 slide-up">📍 Địa điểm nổi bật</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {#each Object.entries(selectedProvince.dia_diem || {}) as [name, info]}
              <div class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden zoom">
                <img src={info?.anh?.url || '/fallback.jpg'} alt={name} class="w-full h-48 object-cover" />
                <div class="p-4">
                  <h3 class="text-xl font-bold text-gray-800">{name}</h3>
                  <p class="text-gray-600 text-sm">{info.mo_ta}</p>
                </div>
              </div>
            {/each}
          </div>

          <h2 class="text-2xl font-semibold mb-4 text-sky-600 slide-up">🍜 Món ăn đặc sản</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {#each Object.entries(selectedProvince.mon_an || {}) as [dish, info]}
              <div class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden zoom">
                <img src={info?.anh?.url || '/fallback.jpg'} alt={dish} class="w-full h-48 object-cover" />
                <div class="p-4">
                  <h3 class="text-xl font-bold text-gray-800">{dish}</h3>
                  <p class="text-gray-600 text-sm">{info.mo_ta}</p>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    {/if}
  {/if}
</main>
