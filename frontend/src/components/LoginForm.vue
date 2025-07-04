<template>
  <h1>Welcome to Vehicle Parking System</h1>
    <div class="form-container">
      <h2>Login</h2>
      <div v-if="error" class="error">{{ error }}</div>
      <form @submit.prevent="loginUser">
        <label for="email">Email:</label>
        <input v-model="form.email" type="email" id="email" placeholder="Enter your email" />
  
        <label for="password">Password:</label>
        <input v-model="form.password" 
          :type="passwordVisible? 'text' : 'password'" 
          id="password" placeholder="Enter your password" required />
        
        <div class="password-toggle" style="margin-top: 10px;">
          <input type="checkbox" id="showPassword" v-model="passwordVisible" />
        </div>

        <button type="submit">Login</button>
        <p class="link">
          <router-link to="/register">Don't have an account? Register</router-link>
        </p>
      </form>
    </div>
</template>

<script>

export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      error: '',
      passwordVisible: false
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await fetch("http://localhost:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form)
        });
        if (!response.ok) throw new Error("Login failed");
        const data = await response.json();
        // Store token and role, redirect accordingly
        // localStorage.setItem("token", data.token);
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("role", data.role);
        localStorage.setItem("name", data.name);

        if (data.role == "admin") {
          this.$router.push("/admin_dashboard");
        } else {
          this.$router.push("/user_dashboard");
        }
      } catch (err) {
        console.log(err);
        this.error = err.message;
      }
    }
  }
};
</script>
