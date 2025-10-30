<script>
    import { onMount } from 'svelte';
    import { getProvinces } from '$lib/api.js';
    let provinces = [];
    let randomProvinces = [];

    function getRandomPlaces(provinces, count = 6) {
        const allPlaces = [];

        for (const provinceKey in provinces) {
        const province = provinces[provinceKey];
        if (province?.dia_diem) {
            for (const [name, info] of Object.entries(province.dia_diem)) {
            allPlaces.push({ name, ...info, province: province.ten });
            }
        }
        }

        // Trộn ngẫu nhiên và lấy số lượng yêu cầu
        return allPlaces.sort(() => Math.random() - 0.5).slice(0, count);
    }

    onMount(async () => {
        try {
        provinces = await getProvinces();
        randomProvinces = getRandomPlaces(provinces);
        console.log('📍 Địa điểm ngẫu nhiên:', randomProvinces);
        } catch (err) {
        console.error('❌ Lỗi khi tải dữ liệu tỉnh:', err.message || err);
        }
    });
</script>



<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    
</div>