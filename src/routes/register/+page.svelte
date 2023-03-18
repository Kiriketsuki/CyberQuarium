<script>
    import MessagePopup from "../../components/MessagePopup.svelte";
    var message = "";
    var status = "error";
    var showMessage = false;
    var email = "";
    async function handleSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        email = formData.get("email");
        const password = formData.get("password");
        const confirmPassword = formData.get("confirmPassword");

        // Replace this with your registration API endpoint
        const apiUrl = "http://localhost:5000/register";

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
        showMessage = true;
    }

    // Add this function to close the error message popup
    function closeMessage() {
        showMessage = false;
    }

    // Add this function to handle success and proceed to the next step
    function proceed() {
        var user = { username: email.split('@')[0] };
        window.location.href = `/home?username=${encodeURIComponent(user.username)}`;
        closeMessage();
    }
</script>

<main class="flex flex-col justify-around items-center h-screen">
    <h1>Registration</h1>

    {#if showMessage}
        <MessagePopup
            {message}
            {status}
            onClose={closeMessage}
            onSuccess={proceed}
        />
    {/if}
    <div class="w-full flex flex-col items-center">
        <form
            action=""
            class="w-1/2 flex flex-col"
            on:submit|preventDefault={handleSubmit}
        >
            <label for="email">
                Email
                <input type="email" name="email" id="email" />
            </label>

            <label for="password">
                Password
                <input type="password" name="password" id="password" />
            </label>

            <label for="confirmPassword">
                Confirm Password
                <input
                    type="password"
                    name="confirmPassword"
                    id="confirmPassword"
                />
            </label>

            <button type="submit">Register</button>
        </form>
    </div>
</main>

<style>
    label {
        @apply flex gap-10 justify-between w-1/2;
    }

    input {
        @apply border-2 border-black;
    }
</style>
