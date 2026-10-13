import ParrentProduct from './component/product/parrentProduct'
import Navbar from './component/header/navbar/navbar'
import Home from './pages/home'
import ProductDetail from './component/productDetail/productDetail'



const routes = [
    {
        path: "/",
        element: <Home />,
    },
    {
        path: "/product/:id",
        element: (
            <>
                <Navbar />
                <ProductDetail />
            </>
        ),
    },
];

export default routes