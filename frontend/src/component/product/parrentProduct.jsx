import React from 'react'
import OfferProduct from './offerProduct/offerProduct'
import BestSeelsProduct from "./bestSeelsProduct/bestSeelsProduct"
import Banner from '../banner/banner'

export default function ParrentProduct() {
    return (
        <div>
            <BestSeelsProduct />
            <Banner />
            <OfferProduct />
        </div>
    )
}