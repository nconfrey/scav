import React, { Component } from 'react';
import ReactSpeedometer from 'react-d3-speedometer';
import logo from './logo.svg';
import './App.css';


class App extends Component {
  _getValue() {
    const startTimestamp = 1525968282000;
    const endTimestamp = 1526223600000;
    const denominator = endTimestamp - startTimestamp;

    const currDate = new Date();
    const currTime = currDate.getTime();
    const numerator = currTime - startTimestamp;

    const percentChanceOfWinningFromNegHundoToHundo = 200 - ((numerator/denominator)*200) - 100;
    return percentChanceOfWinningFromNegHundoToHundo
  }

  constructor() {
    super();
    this.state = {
      value: this._getValue()
    }
  }

  componentDidMount() {
    console.log("throw me a bone", this.state)
    this.value = setInterval(() => this.setState({value: this._getValue()}), 1000)
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
        <div class="container">
          <div class="row">
            <div class="col">
              <span>Snitchcock</span>
            </div>
            <div class="col-6">
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
            <div class="col">
              <span>Breck</span>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
