<script>
	import SearchBar from '$lib/components/SearchBar.svelte';
	import Landmarks from '$lib/components/Landmarks.svelte';

	let selectedProvince = '';

	function handleProvinceSelected(event) {
		selectedProvince = event.detail.province ?? '';
	}
</script>

<main class="mx-auto flex max-w-6xl flex-col gap-10 px-4 py-12">
	<section class="space-y-3 text-center">
		<h1 class="text-4xl font-bold text-slate-900 sm:text-5xl">
			- MIỀN TÂY -
		</h1>
		<p class="mx-auto max-w-2xl text-base text-slate-600 sm:text-lg">
			KHÁM PHÁ VẺ ĐẸP SÔNG NƯỚC
		</p>
	</section>

	<SearchBar bind:selectedProvince on:provinceSelected={handleProvinceSelected} />

	<Landmarks {selectedProvince} on:reset={() => (selectedProvince = '')} />
</main>
