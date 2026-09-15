import React, { Component } from 'react'
import { Routes, Route } from 'react-router-dom'

import "./App.css"
import Header from './component/header/header'
import ParrentProduct from './component/product/parrentProduct'
import Footer from './component/footer/footer'
import AboutUs from './component/aboutUs/aboutUs'
import ProductDetail from './component/productDetail/productDetail'
import Navbar from './component/header/navbar/navbar'


export default class App extends Component {
  render() {
    return (
      <> 
        <Routes>
          <Route path="/" element={<> <Header /> <ParrentProduct /> <AboutUs /> </>} />
          <Route path='/Product/:id' element={<><Navbar /> <ProductDetail /></>} />
        </Routes>
        <Footer></Footer>
      </>
    )
  }
}
