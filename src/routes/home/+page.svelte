<!-- Home.svelte -->
<script>
    import { onMount } from "svelte";
  
    let username = "";
  
    onMount(() => {
      // Get the URL search parameters
      const searchParams = new URLSearchParams(window.location.search);
  
      // Get the username from the search parameters
      if (searchParams.has("username")) {
        username = searchParams.get("username");
      } else {
        // Redirect to the login page if the username is not present
        window.location.href = "/login";
      }
    });
  </script>
  
  <div class="container">
    <h1>Welcome, {username}!</h1>
    <p>This is your home page.</p>
  </div>
  