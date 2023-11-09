import './pages.css'
import { Link, useParams} from 'react-router-dom';
//page for finalizing the cloning process along with a couple other fields for the user to fill out

import AutoAwesomeMotionIcon from '@mui/icons-material/AutoAwesomeMotion';
import Badge from '@mui/material/Badge';
import { useState, useEffect } from "react";
import axios from "axios";
function Dashboards() {

  let {url} = useParams();
  let {username} = useParams();

  const notification = true;

  // const [dashboardlist, setDashboardList] = useState([]);

  // const dashboard_list_endpoint = ""
  // useEffect(() => {
  //   // upon mounting, fetch the dashboard list from the backend
  //   // upon changes to the dashboard list, update the dashboard list
  //   axios.get(dashboard_list_endpoint).then((response) => {
  //     const d_list = response.data;
  //     setDashboardList(d_list);
  //   })
  //   .catch((error) => {
  //     console.error('Error fetching data:', error);
  //   });
  // }),[dashboardlist];


  const dashboardlist = ["Dashboard1", "Dashboard2", "Dashboard3", "Dashboard4", "Dashboard5", "Dashboard6"]

  //TODO 2: along the same vein, retrive information that notifies the user if there is an update available, and render
  //the update button accordingly

  return( 
    <>
    <body className="w-full flex h-full flex justify-center">
      <div className="content-wrapper  w-1/2 h-1/2 flex flex-col justify-center gap-y-3">


        <div class='flex shrink'>
          <Link to="/"> <button className="bg-sky-400 w-full h-full">←Back to Login</button></Link>
        </div>
        <div class='flex shrink justify-center'>
          <label className="text-sky-400 font-semibold text-3xl">Dashboards for {username}</label>
        </div>
        

        {/* <div class="scroll-smooth"> */}
        <div class="grid grid-cols-3 gap-20 h-screen">
          <div>
            <Link to={`/final_clone/${url}`}>
              <button className="bg-sky-200  w-full h-full" >
                  {
                    notification && <div className="d-flex flex w-full">
                    <Link to={`/update/${url}`}>
                      <p className="text-sky-400 mr-2px hover:text-sky-600 ">Update Available</p>
                    </Link>
                   
                    <Badge badgeContent={1} color="secondary">
                        <AutoAwesomeMotionIcon color="action" />
                    </Badge>
                  </div>
                  }
              </button>
            </Link>
            <label className="text-sky-400 font-semibold text-xl">Dashboard1</label>
            
          </div>      

            {
            dashboardlist.map((dashboard_name) => (
              <div>
                <Link to={`/final_clone/${url}`}><button className="bg-sky-200  w-full h-full" ></button></Link>
                <label className="text-sky-400 font-semibold text-xl">{dashboard_name}</label>
              </div>
            ))
          }

        </div>


      </div>
      {/* </div> */}
    </body>
    </>
  )
}


export default Dashboards;