import React, { useState, useEffect } from 'react'
import './header.css'
import Navbar from './navbar/navbar'
import headerMobileIMG from "../../assets/picture/mobile-header.png"

export default function Header() {

  const [isMobile, setIsMobile] = useState(
    window.innerWidth <= 900
  )

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

        // mobile
        <>
          <div className='mobile-header'>

            <div className="navbar-logo-mobile">
              <div className="logo-icon">
                ✽
              </div>

              <div className="logo-text">
                <span>Aura</span>
                <span>Étoile</span>
              </div>
            </div>

            <img src={headerMobileIMG} alt="" />

            <div className='mobile-hwader-content'>

              <span className='mobile-header-span'>
                مجموعه سلطنتی فرانسه و شرق
              </span>

              <h1 className='mobile-header-title'>
                عطرهای اصل و خاص
                <br />
                تجلی شکوه و اصالت
              </h1>

              <p className='mobile-header-text'>
                کشف رایحه‌های ناب و نفیس که هویت شما را به تصویر می‌کشند.
                با نوآر اسنس، امضای بویایی منحصر‌به‌فرد خود را در میان برترین برندهای
                نیش جهان بیابید.
              </p>

            </div>

            <Navbar />

          </div>
        </>

      ) : (

        // desktop
        <div>

          <Navbar />

          <div className='header-container container'>

            <div className='header-content'>

              <span>
                مجموعه سلطنتی فرانسه و شرق
              </span>

              <h1>
                عطرهای اصل و خاص
                <br />
                تجلی شکوه و اصالت
              </h1>

              <p>
                کشف رایحه‌های ناب و نفیس که هویت شما را به تصویر می‌کشند.
                با نوآر اسنس، امضای بویایی منحصر‌به‌فرد خود را در میان برترین برندهای
                نیش جهان بیابید.
              </p>

              <button className='header-button'>
                مشاهده کلکسیون
              </button>

            </div>

          </div>

        </div>

      )}
    </>
  )
}