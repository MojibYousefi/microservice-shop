import React, { Component } from 'react'
import OfferProduct from './offerProduct/offerProduct'
import BestSeelsProduct from "./bestSeelsProduct/bestSeelsProduct"

export default class ParrentProduct extends Component {
  render() {
    return (
      <div>
        <OfferProduct></OfferProduct>
        <BestSeelsProduct></BestSeelsProduct>
      </div>
    )
  }
}
