// import { useState } from 'react'
import { useState } from "react";
import unicefLogo from "./assets/UNICEF-logo.png"
import './pages.css'
import '../unicef.scss';
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

  var[render,setRender]= useState(false);
  //if the username and password match, dont render anything
  const checkValid = (event) => {
    event.preventDefault(); 
    if(username==user && password==pass){
      // navigateToDashboards(`/dashboards/${url}/${username}`);
      navigateToDashboards(`/dashboards/${username}`, {state: url});
      setRender(false);
    }
    else{
      setRender(true);
    }
  }


  //TODO: once we have a backend, wrap our hooks in a useEffect that will retrieve 
  //the username and password from the backend API and set them to the hooks
  return (
    <>
  
      <body className="w-full flex h-full flex justify-center">
        <div className="content-wrapper h-1/2 flex flex-col justify-center">
          <img class="max-w-md mb-5" src={unicefLogo} className="logo" alt=""/>
          <label className="text-sky-400 font-semibold text-lg">——————————————————————</label>
          <label className="text-sky-400 font-semibold text-lg">For every child</label>
          <div className="form-wrapper">
              <form className="flex flex-col justify-center">
                <div className="mb-2 mt-5">
                  <label className="font-semibold text-xl text-sky-500" for="#url" >Superset Url: </label>
                  <input className="clone-input font-semibold" type="text" id="url"  onInput={handleUrl} required></input>
                </div>
                <div className="mb-2">
                  <label className="font-semibold text-xl text-sky-500" for="#url">Superset Username: </label>
                  <input className="clone-input font-semibold" type="text" id="url" onInput={handleUsername} required></input>
                </div>
                <div className="mb-5">
                  <label className="font-semibold text-xl text-sky-500" for="#url">Superset Password: </label>
                  <input  className="clone-input font-semibold" type="password" id="url" onInput={handlePassword} required></input>
                </div>
                <div className="button-wrapper flex justify-center">
                  <button className="bg-sky-400 w-48 text-white" onClick={checkValid}>Sign in</button>
                </div>
              </form>
              {
                render && 
                  <div class="alert alert-danger" role="alert">
                    <strong>Invalid Credentials, please try again!</strong>
                  </div>
              }
          </div>

        </div>
      </body>
    </>
  )
}

export default Login;
