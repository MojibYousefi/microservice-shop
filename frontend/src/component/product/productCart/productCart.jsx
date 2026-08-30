import React, { Component } from 'react'
import './productCart.css'

export default class ProductCart extends Component {

    render() {
        return (
            <div className='ProductCart'>

                <div className='product-image'>
                    <img src={this.props.ProductImage} alt="" />
                </div>

                {this.props.offerPercentage && (
                    <p className='offerPercentage'>{this.props.offerPercentage}</p>
                )}

                <h3 className='perfum-title'>
                    {this.props.perfumName}
                </h3>
                <div className='product-text'>

                    <del className='old-price'>
                        {this.props.price}
                    </del>
                    {this.props.priceAfteroff && (
                        <p>{this.props.priceAfteroff}</p>
                    )}

                </div>

            </div>
        )
    }
}