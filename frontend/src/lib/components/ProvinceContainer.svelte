<script>
    import { onMount } from 'svelte';
    import { getProvinces } from '$lib/api.js';
    let provinces = [];
    let randomProvinces = [];

    function getRandomPlaces(provinces, count = 6) {

        for (const provinceKey in provinces) {
        const province = provinces[provinceKey];
        if (province?.dia_diem) {
            for (const [name, info] of Object.entries(province.dia_diem)) {
            provinces.push({ name, ...info, province: province.ten });
            }
        }
        }

        // Trộn ngẫu nhiên và lấy số lượng yêu cầu
        return provinces.sort(() => Math.random() - 0.5).slice(0, count);
    }

    onMount(async () => {
        try {
        provinces = await getProvinces();
        console.log('✅ Dữ liệu tỉnh đã tải:', provinces);
        randomProvinces = getRandomPlaces(provinces);
        console.log('📍 Địa điểm ngẫu nhiên:', randomProvinces);
        } catch (err) {
        console.error('❌ Lỗi khi tải dữ liệu tỉnh:', err.message || err);
        }
    });
</script>


<section class="px-6 py-10 bg-linear-to-b from-sky-50 to-white">
    <h2 class="text-3xl font-bold text-center text-sky-800 mb-8">Địa điểm nổi bật</h2>

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