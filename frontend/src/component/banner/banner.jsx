import React from 'react'
import './banner.css'
import { Link } from 'react-router-dom'
import testpicture from '../../assets/picture/header.png'
function Banner() {
  return (
    <>
    <Link className='banner-picture'>
        <img src={testpicture} alt="" />   
    </Link>
    </>
  )
}

export default Banner