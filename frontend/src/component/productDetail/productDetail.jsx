import React, { Component } from 'react'
import './productDetail.css'

import productimage from "../../assets/picture/product.png"

export default class ProductDetail extends Component {

  constructor(props) {
    super(props)

    this.state = {
      products: [
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

          volume: "100ml",
          category: "مردانه"
        }
      ],
      perfumeQuantity: 0,
    }
  }

  onclickHandler = (image) => {
    this.setState({
      products: [
        {
          ...this.state.products[0],
          selectedImage: image
        }
      ]
    })
  }

  plusPerfumeQuantity = () => {
    this.setState(prevState => ({
      perfumeQuantity: prevState.perfumeQuantity + 1
    }))
  }

  minusPerfumeQuantity = () => {
    this.setState(prevState => ({
      perfumeQuantity: prevState.perfumeQuantity > 1 ?
        prevState.perfumeQuantity - 1 : 0
    }))
  }

  render() {

    const product = this.state.products[0]

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
                  <div className='product-thumbnail'
                    key={index}
                    onClick={() => this.onclickHandler(image)}
                  >
                    <img src={image} alt="product" />
                  </div>

                ))}

              </div>

            </div>

          </div>
          <div className='product-content'>
            <h2 className='perfume-name'>{product.name}</h2>
            <p className='perfume-brand'>{`(${product.brand})`}</p>
            <p className='perfume-desc'>{product.descriotion}</p>
            <div className='price-section'>
              <p className='perfume-price'>{product.price}</p>
              <p className='perfume-final-price'>{product.finalPrice}</p>
            </div>
            <div className='buttons-section'>
              <button className='addToCart-btn'>افزودن به سبد خرید</button>
              <div>
                <button className='plusPerfumeCount' onClick={this.plusPerfumeQuantity}>+</button>
                <p>{this.state.perfumeQuantity}</p>
                <button className='minusPerfumeCount' onClick={this.minusPerfumeQuantity}>-</button>
              </div>

            </div>
          </div>
        </div>
        <div className='Features'>
          <div className='Feature-item'>
            <p className='big-p'>  پشتیبانی 24/7 </p>
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
      </>
    )
  }
}