import './pages.css'
import { Link, useParams, useNavigate, useLocation} from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import SyncLoader from "react-spinners/SyncLoader";
//page for finalizing the cloning process along with a couple other fields for the user to fill out


function FinalClone() {
  // code for fetching information from api calls
  let {username} = useParams();
  let {dashboard_name} = useParams();
  let {dashboard_id} = useParams();
  const location = useLocation();
  const superset_url = location.state;
  // console.log(superset_url);
  var [loading, setLoading]=useState(true);

  const [chart_list, setChartList] = useState([]);
  let db_id =0
  const [sourcelist, setSourceList] = useState([]);
  const dashboard_list_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/all-dashboards';
  const source_list_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/all-datasets';
  // let dataset_id=0


  

   useEffect(() => {
    setLoading(true);
    axios.get(dashboard_list_endpoint).then((response) => {
      // getting dashboard info
      const d_list = response.data;
      const c_list = [];
      d_list.forEach(dashboard => {
        if(dashboard.dashboard_name==dashboard_name){
          db_id=dashboard.dashboard_id
          dashboard.all_charts.forEach(chart => {
            c_list.push([chart.chart_name, chart.chart_id])
          })
        }
      })
      setChartList(c_list);
      
      // console.log(c_list)
      setChartList(c_list);  // upon mounting, fetch the chart list from the backend
      setLoading(false);
    }).catch((error) => {
      console.error('Error fetching data from dashboard list endpoint:', error);
    });

    
    axios.get(source_list_endpoint).then((response) => {
      // getting source info
      const sources = response.data;
      // console.log("sources",response.data)
      // let d_id = sources[0].dataset_id
      // setDatasetId(d_id)
      // console.log("dataset id inner", dataset_id)
      const s_list = [];
      sources.forEach(source => {
        // console.log(clone_endpoint, error)
        // console.log([source.dataset_name,source.database_name, source.dataset_id])
        s_list.push([source.dataset_name,source.database_name, source.dataset_id])
      })
      // console.log(s_list)
      setSourceList(s_list);
    }).catch((error) => {
      console.error('Error fetching data from source list endpoint:', error);
    });
  },[]);

  console.log("source list ", sourcelist)
  console.log("chart list ", chart_list)



  // upon mounting, fetch the chart list from the backend
  // console.log("dataset id outer", dataset_id)
  // console.log(chart_list, sourcelist)//debugging purposes

  const [db_name,setdb_name]=useState(dashboard_name);
  const [chart_and_newname_list, appendChartAndNewNameList] = useState([]); //list of charts, and the name that the user wants to use for each chart
  chart_list.forEach(chart => {chart_and_newname_list.append([c[0],c[0]])}) // prepopulate with identical names
  const handleRename = (chartname, newname) => {

    // let dataset_id = 0
    // sourcelist.forEach(sourceIndex => {
    //   if (sourceIndex[0] == source) {
    //     dataset_id = sourceIndex[2]
    //   }
    // })
    let pair = [chartname, newname]  
    for (let i = 0; i < chart_and_newname_list.length; i++) { 
      if (chart_and_newname_list[i][0] == chartname) {
        chart_and_newname_list[i][1] = newname
        appendChartAndNewNameList([...chart_and_newname_list])
        return
      }
    }
    // do a check to see if the chartname is already in the list, and if it is, just update the name

    //otherwise add to list(prob will never get called)
    appendChartAndNewNameList([...chart_and_newname_list, pair])
  }




  // console.log("chart and newname list", chart_and_newname_list)
  const handledb_name=(event)=>{
    if (event.target.value!= db_name){
      setdb_name(event.target.value);
    }
  }

  const[dataset,setDataset]= useState("");
  const chooseDataset = (event) => {
    setDataset(event.target.value);
  }

  let dataset_name=""
  let database_name=""
  let dataset_id=0


  sourcelist.forEach(source => {
    if(source[0] == dataset){
      dataset_name = source[0]
      database_name = source[1]
      dataset_id = source[2]
    }
  })

  // console.log("dataset for all charts", dataset)
  console.log("dataset_name, database_name and dataset_id for dataset", dataset_name, database_name, dataset_id)


  //use enabled_across_instance_cloning to determine if we should include the url,username,and pass in the json object
  const[enabled_across_instance_cloning,setEnableAcrossInstanceCloning]= useState(false);
  const handleAcrossInstanceCloning = (event) => { 
    if(event.target.checked){
      setEnableAcrossInstanceCloning(true);
    }
    else{
      setEnableAcrossInstanceCloning(false);
    }
  }
  console.log("across instance cloning enabled?", enabled_across_instance_cloning)

  // data, for across instance cloning
  const[superSet_url,setSupersetUrl]= useState("");
  const[superSet_username,setSupersetUsername]= useState("");
  const[superSet_password,setSupersetPassword]= useState("");

  // console.log("superset url: ", superSet_url)
  // console.log("superset username: ", superSet_username)
  // console.log("superset password: ", superSet_password)




   //--------------------------------------------------------------------------------------------------
   // this is the packaging code for building the json object to send to the backend
    const dashboard_old_name = dashboard_name;
    const dashboard_new_name = db_name;
    //also have dashboard id
    const charts = []
    //chart_list is a list of lists whwere each list is the name of the chart as well and the id of the chart, for a given dashboard
    //sourcelist is a list of lists, where each list is a pair of source name and database name respectively 
    //chart_and_source_list is a list of lists, where each list is a pair of chart name and new source name respectively
    chart_list.forEach(chart_in_chart_list => {
      const chart_attrib_list=[]
      const chart_id = chart_in_chart_list[1]
      const chart_name = chart_in_chart_list[0]
      chart_attrib_list[0] = chart_id
      chart_attrib_list[1] = chart_name

      chart_and_newname_list.forEach(chart_and_newname => {
        const chart_we_want = chart_in_chart_list[0]
        if (chart_and_newname[0] ==chart_we_want) {
          // check if the chart name is in the chart_and_newname
          // chart_and_newname[0] is the old chart name
          const chart_new_name = chart_and_newname[1]
          // chart_attrib_list.push(chart_new_dataset)
          chart_attrib_list[2] = chart_new_name
          //push the source name to the chart attributes
        }


      })

      const chart_attributes ={
        "chart_id": chart_attrib_list[0],
        "chart_old_name": chart_attrib_list[1],
        "chart_new_name": chart_attrib_list[2]
      }
      charts.push(chart_attributes)
      // should now be a list of json objects, where each object is a chart and its attributes
    })

    const clone_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/clone';
    const[error,setError]= useState(null);
    const navigateToDashboards = useNavigate();
    const handleCloneSubmit = async(event) => {
      const clone_response_data2 = {
        "dashboard_id": Number(dashboard_id),
        "dashboard_old_name": dashboard_old_name,
        "dashboard_new_name": dashboard_new_name, 
        "dataset_id": chart_and_source_list[0][2],
        "charts": charts
      }
      console.log("clone response data2", clone_response_data2)
      event.preventDefault();
      try{
        await axios({
          method: 'post',
          url: clone_endpoint,
          data: clone_response_data2,
        })
         navigateToDashboards(`/dashboards/${username}`, {state: superset_url});
        console.log("Success !")
        setError(null)
      } catch(error){
        setError(error.response ? error.response.data : error.message)
      }
      // navigateToDashboards(`/dashboards/${username}`, state={superset_url});
    };


  return( 
    <>
    <body className="w-full flex h-full flex justify-center">

    <div className="content-wrapper  w-3/4 h-full flex flex-col justify-center content-wrapper-sizing">
      <div className='flex gap-x-24'>
              <Link to={`/dashboards/${username}`} state={superset_url}><button className="bg-sky-400 w-48 h-12 text-white">←Previous</button></Link>
              </div>
              <h1 className="display-1 text-sky-400">{dashboard_name}</h1>      
      <div className="final-clone-wrapper h-7/8">
          <form className="flex flex-col h-full" method="POST" onSubmit={handleCloneSubmit}>
            <div className="form-group mb-2 mt-5 flex flex-row ">
              <label className="text-sky-400 font-bold text-xl w-1/6" for="#dashboard_name">Rename: </label>
              <input className="clone-input w-3/4 text-center text-black" type="text" id="dashboard_name" onInput={handledb_name} required></input>
            </div>

            <div className="form-group mb-2 mt-5 flex flex-row ">
              <label className="text-sky-400 font-bold text-xl w-1/6" for="#dashboard_name">Choose Dataset: </label>
              <select className="w-1/3 h-full bg-sky-400 text-white" 
                        onChange={chooseDataset}>
                        <option>Select a source</option>
                          {
                            sourcelist.map((source) =>(
                              
                              <option value={source[0]}>{source[0]}</option>
                            ))
                          }
                </select>
            </div>
            <div className="block gap-20 h-4/5 scrollable">
              {/* loading animation */}
            <SyncLoader loading={loading} size={10} color='#1CABE2'></SyncLoader>
                {
                  // mapping source to charts
                chart_list.map((chart) =>(
                    <div className="flex flex-row justify-around items-center h-1/8 mb-3 mt-3 input-wrapper">
                        <div className="name-container h-full w-full">
                          <p className="text-sky-400 font-test">{chart[0]}</p>
                          <input className="clone-input w-3/4 text-center text-black" type="text" id="dashboard_name" placeholder="optional rename" onChange={(event)=>handleRename(chart[0],event.target.value)}></input>
                        </div>
                        {/* <select className="w-1/2 h-1/2 bg-sky-400 text-white" 
                        onChange={(event) => handleSelect(chart[0], event.target.value) }>
                        <option>Select a source</option>
                          {
                            sourcelist.map((source) =>(
                              
                              <option value={source[0]}>{source[0]}</option>
                            ))
                          }
                        </select> */}
                    </div>

                  ))
                }
            </div>


            <div className="form-group mb-2 mt-2 flex flex-row justify-center">
              <label className="text-sky-400 font-bold text-xl w-1/2" for="#dashboard_name">Enable across instance cloning ?: </label>
              <input type="checkbox" onChange={handleAcrossInstanceCloning}></input>
            </div>

            { enabled_across_instance_cloning && 
            <div className="form-group mb-2 mt-2 flex flex-col items-center">
              <input type="text" className="text-sky-400 font-bold text-xl w-1/2 bg-sky-200 mb-2 placeholder:text-sky-400" placeholder='Superset Url ...' onChange={(e)=>setSupersetUrl(e.target.value)}/>
              <input type="text" className="text-sky-400 font-bold text-xl w-1/2 bg-sky-200 mb-2 placeholder:text-sky-400" placeholder="Superset username ..." onChange={(e) => setSupersetUsername(e.target.value)}/>
              <input type="password" className="text-sky-400 font-bold text-xl w-1/2 bg-sky-200 placeholder:text-sky-400" placeholder="superset password ..."onChange={(e) => setSupersetPassword(e.target.value)}/>
            </div>}

            {
              enabled_across_instance_cloning && !(superSet_username && superSet_password && superSet_url) &&
              <div class="alert alert-danger" role="alert">
              <strong>Notice, you MUST fill out all fields to clone across instances</strong>
              </div>
            }
            <div className="button-wrapper flex justify-center">
              <button className="bg-sky-400 w-1/2 text-lg text-white" type="submit">Finalize Clone</button>
            </div>
          </form>
      </div>
    </div>
</body>
    
    
    
    
</>)
}
//below are hardcoded data we used for test and debug
  //presumably,we'll have a backend that will check the username and password, but for now we'll
    //just hard code the user and pass
    
  // const navigateToDashboards = useNavigate();
  // const notfication=null;
  // const[render,setRender]= useState(false);
  // if the information isnt correct in some way, or we've
  // ecounter an error from the backend, we'll render this

  // const valid=false;
  // //if the username and password match, dont render anything
  // const checkValid = (event) => {
  //   event.preventDefault(); 
  //   if(language==eng && DBname!=""){
  //     navigateToDashboards(`/dashboards/${dashboard_name}`);
  //   }
  //   else{
  //     setRender(!render)
  //   }
  // }

   // const chart_list=[]
  

  // exampleJsonResponse.forEach(dashboard => { 
  //     if(dashboard.dashboard_name==dashboard_name){
  //       db_id=dashboard.dashboard_id
  //       console.log(db_id)
  //       dashboard.all_charts.forEach(chart => {
  //         chart_list.push(chart.chart_name)
  //         console.log(chart.chart_name)
  //       })
  //     }
  // });

  // const exampleSourceJsonResponse = 
  // [
  //   {
  //     "dataset_name": "name1",
  //     "database_name": "db1"
  //   },
  //   {
  //     "dataset_name": "name2",
  //     "database_name": "db2"
  //   },
  //   {
  //     "dataset_name": "name3",
  //     "database_name": "db3"
  //   }
  // ]
  // const source_list=[]

  // exampleSourceJsonResponse.forEach(data_set => { 
  //   source_list.push(data_set.dataset_name)
  // })


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

export default FinalClone;