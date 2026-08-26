import React, { Component } from 'react'
import "./navbar.css"

export default class Navbar extends Component {
    render() {
        return (
            <>
                <nav className="navbar">
                    <div className="navbar-container">

    
                        <div className="navbar-logo">
                            <div className="logo-icon">
                                ✽
                            </div>

                            <div className="logo-text">
                                <span>Aura</span>
                                <span>Étoile</span>
                            </div>
                        </div>


                        
                        <div className="navbar-menu">
                            <a href="#">تماس با ما</a>
                            <a href="#">درباره ما</a>
                            <a href="#">هدیه</a>
                            <a href="#">کلکسیون عطرها</a>
                        </div>


                        
                        <div className="navbar-actions">
                            <a href="#" className="signin">
                                Sign in
                            </a>

                            <button className="start-btn">
                                شروع کنید
                            </button>
                        </div>

                    </div>
                </nav>
            </>
        )
    }
}
