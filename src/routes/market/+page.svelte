<!-- EggMarket.svelte -->
<script>
    import { onMount } from "svelte";

    let username = "";
    let user = {};
    var egg = {};
    var status = "error";
    var message = "";
    var showPopup = false;

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

        // generate a random egg by calling flask api
        update_egg();
    });

    async function update_egg() {
        var res = await fetch("http://localhost:5000/api/create_egg");
        egg = await res.json();
    };
    import MessagePopup from "../../components/MessagePopup.svelte";

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
                    headers: {
                        "Content-Type": "application/json",
                    },
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
</script>


<div class="container flex flex-col justify-center items-center h-screen">
    {#if showPopup}
        <MessagePopup
            {message}
            {status}
            onClose={closePopup}
            onSuccess={successRefresh}
        />
    {/if}

    <div class="egg-market float-div">
        <img src={egg.image} alt="Egg" class="egg-image" />
        <div class="egg-info">
            <p>Rarity: {egg.rarity}</p>
            <p>Price: {egg.cost} coins</p>
        </div>
        <button class="buy-egg-btn" on:click="{buyEgg}">Buy Egg</button>
    </div>

    <div class="flex flex-col justify-center items-center">
        <p>You have {user.coins} coins.</p>
    </div>
</div>

<style>
    .container {
        width: 100%;
    }

    .egg-market {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .egg-image {
        width: 200px;
        height: auto;
    }

    .egg-info {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .buy-egg-btn {
        background-color: #4caf50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: 0.3s;
    }

    .buy-egg-btn:hover {
        background-color: #45a049;
    }
</style>
