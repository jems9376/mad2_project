<template>
    <div class="dashboard-content">
        <h2>Parking Lots</h2>

        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="message" class="message">{{ message }}</div>

        <div class="lots-container">
            <div
                v-for="lot in parkingLots"
                :key="lot.id"
                class="lot-card"
            >
                <div class="lot-header">
                <h3>{{ lot.name }}</h3>
                <p>
                    {{ lot.address }} || Rs.{{ lot.price }}/hr
                </p>
                <div class="lot-actions">
                    <span class="edit" @click="openEditModal(lot)">Edit</span>
                    <span disabled>|</span>
                    <span class="delete" @click="deleteLot(lot.id)">Delete</span>
                </div>
                <div class="occupancy">
                    (Available: {{ lot.a_spots }}/{{ lot.spots }})
                </div>
                </div>
                <div class="spots-grid">
                <div v-for="spot in lot.spot_details" 
                    :key="spot.spot_id" >
                    <button @click="openSpotModal(spot)" :class="['spot', 
                    spot.status === 'O' ? 'reserved' : 'available']">
                        {{ spot.status }}
                    </button>
                </div>
                </div>
            </div>
        </div>
        <div class="add-lot-button" @click="openCreateModal">
        + Add Lot 
        </div>

        <!-- Create Modal -->
        <div v-if="showCreateModal" class="modal">
            <div class="modal-content">
                <h3>Create New Parking Lot</h3>
                <form @submit.prevent="createParkingLot">
                <input v-model="newLot.name" placeholder="Lot Name" required />
                <input v-model="newLot.address" placeholder="Address" required />
                <input v-model="newLot.pin_code" type="text" placeholder="Pin Code" required />
                <input v-model="newLot.price" type="number" placeholder="Price" required />
                <input v-model="newLot.spots" type="number" placeholder="Number of Spots" required />
                <div class="modal-buttons">
                    <button type="submit">Create</button>
                    <button type="button" @click="closeCreateModal" class="close-button">Cancel</button>
                </div>
                </form>
            </div>
        </div>

        <!-- Edit Modal -->
        <div v-if="showEditModal" class="modal">
            <div class="modal-content">
                <h3>Edit Parking Lot</h3>
                <form @submit.prevent="editLot">
                <label for="name">Name: </label>
                <input v-model="editedLot.name" placeholder="Lot Name" required />
                <label for="address">Address: </label>
                <input v-model="editedLot.address" placeholder="Address" required />
                <label for="pin_code">Pin Code: </label>
                <input v-model="editedLot.pin_code" type="text" placeholder="Pin Code" required />
                <label for="price">Price: </label>
                <input v-model="editedLot.price" type="number" placeholder="Price" required />
                <label for="spots">Spots: </label>
                <input v-model="editedLot.spots" type="number" placeholder="Number of Spots" required />
                <div class="modal-buttons">
                    <button type="submit">Update</button>
                    <button type="button" @click="closeEditModal" class="close-button">Cancel</button>
                </div>
                </form>
            </div>
        </div>

        <!-- Spot Modal -->
        <div v-if="showSpotModal" class="modal">
            <div class="modal-content">
                <h3>Parking Spot</h3>
                <form @submit.prevent="deleteSpot">
                <label for="spot_id">Spot Id: </label>
                <input v-model="spot.spot_id" placeholder="Spot ID" disabled />
                <br>
                <label for="spot_status">Spot Status: </label>
                <input v-if="spot.status==='O'" value="Occupied" placeholder="Spot Status" disabled />
                <input v-else value="Available" disabled>
                <div v-if="spot.status === 'O'" class="modal-buttons">
                    <button v-if="spot.status === 'O'" @click="openSpotDetailModal(spot.spot_id)">View</button>
                    <button type="button" @click="closeSpotModal" class="close-button">Close</button>
                </div>
                <div v-else class="modal-buttons">
                    <button v-if="spot.status === 'A'" type="submit" class="close-button">Delete</button>
                    <button type="button" @click="closeSpotModal" class="cancel-button">Close</button>
                </div>
                </form>
            </div>
        </div>

        <!-- Spot Details Modal -->
        <div v-if="showSpotDetailModal" class="modal">
            <div class="modal-content">
                <h3 style="margin-top: 0px;">Occupied Parking Spot Details</h3>
                <form>
                    <label for="spot_id">Spot ID: </label>
                    <input v-model="spotDetails.spot_id" disabled>
                    <br>
                    <label for="spot_id">Customer ID: </label>
                    <input v-model="spotDetails.customer_id" disabled>
                    <br>
                    <label for="spot_id">Vehicle Number: </label>
                    <input v-model="spotDetails.vehicle_number" disabled>
                    <br>
                    <label for="spot_id">Time of Parking: </label>
                    <input v-model="spotDetails.parking_timestamp" disabled>
                    <br>
                    <label for="spot_id">Est. Parking cost: </label>
                    <input v-model="spotDetails.parking_cost" disabled>
                    <div class="modal-buttons" style="display: flex; flex-direction: column;align-items:center ;margin-top: 0px;">
                        <button @click="closeSpotDetailModal">Close</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                newLot: {
                    name: '',
                    address: '',
                    pin_code: '',
                    price: '',
                    spots: ''
                    },
                editedLot: {
                    id: '',
                    name: '',
                    address: '',
                    pin_code: '',
                    price: '',
                    spots: ''
                    },
                spot: {
                    spot_id: '',
                    status: '',
                    lot_id: ''
                    },
                parkingLots: [],
                parkingSpots: [],
                spotDetails:[],
                error: '',
                message: '',
                showCreateModal: false,
                showEditModal: false,
                showSpotModal: false,
                showSpotDetailModal: false
            };
        },
        methods: {
        async fetchData() {
            const lot = await fetch("http://localhost:5000/lot");
            const lotsData = await lot.json();
            this.parkingLots = await lotsData.map(lot => ({...lot,
            spot_details: this.generateSpots(lot.id,lot.spots,lot.o_spots_ids,lot.spot_ids)
            }));

        },
        generateSpots(id,total, occupiedIds,Ids) {
            const spots = [];
            for (let i = 0; i < total; i++) {
            if (occupiedIds.includes(Ids[i])) {
                spots.push({ spot_id: Ids[i], status: 'O', lot_id: id });
            } else {
                spots.push({ spot_id: Ids[i], status: 'A', lot_id: id });
            }
            }
            return spots;
        },
        getOccupiedCount(lot) {
            return lot.spot_details.filter(spot => spot.status === 'O').length;
        },
        openCreateModal() {
            this.showCreateModal = true;
        },
        closeCreateModal() {
            this.showCreateModal = false;
            this.resetNewLot();
        },
        openEditModal(lot) {
            this.editedLot = { ...lot }; // pre-fill
            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
            this.resetEditedLot();
        },
        openSpotModal(spot) {
            this.spot = { ...spot };
            this.showSpotModal = true;
        },
        closeSpotModal() {
            this.showSpotModal = false;
            this.resetSpot();
        },
        openSpotDetailModal(spot_id){
            this.closeSpotModal();
            this.getSpotDetails(spot_id);
            this.showSpotDetailModal = true;
        },
        closeSpotDetailModal(){
            this.showSpotDetailModal = false;
            this.spotDetails = []
        },
        async getSpotDetails(spot_id){
            const response = await fetch(`http://localhost:5000/spot/detail/${spot_id}`);
            this.spotDetails = await response.json();
        },
        async createParkingLot() {
            const response = await fetch("http://localhost:5000/lot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.newLot)
            });

            if (response.ok) {
            this.message = "Parking lot created";
            } else {
            const err = await response.json();
            this.error = err.message;
            }
            this.closeCreateModal();
            this.fetchData();
        },
        async deleteLot(id) {
            const response = await fetch(`http://localhost:5000/admin/lot/${id}`, { method: "DELETE" });
            if (!response.ok) {
            const err = await response.json();
            this.error = err.message;
            }
            await this.fetchData();
        },
        async deleteSpot() {
            await fetch(`http://localhost:5000/admin/spot/${this.spot.spot_id}`, { method: "DELETE" });
            this.closeSpotModal();
            await this.fetchData();
        },
        async editLot() {
            const response = await fetch(`http://localhost:5000/admin/lot/${this.editedLot.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.editedLot)
            });

            if (response.ok) {
            this.message = "Parking lot updated";
            } else {
            const err = await response.json();
            this.error = err.message;
            }
            this.closeEditModal();
            this.fetchData();
        },
        resetNewLot() {
            this.newLot = { name: '', address: '', pin_code: '', price: '', spots: '' };
        },
        resetEditedLot() {
            this.editedLot = { id: '', name: '', address: '', pin_code: '', price: '', spots: '' };
        },
        resetSpot() {
            this.spot = { spot_id: '', spot_status: '', lot_id: '' };
        },

        },
        mounted() {
        this.fetchData();
        }
    };
</script>

