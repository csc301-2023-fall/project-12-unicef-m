import React from 'react'
import ReactDOM from 'react-dom/client'
// import App from './App.jsx'

import Login from './pages/login_page.jsx'
import FinalClone from './pages/final_clone.jsx'
import TestFunc from './pages/test.jsx'
import Dashboards from './pages/dashboards.jsx'
import Update from './pages/update.jsx'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Login />,
    // login is our root page
  },

  {
    path: "/dashboards/:username",
    element: <Dashboards />,
  },

  //final_clone
  {
    path: "/final_clone/:username/:dashboard_name/:dashboard_id",
    element: <FinalClone />,
  },
  // add pages here following the format of   
  // {
  //   path: "/urlname",
  //   element: <Pagename />,
  // },

  // abandoned pages
  // {
  //   // path: "/update/:url/",
  //   path: "/update/:dashboard_name/",
  //   element: <Update />,
  //   // test function for seeing if data from login page is passed to test page
  // },  
  // {
  //   path: "/test",
  //   element: <TestFunc />,
  //   // test function for seeing if data from login page is passed to test page
  // },
]);


ReactDOM.createRoot(document.getElementById('root')).render(
  <RouterProvider router={router} />
  //below are code for strict mode, which will make the page render twice
  // <React.StrictMode>
  //   {/* <App /> */}
  //   <RouterProvider router={router} />
  // </React.StrictMode>,
)
