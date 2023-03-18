<script>
    import { onMount } from "svelte";

    let username = "";
    let user = {};
    let eggs = [];
    let animals = [];

    onMount(async () => {
        // Get the URL search parameters
        const searchParams = new URLSearchParams(window.location.search);

        // Get the username from the search parameters
        if (searchParams.has("username")) {
            username = searchParams.get("username");
            // Search the user in the database
            const response = await fetch(
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

        // Get user's eggs
        const eggsResponse = await fetch(
            `http://localhost:5000/api/user/${username}/eggs`
        );
        eggs = await eggsResponse.json();

        // Get user's animals
        const animalsResponse = await fetch(
            `http://localhost:5000/api/user/${username}/animals`
        );
        animals = await animalsResponse.json();
    });

    async function hatchEgg(eggId) {
        const egg = eggs.find((e) => e.id === eggId);
        if (!egg) {
            alert("Error: Egg not found");
            return;
        }

        const response = await fetch("http://localhost:5000/hatch", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user: user,
                egg: egg,
            }),
        });

        if (response.ok) {
            const animal = await response.json();
            // Add code to update the inventory UI with the new animal
        } else {
            alert("HTTP-Error: " + response.status);
        }
    }

    function burnAnimal(animal) {
        // Add code to burn the animal
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
            <button class="hatch-btn" on:click={() => hatchEgg(egg.id)}>Hatch</button>
        </div>
    {/each}
</div>
<div class="animals-container container flex flex-wrap">
    {#each animals as animal}
        <div class="animal p-4 m-4">
            <img src={animal.image} alt="Animal" class="animal-image" />
            <div class="animal-info">
                <p>Rarity: {animal.rarity}</p>
                <p>Species: {animal.species}</p>
                <p>Name: {animal.name}</p>
                <p>Yield: {animal.coin_yield} coins/hour</p>
                <p>Yielded: {animal.coins_yielded}</p>
            </div>
            <button class="burn-animal-btn" on:click={() => burnAnimal(animal)}>Burn</button>
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

    .hatch-btn, .burn-animal-btn {
        background-color: #4caf50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: 0.3s;
    }

    .hatch-btn:hover, .burn-animal-btn:hover {
        background-color: #45a049;
    }
</style>
