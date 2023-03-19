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
</script>

<div class="flex flex-col justify-around items-center h-[100vh]">
    <h1>Login</h1>

    <div class="w-[100vw] flex flex-col items-center">
        <form on:submit|preventDefault={loginUser} class="w-1/2 flex flex-col">
            <label for="email">
                Email
                <input
                    type="email"
                    bind:value={email}
                    name="email"
                    id="email"
                />
            </label>

            <label for="password">
                Password
                <input
                    type="password"
                    bind:value={password}
                    name="password"
                    id="password"
                />
            </label>

            <button type="submit">Login</button>
        </form>
    </div>

    {#if showMessage}
        <MessagePopup {message} {status} onClose={closeMessage} />
    {/if}
</div>

<style>
    label {
        @apply flex gap-10 justify-between w-1/2;
    }

    input {
        @apply border-2 border-black;
    }
</style>
