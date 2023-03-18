<!-- Home.svelte -->
<script>
    import { onMount } from "svelte";
    var user = {};

    onMount(async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const username = urlParams.get("username");
        const response = await fetch(`http://localhost:5000/api/user/${username}`);

        if (response.ok) {
            user = await response.json();
        } else {
            console.error("Error retrieving user details.");
        }
    });
</script>

<div class="container">
    <h1>Welcome, {user.username}!</h1>
    <p>You have {user.coins} coins.</p>
    <p>This is your home page.</p>
</div>
