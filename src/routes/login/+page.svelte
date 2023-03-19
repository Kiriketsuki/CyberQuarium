<!-- Login.svelte -->
<script>
    import MessagePopup from "../../components/MessagePopup.svelte";
    // import { Cookies } from "@sveltejs/kit";
    import { onMount } from "svelte";

    let email = "";
    let password = "";
    let message = "";
    let status = "error";
    let showMessage = false;
    let user = {};

    // onMount(async () => {
    //     console.log(Cookies.Page.get("username"));
    // });

    async function loginUser() {
        const data = { email, password };

        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        };

        const response = await fetch(
            "http://localhost:5000/login",
            requestOptions
        );
        const result = await response.json();

        message = result.message;
        status = result.status;
        showMessage = true;

        if (status === "success") {
            user = { username: email.split('@')[0] };
            var sessionid = result.sessionID;
            window.sessionStorage.setItem("username", user.username);
            window.sessionStorage.setItem("sessionid", sessionid);
            window.location.href = `/home`;
            closeMessage();
        }
    }

    function closeMessage() {
        showMessage = false;
    }

    function toRegister() {
        window.location.href = "/register";
    }
</script>

<style>
    h1 {
        @apply font-headers text-text mb-8;
    }

    label {
        @apply flex gap-10 justify-between items-center w-full mb-4;
    }

    input {
        @apply border-2 border-dark_blue w-3/5;
    }

    button {
        @apply bg-dark_blue text-text font-headers text-xl px-4 py-2 rounded-md transition-colors duration-300;
    }
</style>

<body class="w-screen h-screen bg-background flex flex-col items-center justify-between">


    <div class="flex flex-col justify-around items-center h-[80vh]">

        <h1 class="text-white font-title font-semibold text-9xl">
            CyberQuarium Login
        </h1>

        <form on:submit|preventDefault={loginUser} class="flex flex-col justify-between items-center w-[30vw]">
            <label for="email">
                <p>
                    Email:
                </p>
                <input
                    type="email"
                    bind:value={email}
                    name="email"
                    id="email"
                />
            </label>

            <label for="password">
                <p>
                    Password:
                </p>
                <input
                    type="password"
                    bind:value={password}
                    name="password"
                    id="password"
                />
            </label>

            <div>
                <button type="submit" class="mt-4 hover:bg-amethyst hover:text-background">Login</button>
                <button type="button" on:click={toRegister}>Register</button>
            </div>
        </form>
    </div>

    {#if showMessage}
        <MessagePopup {message} {status} onClose={closeMessage} />
    {/if}
</body>

