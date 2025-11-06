<script>
    import '../app.css';
    import Header from '$lib/components/Header.svelte';
    import Footer from '$lib/components/Footer.svelte';

    let keyword = '';

    function handleSearch(event) {
        keyword = event.detail.keyword;
    }

</script>

<Header on:search={handleSearch} />
<slot {keyword}/>
<Footer />
