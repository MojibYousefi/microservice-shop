import React, { Component } from 'react'
import './footer.css'

export default class Footer extends Component {
    render() {
        return (
            <>
                <div className='footer'>
                    <div className='contact'>
                        <h3 className='footer-title'>تماس با ما</h3>
                        <p className='footer-link'>ادرس : تهران خیابان فرشته مرکز تجاری پالادیوم طبقه اول</p>
                        <p className='footer-link'> تلفن : ۰۲۱-۲۲۰۰۳۳۰۰</p>
                        <a className='footer-link' href="mojib0646yousefi@gmail.com"> info@noiressence.ir : ایمیل</a>
                    </div>
                    <div className='Accessibility'>
                        <h3 className='footer-title'>لینک های سریع</h3>
                        <a className='footer-link' href="">پرسش هاس متداول</a>
                        <a className='footer-link' href="">شرایط ارسال و بازگشت</a>
                        <a className='footer-link' href="">درباره ما</a>
                        <a className='footer-link' href="">بلاگ عطر</a>
                    </div>
                    <div className='footer-main-title'>
                        <h4>نوار اسونس</h4>
                        <p>عرضه‌کننده لوکس‌ترین و بااصالت‌ترین عطرهای جهان از معتبرترین عطرسازان بین‌المللی.</p>
                    </div>
                </div>
                <div className='privecy'>
                    <p>NOIR ESSENCE © 2026. All Rights Reserved</p>
                    <p>تمامی حقوق مادی و معنوی متعلق به گالری نوآر اسنس می‌باشد</p>
                </div>
            </>
        )
    }
}
