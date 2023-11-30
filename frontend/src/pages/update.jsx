import './pages.css'
import { Link, useParams, useLocation} from 'react-router-dom';
//page for finalizing the cloning process along with a couple other fields for the user to fill out

//TODO: when we have a backend, pass information to this page, and render how many times its been changed and cloned
function Update() {

  // let {url} = useParams();
  const {dashboard_name} = useParams();
  const location = useLocation();
  // const {url} = location.state;
  const {superset_url}= location.state;
  const{username}=location.state;


  let superset_dashboard_url = superset_url.superset_url
  let username_redirect = username.username
  console.log(username_redirect)
  console.log(superset_dashboard_url);

  
  return( 
    <>
    <body className="w-full flex h-full flex justify-center">
      <div className="content-wrapper  w-1/2 h-4/5 gap-y-3 flex flex-col justify-center">
        <div className='flex'>
          <Link to={`/dashboards/${username_redirect }`} state={superset_dashboard_url}><button className="bg-sky-400 text-white w-48 h-12">←Previous</button></Link>
        </div>
        <label className="text-sky-400 font-semibold text-3xl h-auto">{dashboard_name}</label>
        <div class="flex justify-center h-full gap-3 gap-y-3">
          <div>
            <label className="text-sky-400 font-semibold text-lg">Dashboard Version History</label>
            <div className="bg-sky-200 w-full h-full"/>
          </div>
          <div>
            <label className="text-sky-400 font-semibold text-lg">List of Changes</label>
            <div className="bg-sky-200 w-full h-4/5"/>
            <div class="flex h-auto gap-y-3 gap-x-3 pt-8 justify-center">
              <Link to={`/dashboards/${username_redirect }`} state={superset_dashboard_url}><button className="bg-sky-400 text-white w-48 h-12">discard changes</button></Link>
              <Link to={`/dashboards/${username_redirect }`} state={superset_dashboard_url}><button className="bg-sky-400 text-white w-48 h-12">propagate changes</button></Link>
            </div>
          </div>
        </div>
      </div>
    </body>
    </>
  )
}


export default Update;