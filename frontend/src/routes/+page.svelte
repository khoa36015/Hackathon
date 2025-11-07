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
      // Hết hạn → xóa và trả null
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
    return data.sort(() => 0.5 - Math.random()).slice(0, count);
  }

  // Reactive: khi keyword thay đổi → tìm tỉnh và mở popup
  $: {
    if ($searchQuery && allProvinces.length) {
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

<main>
  {#if error}
    <p class="text-red-500">{error}</p>
  {:else if !allProvinces}
    <p class="text-gray-500">Đang tải dữ liệu...</p>
  {:else}
    <!-- Hiển thị 6 tỉnh ngẫu nhiên -->
    <section class="px-6 py-10 bg-linear-to-b from-sky-50 to-white">
      <h2 class="text-3xl font-bold text-center text-sky-800 mb-8">Tỉnh thành nổi bật</h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each randomProvinces as province}
          <div
            class="bg-white rounded-2xl shadow-lg overflow-hidden hover:scale-[1.02] transition"
          >
            <button on:click={() => openPopup(province)} class="cursor-pointer">
              <img src={province.anh_dai_dien.url} alt={province.id} class="h-48 w-full object-cover" />
              <div class="p-5 space-y-3">
                <h3 class="text-xl font-bold text-sky-700">{province.ten}</h3>
                <p class="text-gray-700 text-sm leading-relaxed line-clamp-3">{province.mo_ta}</p>
              </div>
            </button>
          </div>
        {/each}
      </div>
    </section>

    <!-- Popup chi tiết -->
    {#if showPopup && selectedProvince}
      <div class="fixed inset-0 backdrop-blur-md bg-white/50 bg-opacity-50 flex items-center justify-center z-50 transition-opacity duration-300">
        <div class="relative bg-white rounded-2xl shadow-2xl max-w-4xl w-full p-8 overflow-y-auto max-h-[90vh] transform transition-all duration-300 scale-100">
          <!-- Nút đóng -->
          <button
            class="absolute top-4 right-4 text-gray-500 hover:text-red-500 transition cursor-pointer"
            on:click={() => { closePopup(); searchQuery.set(''); }}
          >
            ✖
          </button>

          <!-- Header -->
          <h1 class="text-4xl font-extrabold text-sky-700 mb-6 text-center">{selectedProvince.ten}</h1>
          <img src={selectedProvince.anh_dai_dien.url} alt="Ảnh tỉnh" class="w-full rounded-xl mb-6 shadow-md" />
          <p class="mb-8 text-lg text-gray-700 leading-relaxed">{selectedProvince.mo_ta}</p>

          <!-- Địa điểm nổi bật -->
          <h2 class="text-2xl font-semibold mb-4 text-sky-600">📍 Địa điểm nổi bật</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {#each Object.entries(selectedProvince.dia_diem) as [name, info]}
              <div class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden">
                <img src={info.anh.url} alt={name} class="w-full h-48 object-cover" />
                <div class="p-4">
                  <h3 class="text-xl font-bold text-gray-800">{name}</h3>
                  <p class="text-gray-600 text-sm">{info.mo_ta}</p>
                </div>
              </div>
            {/each}
          </div>

          <!-- Món ăn đặc sản -->
          <h2 class="text-2xl font-semibold mb-4 text-sky-600">🍜 Món ăn đặc sản</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {#each Object.entries(selectedProvince.mon_an) as [dish, info]}
              <div class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden">
                <img src={info.anh.url} alt={dish} class="w-full h-48 object-cover" />
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
