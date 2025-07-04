<template>
    <div>
      <h2>Registered Users</h2>
      
      <table class = "user-table">
          <thead>
            <tr>
                <th style="text-align: center;">User Id</th>
                <th>Name</th>
                <th>Email</th>
                <th>Address</th>
                <th>Pin Code</th>
            </tr>
          </thead>
          <tbody v-if="users.length > 0">
            <tr v-for="user in users" :key="user.user_id">
                <td style="text-align: center;">
                    <button class="spot" @click="openUserModal(user.user_id)">
                        {{ user.user_id }}
                    </button>
                </td>
                <td>{{ user.email }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.address }}</td>
                <td>{{ user.pin_code }}</td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
                <td colspan="5" style="text-align: center;">No users found</td>
            </tr>
          </tbody>
      </table>

    <div v-if="showUserModal" class="modal">
        <div class="modal-content" style="max-width: 1180px; margin: 0 auto;">
            <h3>Parking History of User</h3>
            <table class = "history-table">
                <thead>
                    <tr>
                        <th style="text-align: center;">Record Id</th>
                        <th>Lot Name / Lot Id</th>
                        <th>Spot Id</th>
                        <th>Vehicle Number</th>
                        <th>Parking Time</th>
                        <th>Release Time</th>
                        <th>Parking Cost</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="record in userRecords" :key="record.record_id">
                        <td style="text-align: center;">{{ record.record_id }}</td>
                        <td>{{ record.lot_name }} / {{ record.lot_id }}</td>
                        <td>{{ record.spot_id }}</td>
                        <td>{{ record.vehicle_number }}</td>
                        <td>{{ record.parking_timestamp }}</td>
                        <td v-if="record.leaving_timestamp">{{ record.leaving_timestamp }}</td>
                        <td v-else>Not released</td>
                        <td>{{ record.parking_cost }}</td>
                    </tr>
                </tbody>
            </table>
            <div class="modal-buttons">
                <button type="button" @click="closeUserModal" class="close-button">Close</button>
            </div>
        </div>
    </div>
      
    </div>
</template>

<script>

    export default{
        data(){
            return{
            users:[],
            showUserModal: false,
            user_id: '',
            userRecords: []
            }
        },
        methods:{
            async fetchData(){
                const resUsers = await fetch("http://localhost:5000/admin/users");
                this.users = await resUsers.json();
            },
            async openUserModal(user_id){
                this.user_id = user_id;
                await this.fetchUserRecords();
                this.showUserModal = true;
            },
            closeUserModal(){
                this.showUserModal = false;
                this.userRecords = [];
            },
            async fetchUserRecords(){
                const resRecords = await fetch(`http://localhost:5000/records/${this.user_id}`);
                this.userRecords = await resRecords.json();
            }
        },
        mounted() {
            this.fetchData();
        }
    };
</script>