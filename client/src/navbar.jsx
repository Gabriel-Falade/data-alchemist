import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './navbar.css';

const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [isDark, setIsDark] = useState(false);

    useEffect(() => {
        document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
    }, [isDark]);

    return (
        <nav className="navbar">
        <div className="navbar-container"> 
            <div className="nav-title">Data Alchemist</div>
            
            <ul className={`nav-links ${isOpen ? 'active' : ''}`}>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/upload">Upload</Link></li>
            <li><Link to="/analytics">Analytics</Link></li>
            <li><Link to="/statistics">Statistics</Link></li>
            <li><Link to="/visualize">Visualize</Link></li>
            <li>
                <button onClick={() => setIsDark(!isDark)} className="theme-toggle">
                    {isDark ? 'LIGHT' : 'DARK'}
                </button>
            </li>
            </ul>

            <div className="nav-toggle" onClick={() => setIsOpen(!isOpen)}>
            <span className="bar"></span>
            <span className="bar"></span>
            <span className="bar"></span>
            </div>
        </div>
        </nav>
    );
};

export default Navbar;