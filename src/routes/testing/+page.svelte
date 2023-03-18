<script>
    async function createTesting() {
      const data = {
        message: "good bye world",
      };
  
      const response = await fetch("http://localhost:5000/api/testing", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
  
      if (response.ok) {
        const result = await response.json();
        console.log(result);
      } else {
        console.error("Error creating testing object:", response.status);
      }
    }
  </script>
  
  <button on:click={createTesting}>Create Testing Object</button>
  