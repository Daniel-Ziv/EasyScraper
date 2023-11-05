import axios from "axios";

// you can add a default url to your server here, then create routes
const rootUrl = 'http://localhost:3000/data.json';

export function getAllBusinesses() {
    return axios({
        method: 'get',
        url: rootUrl,
        headers: { 'Content-Type': 'application/json' },
    })
        .then(function (response) {
            return response.data.businesses;
        })
        .catch(function (error) {
            console.error('Error fetching data:', error);
        });
}

// edit this api to your server later
// im fetching from a default json file i created to present fake data