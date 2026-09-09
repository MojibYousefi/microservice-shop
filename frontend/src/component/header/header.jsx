import React, { Component } from 'react'
import './header.css'
import Navbar from './navbar/navbar'

export default class Header extends Component {
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
              <div className='mobile-header-image'></div>
              <Navbar></Navbar>
            </div>
          </>
        ) : (

          <div>
            <Navbar></Navbar>
            <div className='header-container container'>
              <div className='header-content'>

                <span>مجموعه سلطنتی فرانسه و شرق</span>
                
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
                <button className='header-button'>مشاهده کلکسیون </button>
              </div>
            </div>
          </div>

        )}
      </>
    )
  }
}
