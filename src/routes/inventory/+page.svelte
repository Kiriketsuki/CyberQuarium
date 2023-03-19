<script>
    import { onMount, onDestroy } from "svelte";
    import MessagePopup from "../../components/MessagePopup.svelte";
    import Navbar from "../../components/Navbar.svelte";
    // var username = window.sessionStorage.getItem("username");
    // console.log(username);
    var username = "";
    var user = {};
    var eggs = [];
    var animals = [];
    var message = "";
    var status = "error";
    var showPopup = false;
    var isLoading = false;

    onMount(async () => {
        // isLoading = true;
        user = await check_session();
        username = user.username;
        
        const eggsResponse = await fetch(
            `http://localhost:5000/api/user/${username}/eggs`
        );
        eggs = await eggsResponse.json();

        const animalsResponse = await fetch(
            `http://localhost:5000/api/user/${username}/animals`
        );
        animals = await animalsResponse.json();
        refreshYields(false);
        isLoading = false;
    });

    async function check_session() {
        // Check if the sessionid is valid
        var sessionid = window.sessionStorage.getItem("sessionid");
        var username = window.sessionStorage.getItem("username");

        if (!sessionid || !username) {
            // Redirect to the login page if the sessionid or username is not present
            window.location.href = "/login";
        }

        console.log(sessionid, username)

        // Send a request to the server to check if the sessionid is valid. The payload is the username and the sessionid
        var response = await fetch("http://localhost:5000/api/session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                sessionid: sessionid,
            }),
        });

        if (response.ok) {
            // If the sessionid is valid, get the user from the database
            var response = await fetch(
                `http://localhost:5000/api/user/${username}`
            );

            if (response.ok) {
                user = await response.json();
                return user;
            } else {
                alert("HTTP-Error: " + response.status);
            }
        } else {
            // If the sessionid is not valid, redirect to the login page
            window.location.href = "/login";
        }

        return user
    }

    async function hatchEgg(eggId) {
        console.log(user)
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

    async function refreshYields(show) {
        isLoading = true;
        showPopup = show;
        const response = await fetch(`http://localhost:5000/api/update-coins`);

        if (response.ok) {
            var res = await response.json();
            message = "Yields refreshed!";
            status = "success";
            showPopup = false;
        } else {
            message = "There was an issue refreshing the yields.";
            status = "error";
            showPopup = false;
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
        window.location.href = `/home`;
    }

    function toMarket() {
        window.location.href = `/market`;
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

<body
    class="mx-auto min-h-screen w-screen flex flex-col items-center justify-between bg-background text-text"
>
    <header class="flex items-center justify-between w-full p-6 bg-dark_blue">
        <div class="flex-1"></div>
        <h1 class="text-white font-title font-semibold text-2xl flex-1">
            {user.username}'s Inventory
        </h1>
        <div class="flex items-center text-white font-headers font-semibold">
            <p>You have {user.coins} coins</p>
        </div>
    </header>

    <Navbar />

    <div class="container flex flex-wrap items-center justify-center gap-4">
        {#each eggs as egg (egg.id)}
            <div class="egg-card p-4 bg-white rounded shadow-md">
                <img
                    src="http://photos.newswire.ca/images/20130327_C8486_PHOTO_EN_24852.jpg"
                    alt="Egg"
                    class="egg-image w-48 mx-auto mb-4"
                />
                <ul class="egg-info list-none pl-0 mb-4">
                    <li>
                        <p class="info-label capitalize">Rarity:</p>
                        <p class="info-label capitalize">{egg.rarity}</p>
                    </li>
                    <li>
                        <p class="info-label">Price:</p>
                        <p class="info-label">{egg.cost} coins</p>
                    </li>
                </ul>
                <button
                    class="hatch-btn w-full mt-4 py-2 bg-ugreen text-white rounded hover:bg-green-800"
                    on:click={() => hatchEgg(egg.id)}>Hatch</button
                >
            </div>
        {/each}
    </div>

    <div
        class="animals-container container flex flex-wrap items-center justify-center gap-4"
    >
        {#each animals as animal}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
                class="animal p-4 bg-white rounded shadow-md border-2"
                bind:this={animalRefs[animal.id]}
                on:click={() => selectAnimal(animal.id)}
            >
                <img
                    src={animal.image_url}
                    alt="Animal"
                    class="animal-image w-48 mx-auto mb-4"
                />
                <ul class="animal-info list-none pl-0 mb-4">
                    <li>
                        <p class="info-label capitalize">Rarity:</p>
                        <p class="info-label capitalize">{animal.rarity}</p>
                    </li>
                    <li>
                        <p class="info-label">Species:</p>
                        <p class="info-label">{animal.species}</p>
                    </li>
                    <li>
                        <p class="info-label">Name:</p>
                        <p class="info-label">{animal.name}</p>
                    </li>
                    <li>
                        <p class="info-label">Yield:</p>
                        <p class="info-label">
                            {Number(animal.coin_yield).toFixed(3)} coins/hour
                        </p>
                    </li>
                    <li>
                        <p class="info-label">Yielded:</p>
                        <p class="info-label">
                            {Number(animal.coins_yielded).toFixed(3)}
                        </p>
                    </li>
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

    <div class="flex justify-center mb-4">
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
            on:click={refreshYields(true)}
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
    li {
        @apply flex justify-between;
    }

    li:not(:last-child) {
        @apply border-b border-gray-200 pb-2;
    }

    li:last-child {
        @apply pt-2;
    }

    .info-label {
        @apply font-body font-semibold;
    }
</style>
