import React, { Component } from 'react';
import Cards, { Card } from 'react-swipe-card'
import axios from 'axios';

import request from 'request'
import './App.css';

var	done =false
var	keys  = []
var	team= {}
const data = ['Alexandre', 'Thomas', 'Lucien']
 
const Wrapper = () => {
  return (
      <Cards onEnd={action('end')} className='master-root'>
        {data.map((item,idx) =>
          <Card 
            onSwipeLeft={sdf('dis',idx)}
            onSwipeRight={sdf('apv',idx)}
			key={idx}
			>
            <h2>{item}</h2>
          </Card>
        )}
      </Cards>
  )
}
var sdf = function(ty,n){
	var num = n
	if (ty=='dis'){
	return function(){
		console.log("HEH"+num)
	}
	}
	else{
	return function(){
		console.log("APPROVED"+num)
	}
	}

}
const action = console.log

class App extends Component {
	constructor(props){
		super(props);
		this.state={
			team: {},
			keys: [],
		}
		this.name = window.location.pathname.split('/').pop()
	}
	componentDidMount() {
		console.log(this.name)
		var addr = 'http://'+window.location.hostname+":5000/"
		addr = addr+'?team='+this.name
		console.log("making request to "+addr)
		axios.get(addr)
			.then(res => {
				console.log(res)
				keys = Object.keys(res.data)
				team = res.data
				this.setState({team, keys});
			}).catch(alert);
	}
	render() {
    return (
      <div className="App">
        <header className="App-header">
			<h1 className="App-title">Team Up!</h1>
		</header>
		<div>
			<h3>{this.name}</h3>
			<h3>{this.state.keys}</h3>
			{this.state.keys.map((k,i)=>{
				if (team[k].length>0){
					return(
				 <Cards key={i} onEnd={action('end')} className='member'>
				 {team[k].map((item,idx) =>
				 <Card 
				 onSwipeLeft={sdf('dis',idx)}
				 onSwipeRight={sdf('apv',idx)}
				 key={idx}
				 >
				 <p className='job'>{k} {item.f.toFixed(2)}</p>
				 <p>З/п: {item.payment}</p>
				 <p className="desc">{item.dop}</p>
				 <p>Количество работ: {item.work_history.length}</p>
				 <p>возраст: {item.age}</p>
				 <p>Опыт в месяцах: {item.experience_month_total}</p>
				 </Card>
						 )}
				 </Cards>
				)
				}
				else{
					return(
							<p>{k} не найден</p>
						  )
				}
									  }
				)
			}
		</div>
		</div>
    );
		
  }
}

export default App;
