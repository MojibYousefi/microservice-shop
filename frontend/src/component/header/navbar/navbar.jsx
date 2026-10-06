import React, { useState, useEffect } from 'react'
import "./navbar.css"
import { NavLink } from 'react-router-dom'
import { IoHomeOutline } from "react-icons/io5"
import { IoSearch } from "react-icons/io5"
import { GiDelicatePerfume } from "react-icons/gi"
import { MdAccountCircle } from "react-icons/md"


export default function Navbar() {

    const [isSearching, setIsSearching] = useState(false)

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

                <div className="mobile-navbar">

                    {/* Mobile Navbar */}
                    <div
                        className={`mobile-navbar-2 ${isSearching ? "hide" : ""
                            }`}
                    >

                        <NavLink
                            className="mobile-navbar-item"
                            to="/"
                        >
                            <IoHomeOutline className="mobile-navbar-icon" />
                            خانه
                        </NavLink>


                        <NavLink
                            className="mobile-navbar-item"
                            to="/"
                            onClick={(e) => {
                                e.preventDefault()
                                setIsSearching(true)
                            }}
                        >
                            <IoSearch className="mobile-navbar-icon" />
                            جستجو
                        </NavLink>


                        <NavLink className="mobile-navbar-item">
                            <GiDelicatePerfume className="mobile-navbar-icon" />
                            کلکسیون
                        </NavLink>


                        <NavLink className="mobile-navbar-item">
                            <MdAccountCircle className="mobile-navbar-icon" />
                            پنل کاربری
                        </NavLink>

                    </div>


                    {/* Search Navbar */}
                    <div
                        className={`navbar-after-click ${isSearching ? "show" : ""}`}
                    >
                        <IoSearch className="mobile-navbar-icon" />

                        <input
                            type="text"
                            placeholder=" جستجو کنید ..."
                            className="input-search"
                        />
                    </div>

                </div>

            ) : (

                // Desktop Navbar
                <div className="navbar-container">

                    <div className="navbar-actions">
                        <NavLink className="login-btn"> ورود | عضویت</NavLink>
                    </div>


                    <div className="navbar-menu">

                        <a
                            href="#"
                            className="nav-link"
                        >
                            تماس با ما
                        </a>


                        <a
                            href="/#about-us"
                            className="nav-link"
                        >
                            درباره ما
                        </a>


                        <a
                            href="#"
                            className="nav-link"
                        >
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