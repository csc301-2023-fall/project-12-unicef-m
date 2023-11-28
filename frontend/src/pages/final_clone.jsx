import './pages.css'
import { Link, useParams, useNavigate, useLocation} from 'react-router-dom';

import { useState, useEffect } from 'react';
import axios from 'axios';
//page for finalizing the cloning process along with a couple other fields for the user to fill out


function FinalClone() {
  let {username} = useParams();
  let {dashboard_name} = useParams();
  let {dashboard_id} = useParams();

  const location = useLocation();
  const superset_url = location.state;
  console.log(superset_url);

  const [chart_list, setChartList] = useState([]);
  let db_id =0
  const [sourcelist, setSourceList] = useState([]);
  const dashboard_list_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/all-dashboards';
  const source_list_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/all-datasets';
  let dataset_id=0
   useEffect(() => {
    axios.get(dashboard_list_endpoint).then((response) => {
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
    }).catch((error) => {
      console.error('Error fetching data from dashboard list endpoint:', error);
    });

    
    axios.get(source_list_endpoint).then((response) => {
      const sources = response.data;
      dataset_id = sources[0].dataset_id
      const s_list = [];
      sources.forEach(source => {
        // console.log(clone_endpoint, error)
        s_list.push([source.dataset_name,source.database_name])
      })
      // console.log(s_list)
      setSourceList(s_list);
    }).catch((error) => {
      console.error('Error fetching data from source list endpoint:', error);
    });
  },[]);
  // upon mounting, fetch the chart list from the backend

 //--------------------------------------------------------------------------------------------------
  
  const [db_name,setdb_name]=useState(dashboard_name);
  const [chart_and_source_list, appendChartAndSourceList] = useState([]);
  //list of charts, and the source that the user wants to use for each chart
  const handleSelect = (chartname, source) => {
    let pair = [chartname, source]  
    for (let i = 0; i < chart_and_source_list.length; i++) { 
      if (chart_and_source_list[i][0] == chartname) {
        chart_and_source_list[i][1] = source
        appendChartAndSourceList([...chart_and_source_list])
        return
      }
    }
    // do a check to see if the chartname is already in the list, and if it is, just update the source
    appendChartAndSourceList([...chart_and_source_list, pair])
  }
  const handledb_name=(event)=>{
    if (event.target.value!= db_name){
      setdb_name(event.target.value);
    }
  }
   //--------------------------------------------------------------------------------------------------
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

      chart_and_source_list.forEach(chart_and_source => {
        const chart_we_want = chart_in_chart_list[0]
        if (chart_and_source[0] ==chart_we_want) {
          // check if the chart name is in the chart_and_source_list
          // chart_and_source[0] is the chart name
          const chart_new_dataset = chart_and_source[1]
          // chart_attrib_list.push(chart_new_dataset)
          chart_attrib_list[2] = chart_new_dataset
          //push the source name to the chart attributes
        }

        sourcelist.forEach(source => {
          const source_we_want = chart_and_source[1]
          const source_name = source[0]
          if (source_name == source_we_want ) {
            // check if the source name is in the sourcelist
            const database = source[1]
            chart_attrib_list[3] = database

            // chart_attrib_list.push(database)
            //push the database name to the chart attributes
          }
        })

      })

      const chart_attributes ={
        "chart_id": chart_attrib_list[0],
        "chart_old_name": chart_attrib_list[1],
        "chart_new_dataset": chart_attrib_list[2],
        "database": chart_attrib_list[3]
      }
      charts.push(chart_attributes)
      // should now be a list of json objects, where each object is a chart and its attributes
    })

    const clone_response_data = {
      "dashboard_id": Number(dashboard_id),
      "dashboard_old_name": dashboard_old_name,
      "dashboard_new_name": dashboard_new_name, 
      "dataset_id": Number(dataset_id),
      "charts": charts
    }


    const clone_endpoint = import.meta.env.VITE_REACT_APP_BASEURL + '/view/clone';
    const[error,setError]= useState(null);
    const navigateToDashboards = useNavigate();
    const handleCloneSubmit = async(event) => {
      event.preventDefault();
      try{
        await axios({
          method: 'post',
          url: clone_endpoint,
          data: clone_response_data,
        })
        // navigateToDashboards(`/dashboards/${url}/${username}`);
         navigateToDashboards(`/dashboards/${username}`, state={superset_url});
        console.log("Success !")
        setError(null)
      } catch(error){
        setError(error.response ? error.response.data : error.message)
      }
    };


  return( 
    <>
    <body className="w-full flex h-full flex justify-center">

    <div className="content-wrapper  w-1/2 h-1/2 flex flex-col justify-center content-wrapper-sizing">
      <div className='flex gap-x-24'>
              <Link to={`/dashboards/${username}`} state={superset_url}><button className="bg-sky-400 w-48 h-12 text-white">←Previous</button></Link>
              </div>
              <h1 className="display-1 text-sky-400">{dashboard_name}</h1>      
      <div className="final-clone-wrapper h-4/5">
          <form className="flex flex-col h-full" method="POST" onSubmit={handleCloneSubmit}>
            <div className="form-group mb-2 mt-5 flex flex-row ">
              <label className="text-sky-400 font-bold text-xl w-1/6" for="#dashboard_name">Rename: </label>
              <input className="clone-input w-3/4 text-center" type="text" id="dashboard_name" onInput={handledb_name} required></input>
            </div>
            <div className="block gap-20 h-4/5 scrollable">
                {
                chart_list.map((chart) =>(
                    <div className="flex flex-row justify-around items-center h-1/3">
                        <div className="name-container">
                          <p className="text-sky-400 font-test">{chart[0]}</p>
                        </div>
                        <select className="w-1/2 h-1/2 bg-sky-400 text-white" 
                        onChange={(event) => handleSelect(chart[0], event.target.value) }>
                        <option>Select a source</option>
                          {
                            sourcelist.map((source) =>(
                              
                              <option value={source[0]}>{source[0]}</option>
                            ))
                          }
                        </select>
                    </div>

                  ))
                }
            </div>
            <div className="button-wrapper flex justify-center">
              <button className="bg-sky-400 w-1/2 text-lg text-white" type="submit">Finalize Clone</button>
            </div>
          </form>
      </div>
    </div>
</body>
    
    
    
    
</>)
}
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