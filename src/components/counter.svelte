<script>
    var count = 0;
    export var starting = 0;
    function increase() {
        starting++;
    }

    function decrease() {
        starting--;
    }

</script>

<button on:click={increase} on:dblclick={decrease} class = "w-1/2 bg-black text-white rounded-xl">
    {starting}
</button>