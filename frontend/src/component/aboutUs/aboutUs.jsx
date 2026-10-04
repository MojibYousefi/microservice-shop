import React from 'react'
import './aboutUs.css'
import aboutUsPicture from '../../assets/picture/header.png'

export default function AboutUs() {
    return (
        <div className='aboutUs-container'>
            <div className='aboutUs-IMG'>
                <img src={aboutUsPicture} alt="" />
            </div>

            <div className='aboutUs-content'>
                <span>داستان اصالت ما</span>
                <h2>درباره انور اسنس</h2>

                <p>
                    گالری نوآر اسنس با بیش از یک دهه تجربه در واردات مستقیم و انحصاری عطرهای نیش و سلطنتی،
                    اصالت تک‌تک محصولات خود را صد درصد تضمین می‌کند. ما معتقدیم که عطر شما،
                    امضای پنهان و بیانگر باشکوه‌ترین جنبه‌های شخصیت شماست.
                </p>

                <p>
                    در مجموعه ما،
                    از نایاب‌ترین کارهای عود و چوب تا درخشان‌ترین ترکیبات گلی و میوه‌ای جمع‌آوری شده‌اند تا برای هر ذائقه منحصربه‌فرد،
                    پاسخی درخور کمال‌گرایی ارائه دهیم.
                </p>
            </div>

        </div>
    )
}