<script>
  export let show = false;
  export let onClose = () => {};
</script>

{#if show}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md relative">
      <button class="absolute top-2 right-2 text-gray-500 cursor-pointer" on:click={onClose}>✕</button>
      <slot />
    </div>
  </div>
{/if}
