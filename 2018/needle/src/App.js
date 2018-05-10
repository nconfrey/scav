import React, { Component } from 'react';
import ReactSpeedometer from 'react-d3-speedometer';
import logo from './logo.svg';
import banner from './banner.jpg';
import './App.css';
import Confetti from 'react-confetti'

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
      value: this._getValue(),
      sign: 1
    }
  }

  getWinnningTeam() {
    if (this.state.value > 10) {
      return "Breck"
    } else if (this.state.value >= -10 || this.state.value <= 10) {
      return "Toss Up"
    } 
    else {
      return "Snitchcock"
    }
  }

  componentDidMount() {
    this.value = setInterval(() => this.setState({value: this._getValue() + (0.5*this.state.sign), sign: this.state.sign*-1}), 1000)
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
          We assess our odds to be
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
              {this.state.value > 80 && <Confetti {...this.props.size} />}
              <span>Breck</span>
            </div>
          </div>
        </div>
        <div className="Prediction">
        <header>
          <h1>Prediction:</h1>
          <h1>{Math.round(Math.abs(this.state.value)) + "% " + this.getWinnningTeam()}</h1>
        </header>
        </div>
      </div>

    );
  }
}

export default App;
