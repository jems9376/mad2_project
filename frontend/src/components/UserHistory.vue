<template>
    <div>
        <h2>History</h2>
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
            <tbody v-if="records.length > 0">
                <tr v-for="record in records" :key="record.record_id">
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
            <tbody v-else>
                <tr>
                    <td colspan="7" style="text-align: center;">No records found</td>
                </tr> 
            </tbody>
        </table>
    </div>
</template>

<script>

    export default {
        data() {
            return {
                records: [],
                user_id: localStorage.getItem('user_id'),
            }
        },
        methods : {
            
            async fetchData() {
                const resRecords = await fetch(`http://localhost:5000/records/${this.user_id}`); // <-- important check!
                this.records = await resRecords.json();
            },
        },
        mounted() {
            this.fetchData();
        }

    }

</script>