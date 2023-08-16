import { useState } from 'react';
import { IP } from './config.js';

import AesirLogo from './AesirLogo.png';
import './App.css';
import './index.css';

function App() {
  
  const [router_id, setRouter_id] = useState('')
  const [ssid24, setSsid24] = useState('')
  const [ssid58, setSsid58] = useState('')
  const [wpa_pass, setWpa_pass] = useState('')
  const [wpa2_pass, setWpa2_pass] = useState('')

  const [output, setOutput] = useState('')

  function handleChange(evt) {
    const value = evt.target.value;
    setOutput(value);
  }
  function handleReset() {
    const value = '';
    setOutput(value);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = {
      router_id: router_id,
      ssid24: ssid24,
      ssid58: ssid58,
      wpa_pass: wpa_pass,
      wpa2_pass: wpa2_pass
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
    }).then(data => {
      console.log(data)
      if ('error' in data) {
        alert(data['error'])
      } else {
        setOutput(data[1]);
        setRouter_id('');
        setSsid24('');
        setSsid58('');
        setWpa_pass('');
        setWpa2_pass('');
      }
    })
}

  return (
  <>
    <div className="App-header">
      <div className="navbar shadow-2xl bg-base-200 roundedborders">
        <div className="flex-1">
          {/* <Link to="/home"> */}
            <img src={ AesirLogo } className="App-logo" alt="logo" />
            <h1 className='ml-5'>hermóðr</h1>
          {/* </Link> */}
        </div>
      </div>
    </div>

    <div className="flow-root">
      <div className="float-left">
        <form onSubmit={handleSubmit}>
          <div className="form-control ml-5">
            <label className="label">
              <span className="label-text">Router ID</span>
            </label>
            <input placeholder="Name of Router" className="input input-bordered w-full max-w-xs"
              type="text"
              required
              value={ router_id }
              onChange={(e) => setRouter_id(e.target.value)} 
              />
          </div>
          <div className="form-control ml-5">
              <label className="label">
                <span className="label-text">2.4GHz SSID</span>
              </label>
              <input placeholder="2.4GHz SSID" className="input input-bordered w-full max-w-xs"
                type="text"
                // required
                value={ ssid24 }
                onChange={(e) => setSsid24(e.target.value)} 
                />
          </div>
          <div className="form-control ml-5">
            <label className="label">
              <span className="label-text">5.8GHz SSID</span>
            </label>
            <input placeholder="5.8GHz SSID" className="input input-bordered w-full max-w-xs"
              type="text"
              // required
              value={ ssid58 }
              onChange={(e) => setSsid58(e.target.value)} 
              />
          </div>
          <div className="form-control ml-5">
            <label className="label">
              <span className="label-text">WPA Preshared Key</span>
            </label>
            <input placeholder="WPA Preshared Key" className="input input-bordered w-full max-w-xs"
              type="text"
              // required
              pattern="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
              value={ wpa_pass }
              onChange={(e) => setWpa_pass(e.target.value)} 
              />
          </div>
          <div className="form-control ml-5">
            <label className="label">
              <span className="label-text">WPA2 Preshared Key</span>
            </label>
            <input placeholder="WPA2 Preshared Key" className="input input-bordered w-full max-w-xs"
              type="text"
              // required
              pattern="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"            
              value={ wpa2_pass }
              onChange={(e) => setWpa2_pass(e.target.value)} 
              />
          </div>

          <button className="btn btn-primary my-4 ml-5">DO IT</button>
        </form>
        </div>
        
        <div className="float-right border m-5">
          <textarea name="outputtext" cols="150" rows="20" value={output} onChange={handleChange}></textarea>
        </div>
    </div>

    <div className='float-right mx-5'>
      <button className="btn btn-primary my-4 ml-5" onClick={handleReset}>Clear</button>
    </div>
  </>
  );

}

export default App;
