<script>
	import { URL } from './../../node_modules/uuid/dist/esm/v35.js';
  import '../app.css';
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';
  export let data;
  
  import { getProvinceData } from '$lib';

  let allProvinces = null;
  let selectedProvince = null;
  let randomPlaces = [];
  let error = null;

  let URL_tinh = '';

  // Hàm lấy ngẫu nhiên 6 địa điểm từ tất cả tỉnh
  function getRandomPlaces(data, count = 6) {
    const allPlaces = [];

    for (const provinceKey in data) {
      const province = data[provinceKey];
      for (const [name, info] of Object.entries(province.dia_diem)) {
        allPlaces.push({ name, ...info, province: province.ten });
      }
    }

    // Shuffle và lấy 6 phần tử
    return allPlaces.sort(() => 0.5 - Math.random()).slice(0, count);
  }

  onMount(async () => {
    try {
      allProvinces = await getProvinceData('/provinces.json');
      randomPlaces = getRandomPlaces(allProvinces);
    } catch (err) {
      error = err.message;
    }
  });

  // Hàm xử lý khi người dùng chọn tỉnh
  function selectProvince(keyword) {
    const foundKey = Object.keys(allProvinces).find(
      (key) => allProvinces[key].ten.toLowerCase().includes(keyword)
    );

    if (foundKey) {
      selectedProvince = allProvinces[foundKey];
    } else {
      selectedProvince = null;
      alert('Không tìm thấy tỉnh phù hợp!');
    }
  }

  async function getProvinces(URL_tinh) {
    const res = await fetch(URL_tinh);
    if (!res.ok) {
      throw new Error('Không thể tải dữ liệu tỉnh.');
    }
    return await res.json();
  }

</script>

<Header on:search={(e) => selectProvince(e.detail.keyword)} />
<main>
  {#if error}
    <p class="text-red-500">{error}</p>
  {:else if !allProvinces}
    <p class="text-gray-500">Đang tải dữ liệu...</p>
  {:else if !selectedProvince}
    <!-- Hiển thị 6 địa điểm ngẫu nhiên -->
    <section class="px-6 py-10 bg-linear-to-b from-sky-50 to-white">
      <h2 class="text-3xl font-bold text-center text-sky-800 mb-8">📍 Địa điểm nổi bật</h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each randomPlaces as place}
          <div class="bg-white rounded-2xl shadow-lg overflow-hidden transform transition duration-300 hover:scale-[1.02] hover:shadow-xl">
            <div class="h-48 w-full overflow-hidden">
              <img src={place.anh} alt={place.name} class="w-full h-full object-cover transition duration-300 group-hover:scale-105" />
            </div>
            <div class="p-5 space-y-3">
              <h3 class="text-xl font-bold text-sky-700">{place.name}</h3>
              <p class="text-sm text-gray-500 italic">Tỉnh: {place.province}</p>
              <p class="text-gray-700 text-sm leading-relaxed line-clamp-3">{place.mo_ta}</p>
            </div>
          </div>
        {/each}
      </div>

      <div class="mt-10 flex justify-center">
        <button
          on:click={() => randomPlaces = getRandomPlaces(allProvinces)}
          class="bg-sky-600 hover:bg-sky-700 text-white font-semibold px-6 py-3 rounded-full shadow-md transition-all duration-300">
          🔁 Gợi ý khác
        </button>
      </div>
    </section>
  {:else}
    <!-- Hiển thị chi tiết tỉnh đã chọn -->
    <div class="p-6 space-y-6">
      <h1 class="text-3xl font-bold">{selectedProvince.ten}</h1>
      <p>{selectedProvince.mo_ta}</p>
      <img src={selectedProvince.anh_dai_dien} alt="Ảnh Tỉnh" class="w-full rounded-lg" />

      <section>
        <h2 class="text-2xl font-semibold mt-6 mb-2">📍 Địa điểm nổi bật</h2>
        <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#each Object.entries(selectedProvince.dia_diem) as [name, info]}
            <li class="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group">
              <img src={info.anh} alt={name} class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300" />
              <div class="p-4 space-y-2">
                <h3 class="text-xl font-semibold text-gray-800">{name}</h3>
                <p class="text-gray-600 text-sm">{info.mo_ta}</p>
              </div>
            </li>
          {/each}
        </ul>
      </section>

      <section>
        <h2 class="text-2xl font-semibold mt-6 mb-2">🎭 Văn hoá</h2>
        <ul class="list-disc list-inside">
          {#each selectedProvince.van_hoa as culture}
            <li>{culture}</li>
          {/each}
        </ul>
      </section>

      <section>
        <h2 class="text-2xl font-semibold mt-6 mb-2">🍜 Món ăn đặc sản</h2>
        <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#each Object.entries(selectedProvince.mon_an) as [dish, info]}
            <li class="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden group">
              <img src={info.anh} alt={dish} class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300" />
              <div class="p-4 space-y-2">
                <h3 class="text-xl font-semibold text-gray-800">{dish}</h3>
                <p class="text-gray-600 text-sm">{info.mo_ta}</p>
              </div>
            </li>
          {/each}
        </ul>
      </section>
    </div>
  {/if}
</main>
<Footer />

<div class="6-tinh-mien-tay">
  <div class="1"></div>
  <div class="2"></div>
  <div class="3"></div>
  <div class="4"></div>
  <div class="5"></div>
  <div class="6"></div>
</div>