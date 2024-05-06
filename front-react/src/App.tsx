import React, { useCallback } from 'react'

import './App.css'
import SingleFileUploader from './components/SingleFileUploader'
import SingleFileUploader2 from './components/SingleFileUploader2'
//import { Button } from './components/button'
import JsonView from 'react18-json-view'   
import 'react18-json-view/src/style.css'   



const Button =  () => {
  const [data, setData] = React.useState(null);
  const onClick = useCallback( async () => {
    const formData = new FormData();
    const url="http://127.0.0.1:5000/run_from_react";
    try {
      const result = await fetch(url, {
        method: "POST",
        body: formData,
      });
      const data = await result.json();
      console.log(data);
      setData(data);
    } catch (error) {
      console.error(error);
    }
  },[]);
  return (
    <>
      <button onClick={onClick}
        className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded`}
      >
        run workflow
      </button>
      <JsonView src={data} collapsed={false} style={{ height: '450px', overflow: 'scroll' }} theme="a11y"/>
      <button onClick={()=>setData(null)}
        className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded`}>reset</button>
    </>
  );
};


function App() {
  return (
    <>
    <section style={{'backgroundColor':'wheat','borderRadius':'5px','color':'black'}}>
      <h4>Upload document</h4>
      <SingleFileUploader2 />
    </section>
    <section style={{'backgroundColor':'wheat','borderRadius':'5px','color':'black'}}>
      <h4>Upload flow config</h4>
      <SingleFileUploader />
    </section>
    <div style={{'marginTop':'15px'}} >
      <Button />  
    </div>
    </>
  )
}

export default App
