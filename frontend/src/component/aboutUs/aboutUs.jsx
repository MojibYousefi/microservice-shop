import React, { Component } from 'react'
import './aboutUs.css'

export default class AboutUs extends Component {
    render() {
        return (
            <div className='aboutUs-container'>
                <span>داستان اصالت ما</span>
                <div className='aboutUs-content'>
                    <h2>درباره انور اسنس</h2>
                    <p>گالری نوآر اسنس با بیش از یک دهه تجربه در واردات مستقیم و انحصاری عطرهای نیش و سلطنتی،
                        اصالت تک‌تک محصولات خود را صد درصد تضمین می‌کند. ما معتقدیم که عطر شما،
                        امضای پنهان و بیانگر باشکوه‌ترین جنبه‌های شخصیت شماست.</p>
                    <p>در مجموعه ما،
                        از نایاب‌ترین کارهای عود و چوب تا درخشان‌ترین ترکیبات گلی و میوه‌ای جمع‌آوری شده‌اند تا برای هر ذائقه منحصربه‌فرد،
                        پاسخی درخور کمال‌گرایی ارائه دهیم.</p>
                </div>

            </div>
        )
    }
}
