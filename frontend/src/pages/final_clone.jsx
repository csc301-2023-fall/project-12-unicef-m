import './pages.css'
import { Link, useParams, useNavigate} from 'react-router-dom';

import { useState, useEffect } from 'react';
import axios from 'axios';

//page for finalizing the cloning process along with a couple other fields for the user to fill out


function FinalClone() {

  let {dashboard_name} = useParams();
  let {dashboard_id} = useParams();

  // const [chartlist, setChartList] = useState([]);
  // const [sourcelist, setSourceList] = useState([]);

  // const chartlistendpoint = ""
  // const sourcelistendpoint= ""

  // useEffect(() => {
  //   axios.get(chartlistendpoint).then((response) => {
  //     const c_list = response.data;
  //     setChartList(c_list);
  //   });

  //   axios.get(sourcelistendpoint).then((response) => {
  //     const s_list = response.data;
  //     setSourceList(s_list);
  //   });
  // }),[chartlist, sourcelist];
  // upon mounting, fetch the chart list from the backend

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

  const chart_list=[]
  let db_id =0

  exampleJsonResponse.forEach(dashboard => { 
      if(dashboard.dashboard_name==dashboard_name){
        db_id=dashboard.dashboard_id
        console.log(db_id)
        dashboard.all_charts.forEach(chart => {
          chart_list.push(chart.chart_name)
          console.log(chart.chart_name)
        })
      }
  });

  const exampleSourceJsonResponse = 
  [
    {
      "dataset_name": "name1",
      "database_name": "db1"
    },
    {
      "dataset_name": "name2",
      "database_name": "db2"
    },
    {
      "dataset_name": "name3",
      "database_name": "db3"
    }
  ]
  const source_list=[]

  exampleSourceJsonResponse.forEach(data_set => { 
    source_list.push(data_set.dataset_name)
  })


  // const faux_chart_list=["Chart1", "Chart2", "Chart3", "Chart4", "Chart5"]
  // const faux_source_list=["Source1", "Source2", "Source3", "Source4", "Source5"]
  //later we'll just have a backend that will check the dashboard_id and password, but for now we'll
  //just hard code list of charts and sources


  // const [DBname,setDBname]=useState("");
  const [db_name,setdb_name]=useState(dashboard_name);
  const [chart_and_source_list, appendChartAndSourceList] = useState([]);
  //list of charts, and the source that the user wants to use for each chart



  //basic hooks to retreive username and password from form element

  // const selectSource=(event)=>{
  //   setChartAndSourceList([...chart_and_source_list, [chart_name, event.target.value]])
  // }

  const handleSelect = (chartname, source) => {
    // console.log( (chartname, source) )

    let pair = [chartname, source]
    console.log( pair )
    console.log( chart_and_source_list )
  
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
    console.log(event.target.value)
    if (event.target.value!= db_name){
      setdb_name(event.target.value);
    }
  }
    //presumably,we'll have a backend that will check the username and password, but for now we'll
    //just hard code the user and pass
    
  const navigateToDashboards = useNavigate();
  // const notfication=null;
  const[render,setRender]= useState(false);
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
    return( 
    <>
        <body className="w-full flex h-full flex justify-center">

<div className="content-wrapper  w-1/2 h-1/2 flex flex-col justify-center">
  {/* <div className="form-wrapper" onSubmit={handleSubmit}> */}
  <div class='flex gap-x-24'>
          {/* <Link to="/dashboards"> <button className="bg-sky-400 w-48 h-12">←Previous</button></Link> */}
          {/* <Link to={`/dashboards/${dashboard_name}`}> <button className="bg-sky-400 w-48 h-12">←Previous</button></Link> */}
          <Link to={`/dashboards/${dashboard_name}/${dashboard_id}`}><button className="bg-sky-400 w-48 h-12 text-white">←Previous</button></Link>
           </div>
           <h1 className="display-1 text-sky-400">{dashboard_name}</h1>      
  <div className="final-clone-wrapper h-4/5 ">
  
      <form className="flex flex-col h-full">
        <div className="form-group mb-2 mt-5 flex flex-row ">
          <label className="text-sky-400 font-semibold text-2xl" for="#dashboard_name">Rename: </label>
          {/* <input className="bg-sky-200" type="text" id="dashboard_name" value={dashboard_name} onChange={handleChange}></input> */}
          <input className="clone-input w-3/4 text-center" type="text" id="dashboard_name" onInput={handledb_name} required></input>
        </div>
        <div class="block gap-20 h-4/5 scrollable">
            {
            chart_list.map((chart_name) =>(
                <div className="flex flex-row justify-around items-center h-1/3">
                    <h2 className="text-sky-400 font-test">{chart_name}</h2>
                    <select className="w-1/2 h-1/2 bg-sky-400" 
                    onChange={(event) => handleSelect(chart_name, event.target.value) }>
                    <option>Select a source</option>
                      {
                        source_list.map((source_name) =>(
                          
                          <option value={source_name}>{source_name}</option>
                        ))
                      }
                    </select>
                </div>

              ))
            }
        </div>
        
        <div className="button-wrapper flex justify-center">
          {/* <button className="bg-sky-400 w-1/2 " onClick={handleSubmit}>Sign in</button> */}
          <button className="bg-sky-400 w-1/2 text-lg">Finalize Clone</button>
        </div>
      </form>


      {/* {
        render && !valid && 
        <div className="d-flex flex w-full d-flex justify-center">
            <p className="text-red-500">Something went wrong, please try again !</p>

        </div>
      }

      {
        render || valid && 
        <div className="d-flex flex w-full d-flex justify-center">
            <p className="text-green-500 ">Cloning Successful!</p>

        </div>
      } */}
  
  </div>

</div>
</body>
    
    
    
    
    </>)
}


export default FinalClone;