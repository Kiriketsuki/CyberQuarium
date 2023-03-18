<!-- Home.svelte -->
<script>
    import { onMount } from "svelte";

    let username = "";
    var user = {};

    onMount(async () => {
        // Get the URL search parameters
        const searchParams = new URLSearchParams(window.location.search);

        // Get the username from the search parameters
        if (searchParams.has("username")) {
            username = searchParams.get("username");
            // search the user in the database
            var response = await fetch(`http://localhost:5000/api/user/${username}`);

            if (response.ok) {
                user = await response.json()
            } else {
                alert("HTTP-Error: " + response.status);
            }
        } else {
            // Redirect to the login page if the username is not present
            window.location.href = "/login";
        }
    });

    function to_market() {
        window.location.href = `/market/${username}`;
    }
</script>

<div class="container">
    <h1>Welcome, {user.username}!</h1>
    <p>You have {user.coins} coins.</p>
    <p>This is your home page.</p>
    <div onclick="to_market">
        market
    </div>
</div>
