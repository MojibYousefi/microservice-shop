import './bestSeelsProduct.css'
import ProductCart from '../productCart/productCart'
import productimage from "../../../assets/picture/product.png"

import React, { Component } from 'react'

import { Autoplay } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'

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
                {
                    id: 6,
                    perfumName: "test",
                    priceforBSP: "1,000,000",
                    ProductImage: productimage,
                }
            ],
            slide: 0
        }
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
                <div className='best-seal-product'>
                    <Swiper
                        modules={[Autoplay]}
                        slidesPerView={5}
                        spaceBetween={20}
                        breakpoints={{
                            0: {
                                slidesPerView: 2,
                                spaceBetween: 10
                            },
                            900: {
                                slidesPerView: 2,
                                spaceBetween: 20
                            },
                            1200: {
                                slidesPerView: 5,
                                spaceBetween: 20
                            }
                        }}
                        autoplay={{
                            delay: 2000,
                            pauseOnMouseEnter: true,
                            disableOnInteraction: false
                        }}
                    >
                        {this.state.products.map(perf =>
                            <SwiperSlide key={perf.id}>
                                <ProductCart
                                    {...perf}
                                />
                            </SwiperSlide>
                        )}

                    </Swiper>
                </div>
            </div>
        )
    }
}
