<script>
    import { onMount } from 'svelte';
    import Navbar from '../../components/Navbar.svelte';

    let listings = [];
    var user = {};
    var isEditing = false;
    var currListing = {};
    onMount(async () => {
        // Fetch listings for the current user
        user = await check_session();
        const response = await fetch('http://localhost:5000/api/user_listings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: user.username }),
        });
        listings = await response.json();
        
    });

    function editListing(listing) {
        // Set the current listing to the listing that is being edited
        currListing = listing;
        isEditing = true;
    }

    async function cancelListing(listing) {
        // Send request to cancel listing
        const res = await fetch (`http://localhost:5000/api/cancel_listing`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: listing.id,
                user_id: user.id,
            }),
        });

        if (res.ok) {
            // Refresh page after listing is cancelled
            window.location.reload();
        } else {
            alert('HTTP-Error: ' + res.status);
        }
    }

    async function check_session() {
        // Check if the sessionid is valid
        var sessionid = window.sessionStorage.getItem("sessionid");
        var username = window.sessionStorage.getItem("username");

        if (!sessionid || !username) {
            // Redirect to the login page if the sessionid or username is not present
            window.location.href = "/login";
        }

        console.log(sessionid, username);

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

        return user;
    }

    async function saveEdit() {
        // Send request to update listing
        const res = await fetch(`http://localhost:5000/api/update_listing`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: currListing.id,
                listing_name: currListing.listing_name,
                price: currListing.price,
            }),
        });

        if (res.ok) {
            // Refresh page after listing is updated
            window.location.reload();
        } else {
            alert('HTTP-Error: ' + res.status);
        }
    }

    function cancelEdit() {
        // Cancel editing the listing
        isEditing = false;
    }
</script>

<body class="flex flex-col w-screen items-center h-screen bg-background">
    <header class="flex items-center justify-center w-screen p-6 bg-dark_blue">
        <div class="flex-1" />
        <h1 class="text-white font-title font-semibold text-2xl flex-1 text-center">
            My Listings
        </h1>
        <div class="flex-1" />
    </header>

    <Navbar />

    <div class="flex flex-wrap justify-center gap-4">
        {#each listings as listing}
            <div class="bg-white p-4 rounded shadow-md text-center w-64">
                <img
                    src={listing.image}
                    alt={listing.listing_name}
                    class="w-48 h-48 mx-auto mb-4 border-b"
                />
                <ul class="listing-info list-none pl-0 mb-4">
                    <li
                        class="flex justify-between border-b border-gray-200 pb-2"
                    >
                        <p class="capitalize font-body font-semibold">Item:</p>
                        <p class="capitalize font-body font-semibold">
                            {listing.listing_name}
                        </p>
                    </li>
                    <li
                        class="flex justify-between border-b border-gray-200 pb-2"
                    >
                        <p class="capitalize font-body font-semibold">Type:</p>
                        <p class="capitalize font-body font-semibold">
                            {listing.item_type}
                        </p>
                    </li>
                    {#if listing.item_type != 'egg'}
                    <li
                        class="flex justify-between border-b border-gray-200 pb-2"
                    >
                        <p class="capitalize font-body font-semibold">Name:</p>
                        <p class="capitalize font-body font-semibold">
                            {listing.name}
                        </p>
                    </li>
                    {/if}
                    <li
                        class="flex justify-between border-b border-gray-200 pb-2"
                    >
                        <p class="capitalize font-body font-semibold">Rarity:</p>
                        <p class="capitalize font-body font-semibold">
                            {listing.rarity}
                        </p>
                    </li>
                    {#if listing.item_type != 'egg'}
                    <li
                        class="flex justify-between border-b border-gray-200 pb-2"
                    >
                        <p class="capitalize font-body font-semibold">
                            Yield Rate:
                        </p>
                        <p class="capitalize font-body font-semibold">
                            {listing.yield_rate}
                        </p>
                    </li>
                    {/if}
                        <li class="flex justify-between pt-2">
                            <p class="font-body font-semibold">Price:</p>
                            <p class="font-body font-semibold">
                                {listing.price} coins
                            </p>
                        </li>

                        <li class="flex justify-between pt-2">
                            <p class="font-body font-semibold">Status:</p>
                            <p class="font-body font-semibold">
                                {listing.status}
                            </p>
                        </li>
                    </ul>
                    {#if listing.status != 'Cancelled'}
                    <div class="flex justify-center gap-4">
                        <button
                            class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                            on:click={() => editListing(listing)}
                        >
                            Edit
                        </button>
                        <button
                            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                            on:click={() => cancelListing(listing)}
                        >
                            Cancel
                        </button>
                    </div>
                    {/if}
                </div>
        {/each}
    </div>

    {#if isEditing}
        <div
            class="fixed top-0 left-0 w-screen h-screen flex items-center justify-center z-10"
        >
            <div class="bg-white shadow-lg rounded p-6">
                <label
                    for="name"
                    class="block font-medium text-gray-700 mb-2"
                >
                    Listing Name
                </label>
                <input
                    type="text"
                    name="name"
                    id="name"
                    class="border rounded w-full py-2 px-3 mb-3"
                    bind:value={currListing.listing_name}
                />

                <label
                    for="price"
                    class="block font-medium text-gray-700 mb-2"
                >
                    Price
                </label>
                <input
                    type="text"
                    name="price"
                    id="price"
                    class="border rounded w-full py-2 px-3 mb-3"
                    bind:value={currListing.price}
                />


                <div class="flex justify-center">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"
                        on:click={saveEdit}
                    >
                        Save
                    </button>
                    <button
                        class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
                        on:click={cancelEdit}
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    {/if}
</body>

<style>
    img {
        object-fit: cover;
    }
</style>