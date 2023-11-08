import './pages.css'
import { Link, useParams} from 'react-router-dom';
//page for finalizing the cloning process along with a couple other fields for the user to fill out

import AutoAwesomeMotionIcon from '@mui/icons-material/AutoAwesomeMotion';
import Badge from '@mui/material/Badge';
function Dashboards() {

  let {url} = useParams();

  const notification = true;



  //TODO: once we have a backend, use useEffect and hooks to retrieve information for the dashboards
  //TODO 2: along the same vein, retrive information that notifies the user if there is an update available, and render
  //the update button accordingly
  //TODO 3: like todo 1, we need to do some logic so that each of the dashboard cards are rendered dynamically

  return( 
    <>
    <body className="w-full flex h-full flex justify-center">
      <div className="content-wrapper  w-1/2 h-1/2 flex flex-col justify-center gap-y-3">
        <div class='flex shrink'>
          <Link to="/"> <button className="bg-sky-400 w-full h-full">←Back to Login</button></Link>
        </div>
        <div class='flex shrink justify-center'>
          <label className="text-sky-400 font-semibold text-3xl">Dashboards for {url}</label>
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

                    {/*in the future this will be updated with how many versions behind the current dashboard is, but for now we 
                    cant do that yet*/}
                   
                    <Badge badgeContent={1} color="secondary">
                        <AutoAwesomeMotionIcon color="action" />
                    </Badge>
                  </div>
                  }
              </button>
            </Link>
            <label className="text-sky-400 font-semibold text-xl">Dashboard1</label>
            
          </div>          
          <div>
            <Link to={`/final_clone/${url}`}><button className="bg-sky-200 w-full h-full" ></button></Link>
            <label className="text-sky-400 font-semibold text-xl">Dashboard2</label>
          </div>
          <div>
            <Link to={`/final_clone/${url}`}><button className="bg-sky-200  w-full h-full" ></button></Link>
            <label className="text-sky-400 font-semibold text-xl">Dashboard3</label>
          </div>
          <div>
            <Link to={`/final_clone/${url}`}><button className="bg-sky-200  w-full h-full" ></button></Link>
            <label className="text-sky-400 font-semibold text-xl">Dashboard4</label>
          </div>
          <div>
            <Link to={`/final_clone/${url}`}><button className="bg-sky-200 w-full h-full" ></button></Link>
            <label className="text-sky-400 font-semibold text-xl">Dashboard5</label>
          </div>
          <div>
          <Link to={`/final_clone/${url}`}><button className="bg-sky-200 w-full h-full" ></button></Link>
            <label className="text-sky-400 font-semibold text-xl">Dashboard6</label>
          </div>
        </div>
        </div>
      {/* </div> */}
    </body>
    </>
  )
}


export default Dashboards;