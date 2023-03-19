<body
    class="w-screen h-screen bg-background flex flex-col justify-center items-center"
>
    <div class="w-[80vw] flex flex-col items-center gap-[5rem]">
        <h1 class="font-title text-text text-9xl">CyberQuarium</h1>

        <div class="w-full flex flex-row justify-center gap-4">
            <div class="w-1/2 text-center">
                <button on:click={() => goto("/login")}> Login </button>
            </div>

            <div class="w-1/2 text-center">
                <button on:click={() => goto("/register")}> Register </button>
            </div>
        </div>
    </div>
</body>

<style>
    button {
        @apply text-white font-headers text-2xl px-6 py-3 rounded-md bg-amethyst transition-colors duration-300;
    }
</style>

<script>
    function goto(string) {
        window.location.href = string;
    }
</script>
