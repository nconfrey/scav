import React, { Component } from 'react';
import ReactSpeedometer from 'react-d3-speedometer';
import logo from './logo.svg';
import banner from './banner.jpg';
import './App.css';
import Confetti from 'react-confetti'

class App extends Component {
  constructor() {
    super();
    this.state = {
      value: 100
    }
  }

  getWinnningTeam() {
    if (this.state.value > 50) {
      return "Breck"
    } else {
      return "Other"
    }
  }

  componentDidMount() {
    console.log("throw me a bone", this.state)
    this.value = setInterval(() => this.setState({value: this.state.value + 100}), 1000)
  }

  componentWillUnmount() {
    clearInterval(this.interval)
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={banner} className="App-logo" alt="logo" />
          <h1 className="App-title">Will Breck Scav Win??</h1>
        </header>
        <p className="App-intro">
          Given that is it now blank oclock, we assess our odds to be
        </p>
        <ReactSpeedometer 
          value={this.state.value}
        />
        <div className="Prediction">
        <header>
          <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}>
            <Confetti {...this.props.size} />
          </div>
          <h1>Prediction:</h1>
          <h1>{this.getWinnningTeam()}</h1>
        </header>
        </div>
      </div>

    );
  }
}

export default App;
