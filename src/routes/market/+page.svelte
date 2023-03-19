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
            const response = await fetch(`http://localhost:5000/api/user/${username}`);
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
        egg.image = "http://photos.newswire.ca/images/20130327_C8486_PHOTO_EN_24852.jpg"
    }

    async function buyEgg() {
        if (user.coins < egg.cost) {
            message = "Insufficient coins to buy the egg!";
            status = "error";
            showPopup = true;
        } else {
            const response = await fetch(`http://localhost:5000/api/buy_egg/${username}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(egg),
            });

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
        window.location.href = `/inventory?username=${encodeURIComponent(user.username)}`;
    }
</script>

<div class="container mx-auto h-screen flex flex-col justify-center items-center">
    {#if showPopup}
        <MessagePopup {message} {status} onClose={closePopup} onSuccess={successRefresh} />
    {/if}

    <div class="bg-white p-4 rounded shadow-md text-center">
        <img src={egg.image} alt="Egg" class="w-48 mx-auto mb-4" />
        <div class="egg-info mb-4">
        <p>Rarity: {egg.rarity}</p>
            <p>Price: {egg.cost} coins</p>
        </div>
        <button class="bg-green-500 hover:bg-green-600 py-2 px-4 rounded" on:click="{buyEgg}">Buy Egg</button>
    </div>

    <div class="mt-4 text-center">
        <p>You have {user.coins} coins.</p>
    </div>
    
    <button class="mt-4 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded" on:click={to_inventory}>
        Inventory
    </button>
</div>
