import React from 'react'
import OfferProduct from './offerProduct/offerProduct'
import BestSeelsProduct from "./bestSeelsProduct/bestSeelsProduct"

export default function ParrentProduct() {
    return (
        <div>
            <BestSeelsProduct />
            <OfferProduct />
        </div>
    )
}