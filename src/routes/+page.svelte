<!-- landing.svelte -->
<script>
    import Home from "../routes/home/+page.svelte";
    import Login from "../routes/login/+page.svelte";
    import Register from "../routes/register/+page.svelte";
    import Landing from "../routes/landing/+page.svelte";
    import { user, currentPage } from "../store.js";

    function navigateTo(page) {
        $currentPage = page;
    }
</script>

<!-- landing.svelte -->
{#if $currentPage === 'home'}
  <Home />
{:else if $currentPage === 'login'}
  <Login />
{:else if $currentPage === 'register'}
  <Register />
{:else if $currentPage === 'landing'}
    <Landing />
{/if}
