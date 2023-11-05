import React, {useEffect, useState} from 'react';
import {getAllBusinesses} from '../api/api';
import Business from './business';

const BusinessIndex = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        getAllBusinesses()
            .then((fetchedData) => {
                console.log(fetchedData);
                setData(fetchedData);
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div>
            <h1>List of local businesses</h1>
            <div className="business-container">
                {data.length > 0 ? (
                    data.map((business) => (
                        <Business
                            key={business.id}
                            name={business.name}
                            category={business.category}
                            description={business.description}
                            image={business.image}
                        />
                    ))
                ) : (
                    <p>Loading data...</p>
                )}
            </div>
        </div>
    );
};

export default BusinessIndex;
