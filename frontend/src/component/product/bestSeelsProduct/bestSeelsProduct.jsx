import React, { Component } from 'react'
import ProductCart from '../productCart/productCart'
import './bestSeelsProduct.css'
import productimage from "../../../assets/picture/product.png"

export default class BestSeelsProduct extends Component {
    constructor(props) {
        super(props)
        this.state = {
            products: [
                {
                    id: 1,
                    perfumName: "svage elexir",
                    priceforBSP: "4,500,000",
                    ProductImage: productimage,
                },
                {
                    id: 2,
                    perfumName: "creed aventus",
                    priceforBSP: "6,000,000",
                    ProductImage: productimage,
                },
                {
                    id: 3,
                    perfumName: "blue chanel",
                    priceforBSP: "3,650,000",
                    ProductImage: productimage,
                },
                {
                    id: 4,
                    perfumName: "floris",
                    priceforBSP: "8,200,000",
                    ProductImage: productimage,
                },
                {
                    id: 5,
                    perfumName: "almas",
                    priceforBSP: "7,000,000",
                    ProductImage: productimage,
                },
            ],
            slide: 0
        }
    }
    nextSlide = () => {
        this.setState(prevState => ({
            slide: Math.min(
                prevState.slide + 1,
                this.state.products.length - 4
            )
        }))
    }
    prevSlide = () => {
        this.setState(prevState => ({
            slide: Math.max(prevState.slide - 1, 0)
        }))
    }
    render() {
        return (
            <div>
                <div className='best-seal-title'>

                    <p className='whach-all'><a href="">← مشاهده همه</a></p>

                    <div className='right-text'>
                        <span>محبوب ترین رایحه ها</span>
                        <h2>پرفروش ترین محصولات</h2>
                    </div>
                </div>
                <div className='products-slider'>
                    <button onClick={this.prevSlide} className='slider-btn prev'>‹</button>
                    <div className='products-viewport'>
                        <div
                            className='products-track'
                            style={{
                                transform: `translateX(-${this.state.slide * 330}px)`
                            }}
                        >
                            {this.state.products.map(perf =>
                                <ProductCart
                                    key={perf.id}
                                    {...perf}
                                />
                            )}
                        </div>
                    </div>
                    <button className='slider-btn next' onClick={this.nextSlide}>›</button>
                </div>
            </div>
        )
    }
}
