<!-- Home.svelte -->
<script>
    import { onMount } from "svelte";
    import Navbar from "../../components/Navbar.svelte";

    let username = "";
    var user = {};

    onMount(async () => {
        user = await check_session();
        username = user.username;
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
        var response = await fetch("https://cqflask-v3to2tehtq-lz.a.run.app/api/session", {
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
                `https://cqflask-v3to2tehtq-lz.a.run.app/api/user/${username}`
            );

            if (response.ok) {
                user = await response.json();
            } else {
                alert("HTTP-Error: " + response.status);
            }
        } else {
            // If the sessionid is not valid, redirect to the login page
            window.location.href = "/login";
        }

        return user
    }

    function to_market() {
        window.location.href = `/market`;
    }

    function to_inventory() {
        window.location.href = `/inventory`;
    }
</script>

<body class="min-h-screen flex flex-col items-center justify-between bg-background text-text">
    <Navbar />
    <header class="flex items-center justify-between w-screen p-6 bg-dark_blue">
        <div class="flex-1"></div>
        <h1 class="text-white font-title font-semibold text-2xl flex-1 text-center">
          Home
        </h1>
        <div class="flex items-center text-white font-headers font-semibold flex-1 justify-end">
          <p>You have {user.coins} coins</p>
        </div>
      </header>
      

    <div class="bg-background p-4 rounded text-9xl text-center w-full">
        <p>Welcome Back! {user.username}</p>
    </div>

    <div class="mt-4 flex space-x-4 mb-4">
        <button
            class="bg-ugreen hover:bg-green-800 text-white py-2 px-4 rounded"
            on:click={to_market}
        >
            Market
        </button>
        <button
            class="bg-amethyst hover:bg-purple-600 text-white py-2 px-4 rounded"
            on:click={to_inventory}
        >
            Inventory
        </button>
    </div>
</body>
