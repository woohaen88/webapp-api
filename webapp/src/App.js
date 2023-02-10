import logo from './logo.svg';
import './App.css';
import {useState} from "react";

function App() {
    let [likecount, setLikecount] = useState(0)
  return (
    <div className="App">
      <div className="black-nav">
        ReactBlog
      </div>

      <div className="list">
        <h1>남자 코트 추천 <span onClick={ () => {setLikecount(likecount+1)} }>👍 {likecount}</span></h1>
        <p>2월 17일 발행</p>
      </div>
    </div>
  );
}

export default App;
