<script>
	import { westernProvinces } from '$lib/data/provinces.js';
	import { createEventDispatcher, onMount } from 'svelte';

	export let selectedProvince = '';

	const dispatch = createEventDispatcher();

	const allLandmarks = westernProvinces.flatMap((province) =>
		province.landmarks.map((landmark) => ({
			...landmark,
			province: province.name
		}))
	);

	let currentLandmarks = [];
	let provinceLabel = '';

	function showRandomLandmarks(notifyParent = false) {
		const shuffled = [...allLandmarks].sort(() => Math.random() - 0.5);
		currentLandmarks = shuffled.slice(0, 6);
		provinceLabel = '';
		if (notifyParent) {
			dispatch('reset');
		}
	}

	function loadProvinceLandmarks(provinceName) {
		if (!provinceName) {
			showRandomLandmarks();
			return;
		}

		const province = westernProvinces.find((item) => item.name === provinceName);
		if (province) {
			currentLandmarks = province.landmarks.map((landmark) => ({
				...landmark,
				province: province.name
			}));
			provinceLabel = province.name;
		} else {
			showRandomLandmarks();
		}
	}

	onMount(() => {
		loadProvinceLandmarks(selectedProvince);
	});

	$: loadProvinceLandmarks(selectedProvince);
</script>

<section class="space-y-8">
	<header class="space-y-2 text-center">
		<h2 class="text-2xl font-semibold text-slate-900 sm:text-3xl">
			{#if provinceLabel}
				Địa danh nổi bật của {provinceLabel}
			{:else}
				Gợi ý địa danh khắp miền Tây
			{/if}
		</h2>
		<p class="mx-auto max-w-2xl text-sm text-slate-600 sm:text-base">
			{#if provinceLabel}
				Cùng khám phá bốn điểm đến được du khách yêu thích nhất tại tỉnh {provinceLabel}.
			{:else}
				Xin được gợi ý ngẫu nhiên sáu địa danh đặc sắc từ các tỉnh miền Tây khác nhau.
			{/if}
		</p>
	</header>

	{#if currentLandmarks.length === 0}
		<p class="text-center text-slate-600">Chưa có gợi ý nào, hãy thử chọn một tỉnh khác.</p>
	{:else}
		<div class="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
			{#each currentLandmarks as landmark (landmark.name)}
				<article class="flex h-full flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-slate-100 transition hover:-translate-y-1 hover:shadow-lg">
					<img
						src={landmark.image}
						alt={`Ảnh ${landmark.name}`}
						class="h-40 w-full object-cover"
						loading="lazy"
					/>
					<div class="flex flex-1 flex-col gap-3 p-5">
						<div>
							<p class="text-xs font-semibold uppercase tracking-wide text-blue-600">{landmark.province}</p>
							<h3 class="mt-1 text-lg font-semibold text-slate-900">{landmark.name}</h3>
						</div>
						<p class="text-sm text-slate-600">{landmark.description}</p>
					</div>
				</article>
			{/each}
		</div>

		{#if !provinceLabel}
			<div class="text-center">
				<button
					type="button"
					class="inline-flex items-center gap-2 rounded-xl bg-slate-100 px-5 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-300 focus-visible:ring-offset-2"
					on:click={() => showRandomLandmarks(true)}
				>
					<svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 4v5h.582m0 0A7.5 7.5 0 1 1 6 13.5L4.582 9M20 20v-5h-.581m0 0A7.5 7.5 0 0 1 18 10.5L19.419 15"
						/>
					</svg>
					Xem gợi ý khác
				</button>
			</div>
		{/if}
	{/if}
</section>
