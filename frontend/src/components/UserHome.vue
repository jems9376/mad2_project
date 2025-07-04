<template>
    <h2>Available Parking Lots</h2>

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
            <div class="occupancy">
                (Available: {{ lot.a_spots }}/{{ lot.spots }})
            </div>
            </div>
            <div class="spots-grid">
            <div v-for="spot in lot.spot_details" 
                :key="spot.spot_id" >
                <button v-if="spot.status === 'R'" @click="openReleaseModal(spot.spot_id)" :class="['spot','reserved' ]">
                    O
                </button>
                <button v-else @click="openSpotModal(spot.spot_id)" :class="['spot',
                    spot.status === 'O' ? 'occupied'  : 'available']" 
                    :disabled="spot.status === 'O'">
                    {{ spot.status }}
                </button>
            </div>
            </div>
        </div>
    </div>



    <div v-if="showBookingModal" class="modal">
        <div class="modal-content">
            <h3>Book Spot</h3>

            <form @submit.prevent="bookSpot(spotDetails.spot_id)">
                <label for="spot_id">Spot Id: </label>
                <input v-model="spotDetails.spot_id" placeholder="Spot ID" disabled />
    
                <label for="parking_price">Parking Price: </label>
                <input v-model="spotDetails.parking_cost" placeholder="Parking Price" disabled />
    
                <label for="parking_tmestamp">Time of Parking: </label>
                <input v-model="spotDetails.parking_timestamp" placeholder="Time of Parking" disabled />

                <label for="vehicle_number">Vehicle Number: </label>
                <input v-model="spotDetails.vehicle_number" placeholder="Vehicle Number" required/>
                <div class="modal-buttons">
                    <button type="submit" class="reserved">Book</button>
                    <button type="button" @click="closeBookingModal" class="close-button">Close</button>
                </div>
            </form>
        </div>
    </div>

    <div v-if="showReleaseModal" class="modal">
        <div class="modal-content">
            <h3>Release Spot</h3>
            <form @submit.prevent="releaseSpot(spotDetails.spot_id)">
                <label for="spot_id">Spot Id: </label>
                <input v-model="spotDetails.spot_id" placeholder="Spot ID" disabled />

                <label for="parking_tmestamp">Time of Parking: </label>
                <input v-model="spotDetails.parking_timestamp" placeholder="Time of Parking" disabled />

                <label for="leaving_timestamp">Time of Leaving: </label>
                <input v-model="spotDetails.leaving_timestamp" placeholder="Time of Leaving" disabled />

                <label for="parking_cost">Parking Cost: </label>
                <input v-model="spotDetails.parking_cost" placeholder="Parking Cost" disabled />

                <label for="vehicle_number">Vehicle Number: </label>
                <input v-model="spotDetails.vehicle_number" placeholder="Vehicle Number" disabled />
                <div class="modal-buttons">
                    <button type="submit" class="reserved">Release</button>
                    <button type="button" @click="closeReleaseModal" class="close-button">Close</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
    export default {
    data() {
        return {
        parkingLots: [],
        bookings: [],
        spotDetails: {
            spot_id: '',
            lot_id: '',
            vehicle_number: '',
            parking_timestamp: '',
            leaving_timestamp: '',
            parking_cost: ''
        },
        spotIds: [],
        currSpotIds: [],
        spot: {
            spot_id: '',
            lot_id: '',
            vehicle_number: '',
        },
        vehicle_number: '',
        error: '',
        message: '',
        user_id: localStorage.getItem('user_id'),
        selectedLot: null,
        selectedBooking: null,
        showBookingModal: false,
        showReleaseModal: false,
        };
    },
    methods: {
        async fetchData() {
            try {
                const lot = await fetch("http://localhost:5000/lot");
                const lotsData = await lot.json() || [];

                const records = await fetch(`http://localhost:5000/records/${this.user_id}`);
                
                const userResponse = await fetch(`http://localhost:5000/user/${this.user_id}`);
                const userData = await userResponse.json();
                this.vehicle_number = userData.vehicle_number;

                let bookingsData = [];
                if (records.ok) {   // <-- important check!
                    bookingsData = await records.json();
                } else {
                    bookingsData = []; // If not OK, no bookings
                }

                this.currSpotIds = [];
                this.bookings = bookingsData;

                for (let i = 0; i < this.bookings.length; i++) {
                this.spotIds.push(this.bookings[i].spot_id);
                if (this.bookings[i].spot_status === 'O') {
                    this.currSpotIds.push(this.bookings[i].spot_id);
                }
                }

                this.parkingLots = lotsData.map(lot => ({
                ...lot,
                spot_details: this.generateSpots(lot.id, lot.spots, lot.o_spots_ids, lot.spot_ids)
                }));

            } catch (err) {
                console.error(err);
                this.error = err.message;
                this.message = '';
            }
        },
        generateSpots(id,total, occupiedIds,Ids) {
            const spots = [];
            for (let i = 0; i < total; i++) {
                const x = Ids[i];
                if (this.currSpotIds.includes(x)) {
                    spots.push({ spot_id: x, status: 'R', lot_id: id });
                } else if (occupiedIds.includes(x)) {
                    spots.push({ spot_id: x, status: 'O', lot_id: id });
                } else {
                    spots.push({ spot_id: x, status: 'A', lot_id: id });
                }
            }
            return spots;
        },
        async getSpotDetails(spot_id){
            
            const response = await fetch(`http://localhost:5000/spot/detail/${spot_id}`);
            const data = await response.json();

            this.spotDetails['spot_id'] = data['spot_id'];
            this.spotDetails['lot_id'] = data['lot_id'];
            if (data['vehicle_number'] === null) {
                this.spotDetails['vehicle_number'] = this.vehicle_number 
            }else{ 
                this.spotDetails['vehicle_number'] = data['vehicle_number']
            }
            this.spotDetails['parking_timestamp'] = data['parking_timestamp'];
            this.spotDetails['leaving_timestamp'] = data['leaving_timestamp'];
            this.spotDetails['parking_cost'] = data['parking_cost'];
        },
        async logout(){
            try{
                await fetch("http://localhost:5000/logout");
            } catch (error){
                console.warn('Logout request failed:', error.response?.data || error.message);
            }
            localStorage.removeItem('user_id');
            localStorage.removeItem('role');
            this.$router.push('/login')
        },
        editProfile() {
            this.$router.push('/edit_profile'); // Assume you have edit profile page
        },
        async openSpotModal(spot_id) {
            await this.getSpotDetails(spot_id)
            this.showBookingModal = true;
        },
        closeBookingModal() {
            this.showBookingModal = false;
            this.resetSpotDetails();
        },
        resetSpotDetails() {
            this.spotDetails = {
                spot_id: '',
                lot_id: '',
                vehicle_number: '',
                parking_timestamp: '',
                leaving_timestamp: '',
                parking_cost: ''
            };
            this.spot = { spot_id: '', spot_status: '', lot_id: '', vehicle_number: '' };
        },
        async openReleaseModal(spot_id) {
            await this.getSpotDetails(spot_id);
            this.showReleaseModal = true;
        },
        closeReleaseModal() {
            this.showReleaseModal = false;
            this.resetSpotDetails();
        },
        async bookSpot(spot_id) {

            const response = await fetch(`http://localhost:5000/reserve/${this.user_id}/${spot_id}`, 
            { method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify(this.spotDetails) });

            await this.fetchData();
            if (!response.ok) {
                const err = await response.json();
                this.error = err.message;
            }else{
                this.message = "Spot reserved!";
            }
            this.showBookingModal = false;
        },
        async releaseSpot(spot_id) {
            await fetch(`http://localhost:5000/release/${this.user_id}/${spot_id}`, { method: "POST" });
            await this.fetchData();
            this.showReleaseModal = false;
            this.message = "Spot released!";

        },
    },
    mounted() {
        this.fetchData();
    }
    };
</script>