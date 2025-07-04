<template>
  <h1>Welcome to Vehicle Parking System</h1>
  <div class="form-container">
    <h2>Register</h2>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="message" class="message">{{ message }}</div>

    <form @submit.prevent="registerUser">
      <label for="name">Name</label>
      <input v-model="form.name" type="text" id="name" required />

      <label for="email">Email</label>
      <input v-model="form.email" type="email" id="email" required />

      <label for="password">Password</label>
      <input v-model="form.password" type="password" id="password" required />

      <label for="address">Address</label>
      <input v-model="form.address" type="text" id="address" required />

      <label for="pin_code">Pin Code</label>
      <input v-model="form.pin_code" type="text" id="pin_code" required />

      <button type="submit">Register</button>
      <p class="link">
        <router-link to="/login">Already have an account? Login</router-link>
      </p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        address: '',
        pin_code: ''
      },
      error: '',
      message: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await fetch("http://localhost:5000/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form)
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.message || "Registration failed");

        this.message = "Registration successful! Please login.";
        this.error = '';
        this.form.name = '';
        this.form.email = '';
        this.form.password = '';
        this.form.address = '';
        this.form.pin_code = '';
      } catch (err) {
        this.error = err.message;
        this.message = '';
      }
    }
  }
};
</script>
