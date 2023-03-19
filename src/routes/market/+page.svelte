<script>
    import { onMount } from "svelte";
    import MessagePopup from "../../components/MessagePopup.svelte";

    var username = "";
    var user = {};
    var egg = {};
    var status = "error";
    var message = "";
    var showPopup = false;

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
        update_egg();
    });

    async function update_egg() {
        var res = await fetch("http://localhost:5000/api/create_egg");
        egg = await res.json();
        egg.image =
            "http://photos.newswire.ca/images/20130327_C8486_PHOTO_EN_24852.jpg";
    }

    async function buyEgg() {
        if (user.coins < egg.cost) {
            message = "Insufficient coins to buy the egg!";
            status = "error";
            showPopup = true;
        } else {
            const response = await fetch(
                `http://localhost:5000/api/buy_egg/${username}`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(egg),
                }
            );

            if (response.ok) {
                user = await response.json();
                message = "Egg successfully purchased!";
                status = "success";
                showPopup = true;
            } else {
                message = "There was an issue purchasing the egg.";
                status = "error";
                showPopup = true;
            }
        }
    }

    function closePopup() {
        showPopup = false;
    }

    function successRefresh() {
        showPopup = false;
        update_egg();
    }

    function to_inventory() {
        window.location.href = `/inventory?username=${encodeURIComponent(
            user.username
        )}`;
    }
</script>

<body
    class="h-screen w-screen flex flex-col items-center gap-10 bg-background text-text justify-between"
>
    <header class="flex items-center justify-between w-full p-6 bg-dark_blue">
        <h1 class="text-white font-title font-semibold text-2xl">Market</h1>
        <div class="flex items-center text-white font-headers font-semibold">
            <p>You have {user.coins} coins</p>
        </div>
    </header>

    {#if showPopup}
        <MessagePopup
            {message}
            {status}
            onClose={closePopup}
            onSuccess={successRefresh}
        />
    {/if}

    <div class="bg-white p-4 rounded shadow-md text-center w-64">
        <img src={egg.image} alt="Egg" class="w-48 mx-auto mb-4 border-b" />
        <ul class="egg-info list-none pl-0 mb-4">
            <li class="flex justify-between border-b border-gray-200 pb-2">
                <p class="capitalize font-body font-semibold">Rarity:</p>
                <p class="capitalize font-body font-semibold">{egg.rarity}</p>
            </li>
            <li class="flex justify-between pt-2">
                <p class="font-body font-semibold">Price:</p>
                <p class="font-body font-semibold">{egg.cost} coins</p>
            </li>
        </ul>
        <button class="bg-ugreen hover:bg-green-800 text-white py-2 px-4 rounded w-full" on:click="{buyEgg}">Buy Egg</button>
    </div>

    <button
        class="mb-4 bg-amethyst hover:bg-purple-600 text-white py-2 px-4 rounded"
        on:click={to_inventory}
    >
        Inventory
    </button>
</body>
