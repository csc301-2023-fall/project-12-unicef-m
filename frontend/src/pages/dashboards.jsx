import './pages.css'
import { Link, useParams} from 'react-router-dom';
//page for finalizing the cloning process along with a couple other fields for the user to fill out
import {useLocation} from 'react-router-dom';
import AutoAwesomeMotionIcon from '@mui/icons-material/AutoAwesomeMotion';
import Badge from '@mui/material/Badge';
import { useState, useEffect } from "react";
import axios from "axios";
import SyncLoader from "react-spinners/SyncLoader";

function Dashboards() {

  // let {url} = useParams();
  const location = useLocation();
  const superset_url = location.state;
  var [loading, setLoading]=useState(true);
  console.log(superset_url);
  let {username} = useParams();

  const notification = true;

  const [dashboardlist, setDashboardList] = useState([]);

  const dashboard_list_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/all-dashboards';

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    const fetchData = async () => {
      console.log("fetching");
      try {
        const response = await axios.get(dashboard_list_endpoint);
        if (isMounted) {
          const d_list = response.data;
          const new_list = d_list.map(dashboard => [dashboard.dashboard_name, dashboard.dashboard_id, dashboard.dashboard_description]);
          setDashboardList(new_list);
          // console.log(dashboardlist);
        }
      } catch (error) {
        console.error('Error fetching data from dashboard list endpoint:', error);
      }
      setLoading(false);
    console.log("fetched");
    };
  
    fetchData();
    return () => {
      isMounted = false;
    };
  }, []);
  console.log(dashboardlist);
  const [search_query, onSearch] = useState("");
  var[render,setRender]= useState(false);


  const handleSearch = (event) =>{
    onSearch(event.target.value);
  }
  const handleEnter = () =>{
    scrollToDashboard(search_query);
  }
  const scrollToDashboard = (id) => {
    const element = document.getElementById(id);
    if(element){
      element.scrollIntoView({behavior: "smooth"});
      setRender(false);
    }
    else{
      setRender(true);
    }
  }
  return( 
    <>
    <body className="w-full flex h-full flex justify-center">
      <div className="content-wrapper w-4/5 h-4/5 flex flex-col justify-center gap-y-3">
        <div className='flex justify-between'>
          <Link to="/"> <button className="bg-sky-400 h-full text-white">←Back to Login</button></Link>
          <label className="text-sky-400 font-semibold text-3xl">Dashboards for {username}</label>          
          <input className="border-solid w-half" type="text" 
            placeholder='search for dashboard ...'
            onChange={handleSearch}>
          </input>
          <button className="bg-sky-400 text-white"onClick={handleEnter}>Search</button>
        </div>
          <div>
          {
            render &&
            <div class="alert alert-danger" role="alert">
            <strong>Dashboard does not exist, please try again !</strong>
            </div>
          }
          </div>
        <div className="block gap-20 h-screen scrollable bg-white">
          <SyncLoader loading={loading} size={10} color='#1CABE2'></SyncLoader>
          {
            dashboardlist.map((dashboard) => (
              <div className="mt-10 mb-10" key={dashboard[0]}>
                <div className="h-full w-full list_grid" id={dashboard[0]}>
                  <div className="grid-element">
                    <Link to={`/final_clone/${username}/${dashboard[0]}/${dashboard[1]}`} state={superset_url}>
                      <button className="bg-sky-200  w-full h-full">
                        <h2 className="text-sky-400">{dashboard[2]}</h2>
                      </button>
                    </Link>
                    
                  </div>
                  {/* below are code for buttons to access updates in version control, UNICEF didn't want this functionality anymore thus commented out*/}
                  {/* buttons usage: buttons only pop up if there are any updates in version control, this would lead you to the version control page, code see update.jsx */}
                  {/* <div className="grid-element">
                    <Link to={`/update/${dashboard[0]}`} state={{superset_url: {superset_url}, username:{username}}}>
                      <button className="text-sky-600 mr-2px hover:text-sky-800 ">Update Available</button>
                    </Link>
                  </div> */}
                  
                </div>
                <label className="text-sky-500 font-semibold text-xl">{dashboard[0]}</label>
              </div>
            ))
          }
        </div>
      </div>
    </body>
    </>
  )
}

//below is an example we used for testing
//assuming we've called response.get 
  // const exampleJsonResponse = [
  //   {
  //     "dashboard_name": "Dashboard1",
  //     "dashboard_id": 1,
  //     "dashboard_description": "This is the first dashboard",
  //     "all_charts": [ 
  //       {
  //         "chart_name": "Chart1",
  //         "chart_id": 1,
  //       },
  //       {
  //         "chart_name": "Chart2",
  //         "chart_id": 2,
  //       },
  //       {
  //         "chart_name": "Chart3",
  //         "chart_id": 3,
  //       },
  //       {
  //         "chart_name": "Chart4",
  //         "chart_id": 4,
  //       },
  //       {
  //         "chart_name": "Chart5",
  //         "chart_id": 5,
  //       }
  //     ]
  //   },
  //   {
  //     "dashboard_name": "Dashboard2",
  //     "dashboard_id": 2,
  //     "dashboard_description": "This is the second dashboard",
  //     "all_charts": [ 
  //       {
  //         "chart_name": "Chart6",
  //         "chart_id": 6,
  //       },
  //       {
  //         "chart_name": "Chart7",
  //         "chart_id": 7,
  //       },
  //       {
  //         "chart_name": "Chart8",
  //         "chart_id": 8,
  //       },
  //       {
  //         "chart_name": "Chart9",
  //         "chart_id": 9,
  //       },
  //       {
  //         "chart_name": "Chart10",
  //         "chart_id": 10,
  //       }
  //     ]
  //   },
  //   {
  //     "dashboard_name": "Dashboard3",
  //     "dashboard_id": 3,
  //     "dashboard_description": "This is the third dashboard",
  //     "all_charts": [ 
  //       {
  //         "chart_name": "Chart11",
  //         "chart_id": 11,
  //       },
  //       {
  //         "chart_name": "Chart12",
  //         "chart_id": 12,
  //       },
  //       {
  //         "chart_name": "Chart13",
  //         "chart_id": 13,
  //       },
  //       {
  //         "chart_name": "Chart14",
  //         "chart_id": 14,
  //       },
  //       {
  //         "chart_name": "Chart15",
  //         "chart_id": 15,
  //       }
  //     ]
  //   },
  // ];

  // const dashboardlist = []
  // exampleJsonResponse.forEach(dashboard => {
  //   const dashboard_name = dashboard.dashboard_name;
  //   const dashboard_id = dashboard.dashboard_id;
  //   const dashboard_description = dashboard.dashboard_description;
  //   dashboardlist.push([dashboard_name, dashboard_id, dashboard_description]);
  // });

export default Dashboards;