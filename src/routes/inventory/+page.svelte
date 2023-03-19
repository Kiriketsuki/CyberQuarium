<script>
    import { onMount, onDestroy } from "svelte";
    import MessagePopup from "../../components/MessagePopup.svelte";

    let username = "";
    let user = {};
    let eggs = [];
    let animals = [];
    let updateCoinsInterval;
    let message = "";
    let status = "error";
    let showPopup = false;

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

        async () => {
            updateCoinsInterval = setInterval(async () => {
                const response = await fetch(
                    `http://localhost:5000/api/update-coins`
                );
                if (!response.ok) {
                    console.error("Error updating coins: " + response.status);
                }
            }, 5 * 60 * 1000);
            window.location.reload();
        };
    });

    onDestroy(() => {
        clearInterval(updateCoinsInterval);
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
            // refresh the page
            window.location.reload();
        } else {
            alert("HTTP-Error: " + response.status);
        }
    }

    async function burnAnimal(animalId) {
        const response = await fetch("http://localhost:5000/api/burn_animal", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                animal_id: animalId,
                user_id: user.id,
            }),
        });

        const result = await response.json();

        if (response.ok) {
            // Refresh the animal list
            message = result.message;
            status = "success";
            showPopup = true;
        } else {
            console.error(result.message);
        }
    }

    function to_home() {
        window.location.href = `/home?username=${encodeURIComponent(
            user.username
        )}`;
    }

    function to_market() {
        window.location.href = `/market?username=${encodeURIComponent(
            user.username
        )}`;
    }

    // breeding functions

    let selectedAnimals = [];
    let showBreedButton = false;
    let animalRefs = {};

    function selectAnimal(animalId) {
        console.log(animalRefs);
        if (selectedAnimals.includes(animalId)) {
            selectedAnimals = selectedAnimals.filter((id) => id !== animalId);
            animalRefs[animalId].classList.remove("border-2");
            animalRefs[animalId].classList.remove("border-green-500");
            animalRefs[animalId].classList.remove("bg-green");
        } else {
            selectedAnimals.push(animalId);
            animalRefs[animalId].classList.add("border-2");
            animalRefs[animalId].classList.add("border-green-500");
            animalRefs[animalId].classList.add("bg-green");

        }

        if (selectedAnimals.length === 2) {
            showBreedButton = true;
        } else {
            showBreedButton = false;
        }
    }

    async function breedAnimals() {
        const response = await fetch(
            "http://localhost:5000/api/breed_animals",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    animal_id_1: selectedAnimals[0],
                    animal_id_2: selectedAnimals[1],
                    user_id: user.id,
                }),
            }
        );

        const result = await response.json();

        if (response.ok) {
            // Refresh the animal list
            message = result.message;
            status = "success";
            showPopup = true;
        } else {
            console.error(result.message);
        }
    }

    function onSuccess() {
        window.location.reload();
    }
</script>

<body>
    <div class="container flex flex-wrap">
        {#each eggs as egg (egg.id)}
            <div class="egg-card p-4 m-4">
                <img
                    src="https://cdn.vox-cdn.com/thumbor/W7fnltoIgaRovhaGC9UG53kHfo4=/0x0:876x584/1400x1050/filters:focal(438x292:439x293)/cdn.vox-cdn.com/uploads/chorus_asset/file/13689000/instagram_egg.jpg"
                    alt="Egg"
                    class="egg-image"
                />
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

    <div class="animals-container container flex flex-wrap">
        {#each animals as animal}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
                class="animal p-4 m-4"
                bind:this={animalRefs[animal.id]}
                on:click={() => selectAnimal(animal.id)}
            >
                <img src={animal.image_url} alt="Animal" class="animal-image" />
                <div class="animal-info">
                    <p>Rarity: {animal.rarity}</p>
                    <p>Species: {animal.species}</p>
                    <p>Name: {animal.name}</p>
                    <p>Yield: {animal.coin_yield} coins/hour</p>
                    <p>Yielded: {animal.coins_yielded}</p>
                </div>
                <button
                    class="burn-animal-btn"
                    on:click={() => burnAnimal(animal.id)}>Burn</button
                >
            </div>
        {/each}
    </div>

    {#if showPopup}
        <MessagePopup
            {message}
            {status}
            {onSuccess}
            on:close={() => window.location.reload()}
        />
    {/if}

    {#if showBreedButton}
        <button on:click={breedAnimals}>Breed Animals</button>
    {/if}

    <div class="flex flex-col justify-center items-center">
        <p>You have {user.coins} coins</p>
    </div>

    <button on:click={to_home}> home </button>

    <button on:click={to_market}> market </button>
</body>

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

    .hatch-btn,
    .burn-animal-btn {
        background-color: #4caf50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: 0.3s;
    }

    .hatch-btn:hover,
    .burn-animal-btn:hover {
        background-color: #45a049;
    }

    .selected {
        border: 2px solid limegreen;
        box-sizing: border-box;
        @apply bg-green;
    }
</style>
