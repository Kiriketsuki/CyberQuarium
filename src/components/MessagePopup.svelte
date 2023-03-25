<script>
    export var message = "";
    export var status = "error";
    export var onClose = function () {};
    export var onSuccess = function () {};
</script>

<div
    class="message-popup fixed top-0 left-0 w-screen h-screen flex justify-center items-center z-50"
>
    <div
        class="bg-white rounded-lg shadow-lg p-8 flex flex-col w-full md:w-1/3"
    >
        <div class="flex items-center justify-between">
            <h2
                class="text-xl font-semibold"
                class:success={status === "success"}
                class:error={status === "error"}
            >
                {message}
            </h2>
            {#if status === "error"}
                <button
                    on:click={onClose}
                    class="text-gray-500 hover:text-gray-600"
                >
                    &times;
                </button>
            {/if}

            {#if status === "success"}
                <button
                    on:click={onSuccess}
                    class="mt-4 bg-green-500 text-green px-4 py-2 rounded self-center z-100"
                >
                    Proceed
                </button>
            {/if}
        </div>
    </div>
</div>

<style>
    .success {
        color: green;
    }
    .error {
        color: red;
    }
</style>
