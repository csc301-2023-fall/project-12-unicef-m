import './pages.css'
import { Link, useParams, useNavigate} from 'react-router-dom';

import { useState } from 'react';

//page for finalizing the cloning process along with a couple other fields for the user to fill out


// {`/dashboards/${url}`}
function FinalClone() {
  const [language,setLanguage]=useState("");
  const [DBname,setDBname]=useState("");
  //basic hooks to retreive username and password from form element
  const handleLanguage=(event)=>{
    setLanguage(event.target.value);
  }

  const handleDBname=(event)=>{
    setDBname(event.target.value);
  }

    //presumably,we'll have a backend that will check the username and password, but for now we'll
    //just hard code the user and pass
    const eng ="english";
    const navigateToDashboards = useNavigate();
  // const notfication=null;
  const[render,setRender]= useState(false);
  // if the information isnt correct in some way, or we've
  // ecounter an error from the backend, we'll render this
  // const handleButton=(event)=>{
  //   event.preventDefault(); 
  //   setRender(!render)
  // }  
  const valid=false;
  //if the username and password match, dont render anything
  const checkValid = (event) => {
    event.preventDefault(); 
    if(language==eng && DBname!=""){
      navigateToDashboards(`/dashboards/${url}`);
    }
    else{
      setRender(!render)
    }
  }
  //in the futre, reconfigure this so that, on a successful clone, along with render
  // we'll render a success popup
  // for now though, since we dont have a backend, we'll just render this on button press
  // unconditionaly
let {url} = useParams();
    return( 
    <>
        <body className="w-full flex h-full flex justify-center">

<div className="content-wrapper  w-1/2 h-1/2 flex flex-col justify-center">
  {/* <div className="form-wrapper" onSubmit={handleSubmit}> */}
  <div class='flex gap-x-24'>
          {/* <Link to="/dashboards"> <button className="bg-sky-400 w-48 h-12">←Previous</button></Link> */}
          {/* <Link to={`/dashboards/${url}`}> <button className="bg-sky-400 w-48 h-12">←Previous</button></Link> */}
          <Link to={`/dashboards/${url}`}><button className="bg-sky-400 w-48 h-12">←Previous</button></Link>
           </div>
           
  <div className="final-clone-wrapper">
    
      <form className="flex flex-col">
        <div className="form-group mb-2 mt-5 flex flex-col items-center">
          <label className="text-sky-400 font-semibold text-2xl" for="#url" >Language </label>
          {/* <input className="bg-sky-200" type="text" id="url" value={url} onChange={handleChange}></input> */}
          <input className="clone-input w-3/4 text-center" type="text" id="url" onInput={handleLanguage} required></input>
        </div>

        {/*Todo, figure out how to auto populate this stuff, but for now just leave it as a text field */}
        <div className="form-group mb-5 flex  flex-col items-center">
          <label className="text-sky-400 font-semibold text-2xl" for="#url">Dashboard Name </label>
          <input className="clone-input  w-3/4 text-center"type="text" id="url" onInput={handleDBname} required></input>
        </div>
        <div className="button-wrapper flex justify-center">
          {/* <button className="bg-sky-400 w-1/2 " onClick={handleSubmit}>Sign in</button> */}
          <button className="bg-sky-400 w-1/2 text-lg" onClick={checkValid}>Finalize Clone</button>
        </div>
      </form>
      {
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
      }
  
  </div>

</div>
</body>
    
    
    
    
    </>)
}


export default FinalClone;