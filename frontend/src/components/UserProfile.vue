<template>
    <div class="form-container" style="margin: 15px auto">
        <h2 style="margin-top: 0px; margin-bottom: 0px;">Profile</h2>

        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="message" class="message" style=" margin-bottom: 0px;">{{ message }}</div>

        <form @submit.prevent="updateProfile" class="grid-form">
            
            <div class="form-column">
                <label for="user_id">User Id</label>
                <input v-model="profile.user_id" type="text" id="user_id" disabled />

                <label for="name">Name</label>
                <input v-model="profile.name" type="text" id="name" required />
                
                
                <label for="contact_number">Contact Number</label>
                <input v-model="profile.contact_number" type="text" id="contact_number" placeholder="Enter 10 digit number" required />
                
                <label for="pin_code">Pin Code</label>
                <input v-model="profile.pin_code" type="text" id="pin_code" required />
                
            </div>
            <div class="form-column">
                <label for="email">Email</label>
                <input v-model="profile.email" type="email" id="email" disabled />
                
                <label for="password">Password</label>
                <input :type="passwordVisible ? 'text' : 'password'" id="password" v-model="profile.password"/>
                
                <div class="password-toggle">
                    <input type="checkbox" id="showPassword" v-model="passwordVisible" />
                </div>
                
                <label for="vehicle_number" style="margin-top: -10px;">Vehicle Number</label>
                <input v-model="profile.vehicle_number" type="text" id="vehicle_number" placeholder=" Enter vehicle number" required />

                <label for="address">Address</label>
                <input v-model="profile.address" type="text" id="address" required />


                <button type="submit">Update</button>
            </div>
        </form>
    </div>
</template>

<script>

export default {
    data() {
        return {
            profile: [],
            user_id: localStorage.getItem('user_id'),
            passwordVisible: false,
            error: '',
            message: '',
        };
    },
    methods: {
        async fetchData() {
            const resProfile = await fetch(`http://localhost:5000/user/${this.user_id}`); // <-- important check!
            this.profile = await resProfile.json();
            this.profile.password = '';
        },
        async updateProfile() {
            const response = await fetch(`http://localhost:5000/user/${this.user_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.profile)
            })

            if (response.ok) {
                this.message = 'Profile updated';
            } else {
                const err = await response.json();
                this.error = err.message;
            }
            this.fetchData();

        }
    },
    mounted() {
        this.fetchData();
    }
};

</script>

<style scoped>

    .form-container {
        max-width: 800px;
        padding: 20px;
    }

    .grid-form {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        margin-top: 20px;
    }

    .form-column {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>