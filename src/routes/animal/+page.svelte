<script>
    import { onMount } from "svelte";
    import Navbar from "../../components/Navbar.svelte";
    var animal = {};
    var isEditing = false;
    var nicknameInput = "";
    onMount(async () => {
        const params = new URLSearchParams(window.location.search);
        var animalId = params.get("id");
        const response = await fetch(
            `http://localhost:5000/api/animal`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ animal_id: animalId }),
            }
        );

        animal = await response.json();
        animal.dob = new Date(animal.dob * 1000);
        animal.dob = formatDate(animal.dob);
        if (response.ok) {
            console.log(animal);
            const res = await fetch(
                `http://localhost:5000/api/update_coins`
            );
        } else {
            window.location.href = "/inventory";
        }
    });

    function backToInventory() {
        window.location.href = "/inventory";
    }

    function padTo2Digits(num) {
        return num.toString().padStart(2, "0");
    }

    function formatDate(date) {
        return (
            [
                date.getFullYear(),
                padTo2Digits(date.getMonth() + 1),
                padTo2Digits(date.getDate()),
            ].join("-") +
            " " +
            [
                padTo2Digits(date.getHours()),
                padTo2Digits(date.getMinutes()),
                padTo2Digits(date.getSeconds()),
            ].join(":")
        );
    }

    function editNickname() {
        isEditing = true;
    }

    async function saveNickname() {
        // send request to update animal's nickname
        isEditing = false;
        const res = await fetch(
            `http://localhost:5000/api/update_nickname`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    animal_id: animal.animal_id,
                    nickname: nicknameInput,
                }),
            }
        );

        if (res.ok) {
            animal.nickname = nicknameInput;
        }

        nicknameInput = "";
    }

    function cancelNicknameEdit() {
        isEditing = false;
    }
</script>

<body class="flex flex-col w-screen items-center h-screen bg-background">
    <header class="flex items-center justify-center w-screen p-6 bg-dark_blue">
        <div class="flex-1" />
        <h1
            class="text-white font-title font-semibold text-2xl flex-1 text-center"
        >
            {animal.name}
        </h1>
        <div class="flex-1" />
    </header>

    <Navbar />

    <div
        class="flex w-full h-[80vh] items-center justify-between rounded bg-white mb-4"
    >
        <img
            src={animal.image_url}
            alt={animal.species}
            class="w-2/3 rounded-lg h-[70vh]"
        />
        <ul class="text-left w-1/3 flex flex-col items-center">
            {#if animal.nickname != null}
                <li class="mb-4">
                    <span class="font-medium">Nickname:</span>
                    <p class="font-body capitalize">{animal.nickname}</p>
                </li>
            {/if}

            <li class="mb-4">
                <span class="font-medium">Date of Birth:</span>
                <p class="font-body capitalize">{animal.dob}</p>
            </li>
            <li class="mb-4">
                <span class="font-medium">Rarity:</span>
                <p class="font-body capitalize">{animal.rarity}</p>
            </li>
            <li class="mb-4">
                <span class="font-medium">Species:</span>
                <p class="font-body capitalize">{animal.species}</p>
            </li>
            <li class="mb-4">
                <span class="font-medium">Name:</span>
                <p class="font-body capitalize">{animal.name}</p>
            </li>
            <li class="mb-4">
                <span class="font-medium">Coin Yield:</span>
                <p class="font-body capitalize">
                    {Number(animal.coin_yield).toFixed(3)} coins/hour
                </p>
            </li>
            <li class="mb-4">
                <span class="font-medium">Coins Yielded:</span>
                <p class="font-body capitalize">
                    {Number(animal.coins_yielded).toFixed(3)}
                </p>
            </li>
            <li class="mb-4">
                <span class="font-medium">Owner:</span>
                <p class="font-body capitalize">{animal.username}</p>
            </li>
        </ul>
    </div>

    {#if isEditing}
        <div
            class="fixed top-0 left-0 w-screen h-screen flex items-center justify-center z-10"
        >
            <div class="bg-white shadow-lg rounded p-6">
                <label
                    for="nickname"
                    class="block font-medium text-gray-700 mb-2"
                >
                    New Nickname
                </label>
                <input
                    type="text"
                    name="nickname"
                    id="nickname"
                    class="border rounded w-full py-2 px-3 mb-3"
                    bind:value={nicknameInput}
                />
                <div class="flex justify-center">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"
                        on:click={saveNickname}
                    >
                        Save
                    </button>
                    <button
                        class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
                        on:click={cancelNicknameEdit}
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    {/if}

    <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded my-4"
        on:click={backToInventory}
    >
        Back to Inventory
    </button>

    <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded my-4"
        on:click={editNickname}
    >
        Edit Nickname
    </button>
</body>

<style>
    img {
        object-fit: cover;
    }

    li {
        @apply flex flex-row font-body text-3xl w-[90%] justify-between;
    }
</style>
