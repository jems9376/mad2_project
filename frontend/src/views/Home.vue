<template>
    <div class="home-container">
      <h1>Welcome to Vehicle Parking System</h1>
      <div class="home-button-group">
        <router-link to="/login">
          <button>Login</button>
        </router-link>
        <router-link to="/register">
          <button>Register</button>
        </router-link>
      </div>
    </div>
</template>
  
<script>
  export default {
    name: 'HomeView'
  };
</script>
  
<style>

  .home-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  
  .home-button-group {
    display: flex;
    gap: 20px;
  }

</style>