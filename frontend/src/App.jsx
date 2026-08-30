import React, { Component } from 'react'
import "./App.css"
import Header from './component/header/header'
import ParrentProduct from './component/product/parrentProduct'



export default class App extends Component {
  render() {
    return (
      <div>
        <Header></Header>
        <ParrentProduct></ParrentProduct>
      </div>
    )
  }
}
