import React, { Component } from 'react';
import ReactSpeedometer from 'react-d3-speedometer';
import logo from './logo.svg';
import './App.css';


class App extends Component {
  constructor() {
    super();
    this.state = {
      value: 100
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
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <ReactSpeedometer 
          value={this.state.value}
          width={600}
          height={400}
          currentValueText={"2018 Scav"}
          startColor={"#7474ea"}
          minValue={-100}
          maxValue={100}
        />
      </div>
    );
  }
}

export default App;
