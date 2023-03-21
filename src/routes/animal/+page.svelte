<script>
    import { onMount } from "svelte";
    import Navbar from "../../components/Navbar.svelte";
    var animal = {};
    onMount(async () => {
        const params = new URLSearchParams(window.location.search);
        var animalId = params.get("id");
        const response = await fetch(`http://localhost:5000/api/animal`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ animal_id: animalId }),
        });

        animal = await response.json();
        animal.dob = new Date(animal.dob * 1000);
        animal.dob = formatDate(animal.dob);
        if (response.ok) {
            console.log(animal);
            const res = await fetch(`http://localhost:5000/api/update-coins`);
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

    <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded my-4"
        on:click={backToInventory}
    >
        Back to Inventory
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
