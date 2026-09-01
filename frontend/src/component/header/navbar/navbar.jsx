import React, { Component, useState, useEffect } from 'react'
import "./navbar.css"

export default class Navbar extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isMobile: window.innerWidth <= 900
        };
    }

    componentDidMount() {
        window.addEventListener("resize", this.handleResize);
    }

    componentWillUnmount() {
        window.removeEventListener("resize", this.handleResize);
    }

    handleResize = () => {
        this.setState({
            isMobile: window.innerWidth <= 900
        });
    };


    render() {
        return (
            <>
                {this.state.isMobile ? (
                    <div className='mobile-navbar'>
                        <div className="mobile-navbar-item">
                            <a href="">خانه</a>
                        </div>
                        <div className="mobile-navbar-item">
                            <a href="">کلکسیون</a>
                        </div>
                        <div className="mobile-navbar-item">
                            <a href="">سبد خرید</a>
                        </div>
                        <div className="mobile-navbar-item">
                            <a href="">حساب کاربری</a>
                        </div>
                        <div className="mobile-navbar-item">
                            <a href="">منو</a>
                        </div>
                    </div>) : (
                    // desktop navbar
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
                )}
            </>
        )
    }
}
