<script>
    import { slide } from "svelte/transition";
    var isOpen = false;
    // var username = window.sessionStorage.getItem("username");
    function toggleNav() {
        isOpen = !isOpen;
    }

    function toHome() {
        window.location.href = `/home`;
    }

    function toMarket() {
        window.location.href = `/market`;
    }

    function toInventory() {
        window.location.href = `/inventory`;
    }

    function toListings() {
        window.location.href = `/listings`;
    }

    async function logout() {
        // get user from session storage
        var user = window.sessionStorage.getItem("username");
        const res = await fetch('http://localhost:5000/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: user
            })
        });

        if (res.ok) {
            window.sessionStorage.removeItem("sessionid");
            window.sessionStorage.removeItem("username");
            window.location.href = "/";
        } else {
            alert("HTTP-Error: " + res.status);
        }
    }
</script>

<aside class="navbar">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="navbar-brand" on:click={toggleNav}>CyberQuarium</div>
    {#if isOpen}
        <nav
            class="navbar-menu"
            class:bg-dark_blue={isOpen}
            transition:slide={{ duration: 300 }}
        >
            <ul>
                <!-- <li>{username}'s CyberQuarium</li> -->
                <li><button on:click={toHome} class="navbar-item">Home</button></li>
                <li><button on:click={toMarket} class="navbar-item">Market</button></li>
                <li><button on:click={toInventory} class="navbar-item">Inventory</button></li>
                <li><button on:click={toListings} class="navbar-item">Listings</button></li>
                <li><button on:click={logout} class="navbar-item logout">Logout</button></li>

            </ul>
        </nav>
    {/if}
</aside>

<style>
    .navbar {
        @apply w-[10vw] h-screen fixed top-0 left-0 text-background flex flex-col items-center;
    }

    .navbar-brand {
        @apply font-semibold text-2xl py-4 cursor-pointer font-title mt-2;
    }

    .navbar-menu {
        @apply flex-1 flex flex-col justify-center items-center w-full;
    }

    ul {
        @apply list-none pl-0 h-full flex flex-col justify-center;
    }

    .navbar-item {
        @apply bg-transparent text-background font-semibold text-xl mb-4 px-4 py-2 rounded-md w-full text-center transition-colors duration-300;
    }

    .navbar-item:hover {
        @apply bg-amethyst text-background;
    }

    .logout {
        @apply text-chilli_red;
    }

    .logout:hover {
        @apply bg-chilli_red text-background;
    }
</style>
