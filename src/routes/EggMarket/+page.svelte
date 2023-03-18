<!-- EggMarket.svelte -->
<script>
    export let user = {};
    export let egg = {
        rarity: "common",
        image: "/path/to/egg-image.png",
        price: 10,
    };

    function buyEgg() {
        // Handle egg purchase logic here
        console.log("Egg purchased by", user.username);
    }
</script>

<div class="container flex flex-col justify-center items-center h-screen">
    <div class="egg-market float-div">
        <img src={egg.image} alt="Egg" class="egg-image" />
        <div class="egg-info">
            <p>Rarity: {egg.rarity}</p>
            <p>Price: {egg.price} coins</p>
        </div>
        <button class="buy-egg-btn" on:click={buyEgg}>Buy Egg</button>
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
