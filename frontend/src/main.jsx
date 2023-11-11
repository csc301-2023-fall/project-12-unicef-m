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
    // path: "/login",
    element: <Login />,
    // login is our root page
  },
  {
    path: "/test",
    element: <TestFunc />,
    // test function for seeing if data from login page is passed to test page
  },
  // {
  //   path: "/dashboards",
  //   element: <Dashboards />,
  // },

  {
    path: "/dashboards/:dashboard_name/:username",
    element: <Dashboards />,
    // test function for seeing if data from login page is passed to test page
  },

  {
    path: "/update/:url/",
    element: <Update />,
    // test function for seeing if data from login page is passed to test page
  },
  //final_clone
  {
    path: "/final_clone/:dashboard_name/:dashboard_id",
    // path: "/",
    element: <FinalClone />,
    // test function for seeing if data from login page is passed to test page
  },
  
]);


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* <App /> */}
    <RouterProvider router={router} />
  </React.StrictMode>,
)
