<script>
	import { westernProvinces } from '$lib/data/provinces.js';
	import { createEventDispatcher } from 'svelte';

	export let selectedProvince = '';

	const dispatch = createEventDispatcher();

	function handleSearch(event) {
		event?.preventDefault?.();
		dispatch('provinceSelected', { province: selectedProvince });
	}
</script>

<form
	class="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-100 transition hover:shadow-md"
	on:submit|preventDefault={handleSearch}
>
	<div class="flex flex-col gap-4 sm:flex-row sm:items-end">
		<label class="flex-1">
			<span class="mb-2 block text-sm font-medium text-slate-700">
				Chọn tỉnh bạn muốn khám phá
			</span>
			<select
				bind:value={selectedProvince}
				class="w-full rounded-xl border border-slate-200 px-4 py-3 text-base text-slate-800 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
			>
				<option value="">Chọn tỉnh miền Tây...</option>
				{#each westernProvinces as province}
					<option value={province.name}>{province.name}</option>
				{/each}
			</select>
		</label>

		<div class="flex flex-col gap-3 sm:flex-row sm:items-center">
			<button
				type="submit"
				class="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-300 focus-visible:ring-offset-2"
			>
				<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M21 21l-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z"
					/>
				</svg>
				<span>Hiển thị địa danh</span>
			</button>

			{#if selectedProvince}
				<button
					type="button"
					class="text-sm font-medium text-blue-600 transition hover:text-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-300 focus-visible:ring-offset-2"
					on:click={() => {
						selectedProvince = '';
						handleSearch();
					}}
				>
					Xóa lựa chọn
				</button>
			{/if}
		</div>
	</div>
</form>
