import React, { Component } from 'react'
import "./App.css"
import Header from './component/header/header'
import ParrentProduct from './component/product/parrentProduct'
import Footer from './component/footer/footer'
import AboutUs from './component/aboutUs/aboutUs'



export default class App extends Component {
  render() {
    return (
      <div>
        <Header></Header>
        <ParrentProduct></ParrentProduct>
        <AboutUs></AboutUs>
        <Footer></Footer>
      </div>
    )
  }
}
