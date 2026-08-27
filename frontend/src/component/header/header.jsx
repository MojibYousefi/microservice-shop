import React, { Component } from 'react'
import './header.css'
import Navbar from './navbar/navbar'

export default class Header extends Component {
  render() {
    return (
      <div>
        <Navbar></Navbar>
        <div className='header-container'>
          <div className='header-content'>
            <h1>تجربه <span>لوکس ترین</span> عطر ها </h1>

            <p>شاهکار هایی از دنیای عطر سازی</p>

            <button className='header-button'>مشاهده کلکسیون </button>
          </div>
        </div>
      </div>
    )
  }
}
