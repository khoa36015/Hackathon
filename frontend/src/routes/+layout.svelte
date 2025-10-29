<script lang="js">
  let { children } = $props();
  import '../app.css';
  import { onMount } from 'svelte';
  import { checkSession } from '$lib/api';
  import { session } from '$lib/stores/session';

  onMount(async () => {
    const data = await checkSession();
    session.set({
      isLoggedIn: data.isLoggedIn,
      username: data.username
    });
  });
</script>

<main>
{@render children()}
</main>