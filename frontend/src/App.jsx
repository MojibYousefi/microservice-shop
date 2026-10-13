import React from 'react'
import { Routes, Route } from 'react-router-dom'
import "@fontsource-variable/vazirmatn/wght.css";

import "./App.css"
import routes from './routes';
import ScrollToTop from './scrollToTop'
import Footer from './component/footer/footer'
import { useRoutes } from 'react-router-dom'




export default function App() {
  let mainRoute = useRoutes(routes)
  return (
    <>
      <ScrollToTop />
      {mainRoute}
      <Footer />
    </>
  )
}
