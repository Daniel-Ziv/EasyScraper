import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="navbar">
            <Link to="/">Home</Link>
            <Link to="/about">About</Link>
        </nav>
    );
};

export default Navbar;

// simple navbar, add links to other pages if you want
// add an icon to the top left, makes it look better