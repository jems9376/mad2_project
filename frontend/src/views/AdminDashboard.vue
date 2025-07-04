<template>
  <div class="admin-dashboard">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/admin_dashboard/home" class="nav-link">Home</router-link>
        <router-link to="/admin_dashboard/users" class="nav-link">Users</router-link>
        <router-link to="/admin_dashboard/summary" class="nav-link">Summary</router-link>
      </div>
      <div class="nav-middle">
        <h2>Admin Dashboard</h2>
      </div>
      
      <div class="nav-right">
        <button class="nav-button" @click="logout">Logout</button>
        <div class="profile">
          <img src="@/assets/profile-icon.png" alt="Profile" class="profile-icon" />
          <span class="profile-name">Admin</span>
        </div>
      </div>
    </nav>
    
    <router-view/>

  </div>
</template>

<script>

export default {
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

