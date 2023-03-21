<script>
    import MessagePopup from "../../components/MessagePopup.svelte";
    import app from "../../firebase.js";
    import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
    var message = "";
    var status = "error";
    var showMessage = false;
    var email = "";
    var user = {};

    const auth = getAuth(app);
    async function googleLogin() {
        try {
            const provider = new GoogleAuthProvider();
            const result = await signInWithPopup(auth, provider);

            // If sucessful, redirect to home page
            if (result) {
                user = result.user;
                var username = user.email.split('@')[0];
                const response = await fetch("https://cqflask-v3to2tehtq-lz.a.run.app/google", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email: user.email, username: username }),
                });
                const result2 = await response.json();
                message = result2.message;
                status = result2.status;
                showMessage = true;
                sessionStorage.setItem("username", username);
                sessionStorage.setItem("sessionid", result.sessionID);
            }

        } catch (error) {
            console.log(error);
        }
    }

    async function handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        email = formData.get("email");
        const password = formData.get("password");
        const confirmPassword = formData.get("confirmPassword");

        // Replace this with your registration API endpoint
        const apiUrl = "https://cqflask-v3to2tehtq-lz.a.run.app/register";

        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password, confirmPassword }),
        });

        const result = await response.json();
        message = result.message;
        status = result.status;
        sessionStorage.setItem("username", email.split('@')[0]);
        sessionStorage.setItem("sessionid", result.sessionID);
        showMessage = true;
    }

    // Add this function to close the error message popup
    function closeMessage() {
        showMessage = false;
    }

    // Add this function to handle success and proceed to the next step
    function proceed() {
        user = { username: email.split('@')[0] };
        window.location.href = `/home`;
        closeMessage();
    }

    function toLogin() {
        window.location.href = "/login";
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

    <main class="flex flex-col justify-around items-center h-[80vh]">
        <h1 class="text-white font-title font-semibold text-9xl">
            CyberQuarium Registration
        </h1>
        <form
            action=""
            class="flex flex-col justify-between items-center w-[30vw]"
            on:submit|preventDefault={handleSubmit}
        >
            <label for="email">
                <p>Email:</p>
                <input type="email" name="email" id="email" />
            </label>

            <label for="password">
                <p>Password:</p>
                <input type="password" name="password" id="password" />
            </label>

            <label for="confirmPassword">
                <p>Confirm Password:</p>
                <input
                    type="password"
                    name="confirmPassword"
                    id="confirmPassword"
                />
            </label>

            <div class="flex gap-4 mt-4">
                <button type="submit" class="hover:bg-amethyst hover:text-background">Register</button>
                <button type="button" on:click={toLogin} class="hover:bg-amethyst hover:text-background">Login</button>
                <button type="button" on:click={googleLogin} class="bg-red-600 text-white px-4 py-2 rounded">
                    Sign Up with Google
                </button>                
            </div>
        </form>
    </main>

    {#if showMessage}
        <MessagePopup
            {message}
            {status}
            onClose={closeMessage}
            onSuccess={proceed}
        />
    {/if}
</body>

