import React, { useState } from 'react'
import './productDetail.css'
import ProductCart from '../product/productCart/productCart'

import productimage from "../../assets/picture/product.png"

import { Autoplay } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'

import { useParams } from 'react-router-dom'


export default function ProductDetail() {

  const { id } = useParams()
  const [isAddedToCart, setIsAddedToCart] = useState(false);

  console.log(id);



  const products = [
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

      volume: "100",
      category: "مردانه"
    },

    {
      id: 2,
      name: "creed aventus",
      brand: "creed",
      price: "6,000,000",
      discount: "10",
      finalPrice: "5,400,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",

      Images: [
        productimage,
        productimage,
        productimage,
      ],

      volume: "100",
      category: "مردانه"
    },

    {
      id: 3,
      name: "blue chanel",
      brand: "chanel",
      price: "3,650,000",
      discount: "20",
      finalPrice: "2,920,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",

      Images: [
        productimage,
        productimage,
        productimage,
      ],

      volume: "100",
      category: "مردانه"
    },

    {
      id: 4,
      name: "floris",
      brand: "floris",
      price: "8,200,000",
      discount: "20",
      finalPrice: "6,500,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",

      Images: [
        productimage,
        productimage,
        productimage,
      ],

      volume: "100",
      category: "مردانه"
    },

    {
      id: 5,
      name: "almas",
      brand: "almas",
      price: "7,000,000",
      discount: "20",
      finalPrice: "4,000,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",

      Images: [
        productimage,
        productimage,
        productimage,
      ],

      volume: "100",
      category: "مردانه"
    }
  ]


  const product = products.find(
    product => product.id === Number(id)
  )


  // تغییر 4:
  // selectedImage دیگر داخل خود product نیست
  const [selectedImage, setSelectedImage] = useState(
    product?.Images[0]
  )


  const [perfumeQuantity, setPerfumeQuantity] = useState(1)


  const onclickHandler = (image) => {
    setSelectedImage(image)
  }


  const plusPerfumeQuantity = () => {
    setPerfumeQuantity(prevQuantity => prevQuantity + 1)
  }


  const minusPerfumeQuantity = () => {
    setPerfumeQuantity(prevQuantity =>
      prevQuantity > 1
        ? prevQuantity - 1
        : 1
    )
  }


  // اگر id محصول وجود نداشت
  if (!product) {
    return <h2>این محصول کیری پیدا نشد</h2>
  }


  return (
    <>
      <div className='product-detail'>

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
          <div className={`buttons-section ${isAddedToCart ? 'added' : ''}`}>

            <div className="quantity-control">

              <button
                className="minusPerfumeCount"
                onClick={minusPerfumeQuantity}
              >
                -
              </button>

              <p>{perfumeQuantity}</p>

              <button
                className="plusPerfumeCount"
                onClick={plusPerfumeQuantity}
              >
                +
              </button>

            </div>

            <button
              className="addToCart-btn"
              onClick={() => setIsAddedToCart(true)}
            >
              <span className="add-text">
                افزودن به سبد خرید
              </span>

              <span className="check-icon">
                ✓
              </span>
            </button>

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

        </div>



        <div className='product-galery'>



          <div className='product-thumbnails'>

            {product.Images.map((image, index) => (
              <div
                className='product-thumbnail'
                key={index}
                onClick={() => onclickHandler(image)}
              >
                <img
                  src={image}
                  alt={product.name}
                />
              </div>
            ))}

          </div>
          <div className='product-main-image'>
            <img
              src={selectedImage}
              alt={product.name}
            />
          </div>


        </div>

      </div>


      {/* Features */}

      {/* <div className='Features'>

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

      </div> */}

      <div className='moreDetail-related-title'>
        <h2 className='head-title'>محصولات مرتبط</h2>
        <p>عطر هایی با توجه به سلیقه شما</p>
      </div>
      <div className='moreDetail-related-section'>




        {/* related product */}

        <div className='relatedProduct'>

          <Swiper
            modules={[Autoplay]}
            slidesPerView={3}
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
                slidesPerView: 4,
                spaceBetween: 20
              }
            }}

            autoplay={{
              delay: 2000,
              pauseOnMouseEnter: true,
              disableOnInteraction: false
            }}
          >

            {products.map((product) => (

              <SwiperSlide key={product.id}>

                <ProductCart
                  id={product.id}
                  perfumName={product.name}
                  ProductImage={product.Images[0]}
                  price={product.price}
                  priceAfteroff={product.finalPrice}
                />

              </SwiperSlide>

            ))}

          </Swiper>

        </div>

      </div>

    </>
  )
}