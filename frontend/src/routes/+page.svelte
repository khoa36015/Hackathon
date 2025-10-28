<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';
  export let data;
  import Footer from '$lib/components/Footer.svelte';
  import Hero from '$lib/components/Hero.svelte';
  
  import { getProvinceData } from '$lib';

  let allProvinces = null;
  let selectedProvince = null;
  let randomPlaces = [];
  let error = null;

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

</script>


<Header token={data.token} />
<main>
  <Hero on:search={(e) => selectProvince(e.detail.keyword)} />


  {#if error}
    <p class="text-red-500">{error}</p>
  {:else if !allProvinces}
    <p class="text-gray-500">Đang tải dữ liệu...</p>
  {:else if !selectedProvince}
    <!-- Hiển thị 6 địa điểm ngẫu nhiên -->
    <section class="p-6">
      <h2 class="text-2xl font-bold mb-4">📍 Gợi ý địa điểm nổi bật</h2>
      <ul class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {#each randomPlaces as place}
          <li class="border p-4 rounded-lg shadow">
            <h3 class="text-xl font-medium">{place.name}</h3>
            <p class="italic text-sm text-gray-600">Tỉnh: {place.province}</p>
            <p>{place.mo_ta}</p>
            <img src={place.anh} alt={place.name} class="mt-2 rounded" />
          </li>
        {/each}
      </ul>
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
            <li class="border p-4 rounded-lg shadow">
              <h3 class="text-xl font-medium">{name}</h3>
              <p>{info.mo_ta}</p>
              <img src={info.anh} alt={name} class="mt-2 rounded" />
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
            <li class="border p-4 rounded-lg shadow">
              <h3 class="text-xl font-medium">{dish}</h3>
              <p>{info.mo_ta}</p>
              <img src={info.anh} alt={dish} class="mt-2 rounded" />
            </li>
          {/each}
        </ul>
      </section>
    </div>
  {/if}
</main>
<Footer />
