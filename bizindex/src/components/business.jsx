import React from 'react';

const Business = ({ name, category, description, image }) => {
    return (
        <div className='single'>
            <h2>{name}</h2>
            <img src={image} alt={name} />
            <p>Category: {category}</p>
            <p>Description: {description}</p>
        </div>
    );
};

export default Business;
