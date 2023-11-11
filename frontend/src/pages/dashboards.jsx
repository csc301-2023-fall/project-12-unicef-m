import './pages.css'
import { Link, useParams} from 'react-router-dom';
//page for finalizing the cloning process along with a couple other fields for the user to fill out

import AutoAwesomeMotionIcon from '@mui/icons-material/AutoAwesomeMotion';
import Badge from '@mui/material/Badge';
import { useState, useEffect } from "react";
import axios from "axios";

function Dashboards() {

  let {dashboard_name} = useParams();
  let {username} = useParams();

  const notification = true;

  //assuming we've called response.get 
  const exampleJsonResponse = [
    {
      "dashboard_name": "Dashboard1",
      "dashboard_id": 1,
      "dashboard_description": "This is the first dashboard",
      "all_charts": [ 
        {
          "chart_name": "Chart1",
          "chart_id": 1,
        },
        {
          "chart_name": "Chart2",
          "chart_id": 2,
        },
        {
          "chart_name": "Chart3",
          "chart_id": 3,
        },
        {
          "chart_name": "Chart4",
          "chart_id": 4,
        },
        {
          "chart_name": "Chart5",
          "chart_id": 5,
        }
      ]
    },
    {
      "dashboard_name": "Dashboard2",
      "dashboard_id": 2,
      "dashboard_description": "This is the second dashboard",
      "all_charts": [ 
        {
          "chart_name": "Chart6",
          "chart_id": 6,
        },
        {
          "chart_name": "Chart7",
          "chart_id": 7,
        },
        {
          "chart_name": "Chart8",
          "chart_id": 8,
        },
        {
          "chart_name": "Chart9",
          "chart_id": 9,
        },
        {
          "chart_name": "Chart10",
          "chart_id": 10,
        }
      ]
    },
    {
      "dashboard_name": "Dashboard3",
      "dashboard_id": 3,
      "dashboard_description": "This is the third dashboard",
      "all_charts": [ 
        {
          "chart_name": "Chart11",
          "chart_id": 11,
        },
        {
          "chart_name": "Chart12",
          "chart_id": 12,
        },
        {
          "chart_name": "Chart13",
          "chart_id": 13,
        },
        {
          "chart_name": "Chart14",
          "chart_id": 14,
        },
        {
          "chart_name": "Chart15",
          "chart_id": 15,
        }
      ]
    },
  ];

  // const dashboardlist = []
  // exampleJsonResponse.forEach(dashboard => {
  //   const dashboard_name = dashboard.dashboard_name;
  //   const dashboard_id = dashboard.dashboard_id;
  //   const dashboard_description = dashboard.dashboard_description;
  //   dashboardlist.push([dashboard_name, dashboard_id, dashboard_description]);
  // });

  const [dashboardlist, setDashboardList] = useState([]);

  const dashboard_list_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/all-dashboards';
  // {process.env.REACT_APP_BASEURL} + /views/all-dashboards
  useEffect(() => {
    // upon mounting, fetch the dashboard list from the backend
    // upon changes to the dashboard list, update the dashboard list
    axios.get(dashboard_list_endpoint).then((response) => {
      const d_list = response.data;
      d_list.ForEach(dashboard => { 
        const dashboard_name = dashboard.dashboard_name;
        const dashboard_id = dashboard.dashboard_id;
        const dashboard_description = dashboard.dashboard_description;
        console.log(dashboard_name, dashboard_id, dashboard_description);
        dashboardlist.push([dashboard_name, dashboard_id, dashboard_description]);
      })
      setDashboardList(d_list);
    })
    .catch((error) => {
      console.error('Error fetching data from dashboard list endpoint:', error);
    });
  }),[dashboardlist];

  const [search_query, onSearch] = useState("");

  // const dashboardlist = ["Dashboard1", "Dashboard2", "Dashboard3", "Dashboard4", "Dashboard5", 
  // "Dashboard6", "Dashboard7", "Dashboard8", "Dashboard9", "Dashboard10"]

  //TODO 2: along the same vein, retrive information that notifies the user if there is an update available, and render
  //the update button accordingly


  const handleSearch = (event) =>{onSearch(event.target.value)}
  const handleEnter = (event) =>{if(event.key === 'Enter'){
    scrollToDashboard(search_query)
  }}
  const scrollToDashboard = (id) => {
    const element = document.getElementById(id);
    if( element){
      element.scrollIntoView({behavior: "smooth"});
    }
  }
  return( 
    <>
    <body className="w-full flex h-full flex justify-center">
      <div className="content-wrapper w-4/5 h-4/5 flex flex-col justify-center gap-y-3">
        <div class='flex justify-between'>
          <Link to="/"> <button className="bg-sky-400 h-full text-white">←Back to Login</button></Link>
          <label className="text-sky-400 font-semibold text-3xl">Dashboards for {username}</label>          
          <input type="text border-solid w-full" 
            placeholder='search for dashboard ...'
            onChange={handleSearch}
            onEnter={handleEnter}>
          </input>
        </div>

        {/* <div class="scroll-smooth"> */}
        <div class="block gap-20 h-screen scrollable bg-white">
            {
            dashboardlist.map((dashboard) => (
              <div className="mt-10 mb-10">
                <div className="h-full w-full list_grid" id={dashboard[0]}>
                  <div className="grid-element test">
                    <Link to={`/final_clone/${dashboard[0]}/${dashboard[1]}`}>
                      <button className="bg-sky-200  w-full h-full">
                        <h2 className="text-sky-400">{dashboard[2]}</h2>
                      </button>
                    </Link>
                    
                  </div>
                 
                  <div className="grid-element">
                    <Link to={`/update/${dashboard_name}`}>
                      <button className="text-sky-400 mr-2px hover:text-sky-600 ">Update Available</button>
                    </Link>
                  </div>
                  
                </div>
                <label className="text-sky-400 font-semibold text-xl">{dashboard[0]}</label>
              </div>
            ))
          }

        </div>
        {/* <div>
            <Link to={`/final_clone/${url}`}>
              <button className="bg-sky-200 w-full h-full" >
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
            <label className="text-sky-400 font-semibold text-xl">Dashboard0</label>
            
          </div>       */}


      </div>
      {/* </div> */}
    </body>
    </>
  )
}


export default Dashboards;