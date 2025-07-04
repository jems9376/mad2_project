<template>
  <div class="user-dashboard">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/user_dashboard/home" class="nav-link">Home</router-link>
        <router-link to="/user_dashboard/history" class="nav-link">History</router-link>
        <router-link to="/user_dashboard/summary" class="nav-link">Summary</router-link>
      </div>

      <div class="nav-middle">
        <h2>{{  name }}'s Dashboard</h2>
      </div>

      <div class="nav-right">
        <button class="nav-button" @click="logout">Logout</button>
        <div class="profile" @click="editProfile">
          <router-link to="/user_dashboard/profile" class="nav-link">
            <span class="profile-name">
            <img src="@/assets/profile-icon.png" alt="Profile" class="profile-icon" />
            User
          </span>
          </router-link>
        </div>
      </div>
    </nav>

    <router-view/>

  </div>
</template>

<script>

export default {  
  data() {
    return {
      name: localStorage.getItem('name')
    }
  },
  methods: {
    async logout(){
      try{
          await fetch("http://localhost:5000/logout");
      } catch (error){
          console.warn('Logout request failed:', error.response?.data || error.message);
      }
      localStorage.removeItem('user_id');
      localStorage.removeItem('role');
      this.$router.push('/login')
  }
  }
};
</script>

