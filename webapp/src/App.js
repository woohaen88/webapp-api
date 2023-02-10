import './App.css';

import {useState} from "react";

import data from "./data"

import "bootstrap/dist/css/bootstrap.min.css"
import Navbar from "./components/Navbar";
import Card from "./components/Card";


function App() {
  let [shoes] = useState(data);
  return (
          <div className="App">
            {/* NavBar Start */}
            <Navbar/>
            {/* NavBar End */}

            {/* Container Start */}
            <div className="container">
              <div className="row">
                {/* Item Start */}
                {
                  shoes.map(function (v, i) {
                    return (
                            <Card item={v} key={i}/>
                    )
                  })
                }
                {/* Item end */}
              </div>
            </div>
            {/* Container End */}
          </div>
  );
}

export default App;
