import React, { useState, useEffect } from 'react'
import "./navbar.css"
import { NavLink } from 'react-router-dom'

export default function Navbar() {

    const [isMobile, setIsMobile] = useState(window.innerWidth <= 900)

    useEffect(() => {

        const handleResize = () => {
            setIsMobile(window.innerWidth <= 900)
        }

        window.addEventListener("resize", handleResize)

        return () => {
            window.removeEventListener("resize", handleResize)
        }

    }, [])

    return (
        <>
            {isMobile ? (
                <div className='mobile-navbar'>
                    <div className='mobile-navbar-2'>

                        <div className="mobile-navbar-item">
                            <a href="">جستجو</a>
                        </div>

                        <div className="mobile-navbar-item">
                            <a href="">کلکسیون</a>
                        </div>

                        <div className="mobile-navbar-item">
                            <a href="">خانه</a>
                        </div>

                        <div className="mobile-navbar-item">
                            <a href="">حساب کاربری</a>
                        </div>

                        <div className="mobile-navbar-item">
                            <a href="">سبد خرید</a>
                        </div>

                    </div>
                </div>

            ) : (

                // desktop navbar
                <div className="navbar-container">

                    <div className="navbar-actions">

                        <button className="start-btn">
                            شروع کنید
                        </button>

                        <a href="#" className="signin">
                            Sign in
                        </a>

                    </div>


                    <div className="navbar-menu">

                        <a href='#' className='nav-link'>
                            تماس با ما
                        </a>

                        <a href='/#about-us' className='nav-link'>
                            درباره ما
                        </a>

                        <a href='#' className='nav-link'>
                            هدیه
                        </a>

                        <NavLink
                            to="/product"
                            className={({ isActive }) =>
                                isActive
                                    ? "nav-link active"
                                    : "nav-link"
                            }
                        >
                            کلکسیون عطر ها
                        </NavLink>

                    </div>


                    <div className="navbar-logo">

                        <div className="logo-icon">
                            ✽
                        </div>

                        <div className="logo-text">
                            <span>Aura</span>
                            <span>Étoile</span>
                        </div>

                    </div>

                </div>
            )}
        </>
    )
}