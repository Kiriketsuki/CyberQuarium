<script>
    import { onMount, onDestroy } from "svelte";
    import MessagePopup from "../../components/MessagePopup.svelte";

    var username = "";
    var user = {};
    var eggs = [];
    var animals = [];
    var message = "";
    var status = "error";
    var showPopup = false;
    var isLoading = false;

    onMount(async () => {
        const searchParams = new URLSearchParams(window.location.search);

        if (searchParams.has("username")) {
            username = searchParams.get("username");
            const response = await fetch(
                `http://localhost:5000/api/user/${username}`
            );

            if (response.ok) {
                user = await response.json();
            } else {
                alert("HTTP-Error: " + response.status);
            }
        } else {
            window.location.href = "/login";
        }

        const eggsResponse = await fetch(
            `http://localhost:5000/api/user/${username}/eggs`
        );
        eggs = await eggsResponse.json();

        const animalsResponse = await fetch(
            `http://localhost:5000/api/user/${username}/animals`
        );
        animals = await animalsResponse.json();
        refreshYields(show=false);
        isLoading = false;
    });

    async function hatchEgg(eggId) {
        isLoading = true;
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
            window.location.reload();
        } else {
            alert("HTTP-Error: " + response.status);
        }
        isLoading = false;
    }

    async function refreshYields(show=true) {
        isLoading = true;
        showPopup = show;
        const response = await fetch(
            `http://localhost:5000/api/update-coins`
        );

        if (response.ok) {
            user = await response.json();
            message = "Yields refreshed!";
            status = "success";
            showPopup = true;
        } else {
            message = "There was an issue refreshing the yields.";
            status = "error";
            showPopup = true;
        }
        isLoading = false;
    }

    async function burnAnimal(animalId) {
        isLoading = true;
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
            message = result.message;
            status = "success";
            showPopup = true;
        } else {
            console.error(result.message);
        }
        isLoading = false;
    }

    function toHome() {
        window.location.href = `/home?username=${encodeURIComponent(
            user.username
        )}`;
    }

    function toMarket() {
        window.location.href = `/market?username=${encodeURIComponent(
            user.username
        )}`;
    }

    var selectedAnimals = [];
    var showBreedButton = false;
    var animalRefs = {};

    function selectAnimal(animalId) {
        if (selectedAnimals.includes(animalId)) {
            selectedAnimals = selectedAnimals.filter((id) => id !== animalId);
            // animalRefs[animalId].classList.remove("border-2");
            animalRefs[animalId].classList.remove("border-green-500");
            animalRefs[animalId].classList.remove("bg-green");
        } else {
            selectedAnimals.push(animalId);
            // animalRefs[animalId].classList.add("border-2");
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
        isLoading = true;
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
            message = result.message;
            status = "success";
            showPopup = true;
        } else {
            console.error(result.message);
        }
        isLoading = false;
    }

    function onSuccess() {
        window.location.reload();
    }
</script>

<body class="w-[100vw] flex flex-col items-center">
    <header class="flex items-center justify-between bg-blue-500 p-6 w-full">
        <h1 class="text-white font-semibold text-2xl">
            {user.username}'s Inventory
        </h1>
        <div class="flex items-center text-white font-semibold">
            <p>You have {user.coins} coins</p>
        </div>
    </header>

    <div class="container flex items-center w-100">
        {#each eggs as egg (egg.id)}
            <div class="egg-card p-4 m-4 bg-white rounded shadow-md">
                <img
                    src="https://cdn.vox-cdn.com/thumbor/W7fnltoIgaRovhaGC9UG53kHfo4=/0x0:876x584/1400x1050/filters:focal(438x292:439x293)/cdn.vox-cdn.com/uploads/chorus_asset/file/13689000/instagram_egg.jpg"
                    alt="Egg"
                    class="egg-image"
                />
                <ul class="egg-info list-none pl-0 mt-2">
                    <li>Rarity: {egg.rarity}</li>
                    <li>Price: {egg.cost} coins</li>
                </ul>
                <button
                    class="hatch-btn w-full mt-4 py-2 bg-green text-white rounded hover:bg-green-600"
                    on:click={() => hatchEgg(egg.id)}>Hatch</button
                >
            </div>
        {/each}
    </div>

    <div class="animals-container container flex flex-wrap w-[100vw] items-center justify-center">
        {#each animals as animal}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
                class="animal p-4 m-4 bg-white rounded shadow-md border-2"
                bind:this={animalRefs[animal.id]}
                on:click={() => selectAnimal(animal.id)}
            >
                <img src={animal.image_url} alt="Animal" class="animal-image" />
                <ul class="animal-info list-none pl-0 mt-2">
                    <li>Rarity: {animal.rarity}</li>
                    <li>Species: {animal.species}</li>
                    <li>Name: {animal.name}</li>
                    <li>Yield: {Number(animal.coin_yield).toFixed(3)} coins/hour</li>
                    <li>Yielded: {Number(animal.coins_yielded).toFixed(3)}</li>
                </ul>
                <button
                    class="burn-animal-btn w-full mt-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
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
        <button
            on:click={breedAnimals}
            class="mx-auto mt-4 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
            >Breed Animals</button
        >
    {/if}

    <div class="flex justify-center mt-4">
        <button
            on:click={toHome}
            class="mx-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
            Home</button
        >
        <button
            on:click={toMarket}
            class="mx-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >Market</button
        >

        <button
            on:click={refreshYields}
            class="mx-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >Refresh Yields</button
        >
    </div>
    {#if isLoading}
        <div
            class="loading-spinner-container fixed inset-0 bg-white bg-opacity-80 z-50 flex items-center justify-center"
        >
            <div
                class="loading-spinner w-16 h-16 border-8 border-t-8 border-blue-500 border-solid rounded-full animate-spin"
            />
        </div>
    {/if}
</body>

<style>
    .egg-image {
        width: 200px;
        height: auto;
    }

    .selected {
        /* border: 2px solid limegreen; */
        box-sizing: border-box;
        @apply bg-green;
    }
</style>