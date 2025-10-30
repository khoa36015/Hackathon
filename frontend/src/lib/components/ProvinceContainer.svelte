<script>
    import { onMount } from 'svelte';
    import { getProvinces } from '$lib/api.js';
    //import ProvinceCard from '$lib/components/ProvinceCard.svelte';
    
    let provinces = [];
    
    onMount(async () => {
        provinces = await getProvinces();
    });
    console.log(provinces);
</script>

