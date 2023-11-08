// import { useState } from 'react'
import { useState } from "react";
import unicefLogo from "./assets/UNICEF-logo.png"
import './pages.css'
// import {useNavigate } from 'react-router-dom';
// import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
function Login() {

  const[url, setUrl] = useState('');  
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");
  //basic hooks to retreive username and password from form element
  const handleUsername=(event)=>{
    setUsername(event.target.value);
  }

  const handlePassword=(event)=>{
      setPassword(event.target.value);
  }
  const handleUrl = (event) => {
    setUrl(event.target.value)
  };

    //presumably,we'll have a backend that will check the username and password, but for now we'll
    //just hard code the user and pass
    const user ="testuser";
    const pass ="testpass";

    const navigateToDashboards = useNavigate();

  const[render,setRender]= useState(false);
  //if the username and password match, dont render anything
  const checkValid = (event) => {
    event.preventDefault(); 
    if(username==user && password==pass){
      navigateToDashboards(`/dashboards/${url}`);
    }
    else{
      setRender(!render)
    }
  }


  //TODO: once we have a backend, wrap our hooks in a useEffect that will retrieve 
  //the username and password from the backend API and set them to the hooks
  return (
    <>
  
      <body className="w-full flex h-full flex justify-center">

        <div className="content-wrapper  w-1/2 h-1/2 flex flex-col justify-center">
          
          <div className='shrink-0'>
            <img class="w-96 mx-auto mb-5" src={unicefLogo} className="logo" alt=""/>
          </div>
          
          <label className="text-sky-400 font-semibold text-lg">——————————————————————</label>
          <label className="text-sky-400 font-semibold text-lg">For every child</label>
      
          {/* <div className="form-wrapper" onSubmit={handleSubmit}> */}
          <div className="form-wrapper">
              <form className="flex flex-col ">
                <div className="form-group mb-2 mt-5">
                  <label className="text-sky-400 font-semibold text-lg" for="#url" >Dashboard URL: </label>
                  <input className="clone-input" type="text" id="url"  onInput={handleUrl} required></input>
                  {/* <input className="clone-input " type="text" id="url" required></input> */}
                </div>
                <div className="form-group mb-2">
                  <label className="text-sky-400 font-semibold text-lg" for="#url">Superset Username: </label>
                  <input className="clone-input " type="text" id="url" onInput={handleUsername} required></input>
                </div>
                <div className="form-group mb-5">
                  <label className="text-sky-400 font-semibold text-lg" for="#url">Superset Password: </label>
                  <input  className="clone-input " type="password" id="url" onInput={handlePassword} required></input>
                </div>
                <div className="button-wrapper flex justify-center">
                  {/* <button className="bg-sky-400 w-1/2 " onClick={handleSubmit}>Sign in</button> */}
                  <button className="bg-sky-400 w-48" onClick={checkValid}>Sign in</button>
                  
                  {/* <button className="bg-sky-400 w-1/2">Sign in</button> */}

                  
                </div>
              </form>
              {
                render && 
                  <div className="d-flex flex w-full d-flex justify-center">
                    <p className="text-red-500">Invalid Username or Password, please try again!</p>

                  </div>
              }
          </div>

        </div>
      </body>
    </>
  )
}

export default Login;
