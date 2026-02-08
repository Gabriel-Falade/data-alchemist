import React from 'react';
import './hero.css';

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-container">
        <p className="hero-eyebrow">ESTABLISHED 2026</p>
        <h1 className="hero-title">
          Turning Dark Data into <span className="accent">Digital Gold</span>
        </h1>
        <p className="hero-subtitle">
          Advanced analytics and visualization for the modern web. 
          Built with precision, powered by alchemy.
        </p>
        <div className="hero-btns">
          <button className="btn-primary">Start Analyzing</button>
          <button className="btn-secondary">View Current Stats</button>
        </div>
      </div>
    </section>
  );
};

export default Hero;