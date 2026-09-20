import React, { useState } from 'react'
import './productDetail.css'
import ProductCart from '../product/productCart/productCart'

import productimage from "../../assets/picture/product.png"

import { Autoplay } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'

export default function ProductDetail() {

  const [products, setProducts] = useState([
    {
      id: 1,
      name: "dior svaage",
      brand: "dior",
      price: "4,500,000",
      discount: "20",
      finalPrice: "3,600,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",

      Images: [
        productimage,
        productimage,
        productimage,
      ],

      selectedImage: productimage,

      volume: "100",
      category: "مردانه"
    }
  ])

  const [relatedProduct, setRelatedProduct] = useState([
    {
      id: 1,
      perfumName: "svage elexir",
      price: "4,500,000",
      ProductImage: productimage,
      priceAfteroff: "4,000,000"
    },
    {
      id: 2,
      perfumName: "creed aventus",
      price: "6,000,000",
      ProductImage: productimage,
      priceAfteroff: "5,400,000"
    },
    {
      id: 3,
      perfumName: "blue chanel",
      price: "3,650,000",
      ProductImage: productimage,
      priceAfteroff: "800,000"
    },
    {
      id: 4,
      perfumName: "floris",
      price: "8,200,000",
      ProductImage: productimage,
      priceAfteroff: "6,500,000"
    },
    {
      id: 5,
      perfumName: "almas",
      price: "7,000,000",
      ProductImage: productimage,
      priceAfteroff: "4,000,000"
    },
  ])

  const [perfumeQuantity, setPerfumeQuantity] = useState(0)


  const onclickHandler = (image) => {
    setProducts(prevProducts => [
      {
        ...prevProducts[0],
        selectedImage: image
      }
    ])
  }


  const plusPerfumeQuantity = () => {
    setPerfumeQuantity(prevQuantity => prevQuantity + 1)
  }


  const minusPerfumeQuantity = () => {
    setPerfumeQuantity(prevQuantity =>
      prevQuantity > 1
        ? prevQuantity - 1
        : 0
    )
  }


  const product = products[0]


  return (
    <>
      <div className='product-detail'>
        <div className='first-sectiom'>
          <div className='product-galery'>
            <div className='product-main-image'>
              <img
                src={product.selectedImage}
                alt="product"
              />
            </div>
            <div className='product-thumbnails'>
              {product.Images.map((image, index) => (
                <div
                  className='product-thumbnail'
                  key={index}
                  onClick={() => onclickHandler(image)}
                >
                  <img src={image} alt="product" />
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className='product-content'>
          <h2 className='perfume-name'>
            {product.name}
          </h2>
          <p className='perfume-brand'>
            {`(${product.brand})`}
          </p>
          <p className='perfume-desc'>
            {product.descriotion}
          </p>
          <div className='price-section'>
            <p className='perfume-price'>
              {product.price}
            </p>
            <p className='perfume-final-price'>
              {product.finalPrice}
            </p>
          </div>
          <div className='buttons-section'>
            <button className='addToCart-btn'>
              افزودن به سبد خرید
            </button>
            <div>
              <button className='plusPerfumeCount' onClick={plusPerfumeQuantity}>
                +
              </button>
              <p>{perfumeQuantity}</p>
              <button className='minusPerfumeCount' onClick={minusPerfumeQuantity}>
                -
              </button>
            </div>
          </div>
        </div>


        {/* feature section */}
      </div>
      <div className='Features'>
        <div className='Feature-item'>
          <p className='big-p'>پشتیبانی 24/7</p>
          <p className='smal-p'>پاسخگویی سریع</p>
        </div>
        <div className='Feature-item'>
          <p className='big-p'>ضمانت اصالت کالا</p>
          <p className='smal-p'>با ضمانت نامه</p>
        </div>
        <div className='Feature-item'>
          <p className='big-p'>ارسال سریع</p>
          <p className='smal-p'>در سراسر کشور</p>
        </div>
        <div className='Feature-item'>
          <p className='big-p'>بازگشت کالا</p>
          <p className='smal-p'>تا 7 روز</p>
        </div>
      </div>


      <div className='moreDetail-related-section'>
        {/* more detail */}
        <div className='moreDetail'>
          <h4 className='moreDetail-title'>
            جزئیات بیشتر
          </h4>
          <div className='moreDetail-item'>
            <div className='details'>
              <p>{product.brand}</p>
              <p>برند</p>
            </div>
            <div className='details'>
              <p>{product.category}</p>
              <p>جنسیت</p>
            </div>
            <div className='details'>
              <p>{product.volume} میلی لیتر</p>
              <p>حجم</p>
            </div>
          </div>
        </div>
        {/* related product */}
        <div className='relatedProduct'>

          <Swiper
            modules={[Autoplay]}
            slidesPerView={3  }
            spaceBetween={20}
            breakpoints={{
              0: {
                slidesPerView: 2,
                spaceBetween: 10,
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
            {relatedProduct.map((product) =>
              <SwiperSlide key={product.id} >
                <ProductCart {...product} />
              </SwiperSlide>
            )}
          </Swiper>
        </div>

      </div>
    </>
  )
}