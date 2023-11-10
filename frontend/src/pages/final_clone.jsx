import './pages.css'
import { Link, useParams, useNavigate} from 'react-router-dom';

import { useState } from 'react';

//page for finalizing the cloning process along with a couple other fields for the user to fill out


function FinalClone() {

  let {url} = useParams();
  let {username} = useParams();

  const faux_chart_list=["Chart1", "Chart2", "Chart3", "Chart4", "Chart5"]
  const faux_source_list=["Source1", "Source2", "Source3", "Source4", "Source5"]
  //later we'll just have a backend that will check the username and password, but for now we'll
  //just hard code list of charts and sources


  // const [DBname,setDBname]=useState("");
  const [chartname,setChartname]=useState(url);
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

  const handleChartname=(event)=>{
    console.log(event.target.value)
    if (event.target.value!= chartname){
      setChartname(event.target.value);
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
  //     navigateToDashboards(`/dashboards/${url}`);
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
          {/* <Link to={`/dashboards/${url}`}> <button className="bg-sky-400 w-48 h-12">←Previous</button></Link> */}
          <Link to={`/dashboards/${url}/${username}`}><button className="bg-sky-400 w-48 h-12">←Previous</button></Link>
           </div>
           <h1 className="display-1 text-sky-400">{url}</h1>      
  <div className="final-clone-wrapper h-4/5 ">
  
      <form className="flex flex-col h-full">
        <div className="form-group mb-2 mt-5 flex flex-row ">
          <label className="text-sky-400 font-semibold text-2xl" for="#url">Rename: </label>
          {/* <input className="bg-sky-200" type="text" id="url" value={url} onChange={handleChange}></input> */}
          <input className="clone-input w-3/4 text-center" type="text" id="url" onInput={handleChartname} required></input>
        </div>
        <div class="block gap-20 h-4/5 scrollable">
            {
            faux_chart_list.map((chart_name) =>(
                <div className="flex flex-row justify-around items-center h-1/3">
                    <h2 className="text-sky-400 font-test">{chart_name}</h2>
                    <select className="w-1/2 h-1/2 bg-sky-400" 
                    onChange={(event) => handleSelect(chart_name, event.target.value) }>
                    <option>Select a source</option>
                      {
                        faux_source_list.map((source_name) =>(
                          
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