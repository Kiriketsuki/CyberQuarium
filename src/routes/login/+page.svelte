<!-- Login.svelte -->
<script>
    import MessagePopup from "../../components/MessagePopup.svelte";
    import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
    import app from "../../firebase.js";

    var email = "";
    var password = "";
    var message = "";
    var status = "error";
    var showMessage = false;
    var user = {};


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
            user = { username: email.split("@")[0] };
            var sessionid = result.sessionID;
            window.sessionStorage.setItem("username", user.username);
            window.sessionStorage.setItem("sessionid", sessionid);
            window.location.href = `/home`;
            closeMessage();
        }
    }
    const auth = getAuth(app);
    async function googleLogin() {
        try {
            const provider = new GoogleAuthProvider();
            const result = await signInWithPopup(auth, provider);

            // If sucessful, redirect to home page
            if (result) {
                user = result.user;
                var username = user.email.split("@")[0];
                const response = await fetch("http://localhost:5000/google", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email: user.email,
                        username: username,
                    }),
                });
                const result2 = await response.json();
                message = result2.message;
                status = result2.status;
                if (status === "success") {
                    user = { username: email.split("@")[0] };
                    var sessionid = result.sessionID;
                    window.sessionStorage.setItem("username", user.username);
                    window.sessionStorage.setItem("sessionid", sessionid);
                    window.location.href = `/home`;
                } else {
                    throw new Error(message);
                }
            }
        } catch (error) {
            console.log(error);
        }
    }

    function closeMessage() {
        showMessage = false;
    }

    function toRegister() {
        window.location.href = "/register";
    }
</script>

<body
    class="w-screen h-screen bg-background flex flex-col items-center justify-between"
>
    <div class="flex flex-col justify-around items-center h-[80vh]">
        <h1 class="text-white font-title font-semibold text-9xl">
            CyberQuarium Login
        </h1>

        <form
            on:submit|preventDefault={loginUser}
            class="flex flex-col justify-between items-center w-[30vw]"
        >
            <label for="email">
                <p>Email:</p>
                <input
                    type="email"
                    bind:value={email}
                    name="email"
                    id="email"
                />
            </label>

            <label for="password">
                <p>Password:</p>
                <input
                    type="password"
                    bind:value={password}
                    name="password"
                    id="password"
                />
            </label>

            <div>
                <button
                    type="submit"
                    class="mt-4 hover:bg-amethyst hover:text-background"
                    >Login</button
                >
                <button type="button" on:click={toRegister}>Register</button>
                <button type="button" on:click={googleLogin} class="bg-red-600 text-white px-4 py-2 rounded">
                    Login with Google
                </button>   
            </div>
        </form>
    </div>

    {#if showMessage}
        <MessagePopup {message} {status} onClose={closeMessage} />
    {/if}
</body>

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
