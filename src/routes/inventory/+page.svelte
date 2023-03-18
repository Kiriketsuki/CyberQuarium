<script>
    import { onMount } from "svelte";

    let username = "";
    let user = {};
    let eggs = [];

    onMount(async () => {
        // Get the URL search parameters
        const searchParams = new URLSearchParams(window.location.search);

        // Get the username from the search parameters
        if (searchParams.has("username")) {
            username = searchParams.get("username");
            const response = await fetch(
                `http://localhost:5000/api/user/${username}/eggs`
            );

            if (response.ok) {
                eggs = await response.json();
            } else {
                alert("HTTP-Error: " + response.status);
            }
        } else {
            // Redirect to the login page if the username is not present
            window.location.href = "/login";
        }
    });

    function hatchEgg(eggId) {
        alert("Hatching egg with ID " + eggId);
        // Add hatching logic here
    }
</script>

<div class="container flex flex-wrap">
    {#each eggs as egg (egg.id)}
        <div class="egg-card p-4 m-4">
            <img src="/path/to/egg-image.png" alt="Egg" class="egg-image" />
            <div class="egg-info">
                <p>Rarity: {egg.rarity}</p>
                <p>Price: {egg.cost} coins</p>
            </div>
            <button class="hatch-btn" on:click={() => hatchEgg(egg.id)}
                >Hatch</button
            >
        </div>
    {/each}
</div>

<style>
    .container {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    .egg-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .egg-image {
        width: 200px;
        height: auto;
    }

    .hatch-btn {
        background-color: #4caf50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: 0.3s;
    }

    .hatch-btn:hover {
        background-color: #45a049;
    }
</style>
