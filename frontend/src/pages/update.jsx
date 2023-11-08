import './pages.css'
import { Link, useParams } from 'react-router-dom';
//page for finalizing the cloning process along with a couple other fields for the user to fill out

//TODO: when we have a backend, pass information to this page, and render how many times its been changed and cloned
function Update() {

  let {url} = useParams();

  
  return( 
    <>
    <body className="w-full flex h-full flex justify-center">
      <div className="content-wrapper  w-1/2 h-1/2 gap-y-28 flex flex-col justify-center">
        <div class="h-56 grid grid-cols-3 gap-y-25 content-center">
          <Link to={`/dashboards/${url}`}><button className="bg-sky-400 w-48 h-12">←Previous</button></Link>
          <Link to={`/dashboards/${url}`}><button className="bg-sky-400 w-48 h-12">discard changes</button></Link>
          <Link to={`/dashboards/${url}`}><button className="bg-sky-400 w-48 h-12">propagate changes</button></Link>
        </div>
        <div class="h-56 grid grid-cols-2 gap-y-3 content-center">
          <div>
            <div className="bg-sky-200 w-80 h-96"/>
            <label className="text-sky-400 font-semibold text-2xl">Newest Version</label>
          </div>
          <div>
            <div className="bg-sky-200 w-80 h-96"/>
            <label className="text-sky-400 font-semibold text-2xl">Current Version</label>
          </div>
        </div>
        <div class="h-56 grid grid-cols-1 content-center">
          <label className="text-sky-400 font-semibold text-2xl">————————————————————————————</label>
          <label className="text-sky-400 font-semibold text-md">Info: Dashboard changed __ times, cloned by __ users.</label>
        </div>
      </div>
    </body>
    </>
  )
}


export default Update;