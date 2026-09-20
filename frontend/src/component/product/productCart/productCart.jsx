import React from 'react'
import './productCart.css'
import { useNavigate } from 'react-router-dom'

export default function ProductCart(props) {

    const navigate = useNavigate()

    const goingProductDetail = () => {
        navigate(`/product/${props.id}`)
    }

    return (
        <div
            className='ProductCart'
            onClick={goingProductDetail}
        >

            {/* product cart image */}
            <div className='product-image'>
                <img
                    src={props.ProductImage}
                    alt={props.perfumName}
                />
            </div>


            {/* product cart name title */}
            <h3 className='perfum-title'>
                {props.perfumName}
            </h3>


            {/* perfume description */}
            <p className='perfum-discription'>
                Lorem ipsum dolor, sit amet consectetur adipisicing elit.
                Reiciendis, quia?
            </p>


            <div className='product-text'>

                {/* old price */}
                {props.priceforBSP && (
                    <p className='BSPprice'>
                        {props.priceforBSP}
                    </p>
                )}


                {/* new price */}
                {props.priceAfteroff && (
                    <div className='offerPrice'>

                        <p>
                            {props.priceAfteroff}
                        </p>

                        <del className='old-price'>
                            {props.price}
                        </del>

                    </div>
                )}

                <button>
                    افزودن به سبد خرید
                </button>

            </div>

        </div>
    )
}