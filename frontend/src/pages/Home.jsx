import Header from "../component/header/header";
import ParrentProduct from "../component/product/parrentProduct";
import AboutUs from "../component/aboutUs/aboutUs";
import React from 'react'



export default function Home() {
    return (
        <>
            <Header />
            <ParrentProduct />

            <section id="about-us">
                <AboutUs />
            </section>
        </>
    )
}
