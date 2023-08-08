import { useEffect, useState } from 'react';
import { IP } from './config.js';

import logo from './logo.svg';
import './App.css';
import './index.css';

function App() {
  
  const [router_id, setRouter_id] = useState('')
  const [ssid2_un, setSsid2_un] = useState('')
  const [ssid2_pw, setSsid2_pw] = useState('')
  const [ssid5_un, setSsid5_un] = useState('')
  const [ssid5_pw, setSsid5_pw] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = {
      router_id: router_id,
      ssid2_un: ssid2_un,
      ssid2_pw: ssid2_pw,
      ssid5_un: ssid5_un,
      ssid5_pw: ssid5_pw
    };
    // console.log(form)
    fetch(IP + '/', {
      method: 'POST',
      headers: { "Authorization": 'Basic',
                "Content-Type": 'application/json',
                "Access-Control-Allow-Origin": 'true'},
      body: JSON.stringify(form),
      mode: "cors",
      credentials: "include"
    }).then(res => {
      console.log(res);
      return res.json();
  }) .then(data => {
    console.log(data)
    })
}
// .then(() => {
//     navigate('/antrag/3')
//   }) 

  return (
  <>  
    <form onSubmit={handleSubmit}>
      <div className="form-control">
        <label className="label">
          <span className="label-text">Router ID</span>
        </label>
        <input placeholder="Name of Router" className="input input-bordered w-full max-w-xs"
          type="text"
          // required
          value={ router_id }
          onChange={(e) => setRouter_id(e.target.value)} 
          />
      </div>
      <div className="form-control">
          <label className="label">
            <span className="label-text">2.4GHz SSID</span>
          </label>
          <input placeholder="2.4GHz SSID" className="input input-bordered w-full max-w-xs"
            type="text"
            // required
            value={ ssid2_un }
            onChange={(e) => setSsid2_un(e.target.value)} 
            />
      </div>
      <div className="form-control">
        <label className="label">
          <span className="label-text">2.4GHz Password</span>
        </label>
        <input placeholder="2.4GHz Password" className="input input-bordered w-full max-w-xs"
          type="text"
          // required
          value={ ssid2_pw }
          onChange={(e) => setSsid2_pw(e.target.value)} 
          />
      </div>
      <div className="form-control">
        <label className="label">
          <span className="label-text">5GHz SSID</span>
        </label>
        <input placeholder="5GHz SSID" className="input input-bordered w-full max-w-xs"
          type="text"
          // required
          value={ ssid5_un }
          onChange={(e) => setSsid5_un(e.target.value)} 
          />
      </div>
      <div className="form-control">
        <label className="label">
          <span className="label-text">5GHz Password</span>
        </label>
        <input placeholder="5GHz Password" className="input input-bordered w-full max-w-xs"
          type="text"
          // required
          value={ ssid5_pw }
          onChange={(e) => setSsid5_pw(e.target.value)} 
          />
      </div>

      <button className="btn btn-primary my-4">DO IT</button>
    </form>
  </>
  );

}

export default App;
