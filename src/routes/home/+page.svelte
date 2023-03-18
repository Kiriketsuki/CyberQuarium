<script>
    import { onMount } from 'svelte';
    var data;
    onMount(async ()=> {
        const res = await fetch('http://localhost:5000/api/view_testings');
        data = await res.json();
        console.log(data.testings[0].message);
        data = data.testings[0].message;
    })
    
</script>

<body>
    <h1>
        Hello World
    </h1>

    <ul>
        <li>
            {data}
        </li>
    </ul>
</body>