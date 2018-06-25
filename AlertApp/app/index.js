import React, { Component } from 'react';
import { AsyncStorage } from 'react-native';
import { connect } from 'react-redux';
import { Router, Scene } from 'react-native-router-flux';
 
import { getAlarms } from './actions'
import Data from './alarms.json'

import Home from './components/home'
import Config from './components/config'

class Main extends Component {
 
    componentDidMount() {
        var _this = this;
        //Check if any data exist
        AsyncStorage.getItem('data', (err, data) => {
            //if it doesn't exist, extract from json file
            //save the initial data in Async
            if (data === null){
                AsyncStorage.setItem('data', JSON.stringify(Data.alarms));
                _this.props.getAlarms();
            }
        });
    }
 
    render() {
        return (
            <Router>
                <Scene key="root">
                    <Scene key="home" component={Home} title="Home" initial/>
                    <Scene key="config" component={Config} title="Config" />
                </Scene>
            </Router>
        );
    }
}
 
//Connect everything
export default connect(null, { getAlarms })(Main);
