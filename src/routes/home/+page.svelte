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
            var response = await fetch(
                `http://localhost:5000/api/user/${username}`
            );

            if (response.ok) {
                user = await response.json();
            } else {
                alert("HTTP-Error: " + response.status);
            }
        } else {
            // Redirect to the login page if the username is not present
            window.location.href = "/login";
        }
    });

    function to_market() {
        window.location.href = `/market?username=${encodeURIComponent(
            user.username
        )}`;
    }

    function to_inventory() {
        window.location.href = `/inventory?username=${encodeURIComponent(
            user.username
        )}`;
    }
</script>

<body class="container mx-auto h-screen flex flex-col items-center justify-between">
    <header class="flex items-center justify-between bg-blue-500 p-6 w-screen">
        <h1 class="text-white font-semibold text-2xl">
            CyberQuarium
        </h1>
        <div class="flex items-center text-white font-semibold">
            <p>You have {user.coins} coins</p>
        </div>
    </header>

    <div class="bg-white p-4 rounded text-9xl text-center w-screen">
        <p>Welcome Back! {user.username}</p>
    </div>

    <div class="mt-4 flex space-x-4 mb-4">
        <button
            class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
            on:click={to_market}
        >
            Market
        </button>
        <button
            class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
            on:click={to_inventory}
        >
            Inventory
        </button>
    </div>
</body>
