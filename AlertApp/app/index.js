import React, {Component} from 'react';                                                                                                                                                               
import { View, AsyncStorage } from 'react-native';
 
import { Router, Scene } from 'react-native-router-flux';
 
import Home from './components/home'
import NewAlert from './components/new_alert'
 
import Data from './alerts.json'
 
import {connect} from 'react-redux';
import { getAlerts } from './actions'
 
class Main extends Component {
 
    componentDidMount() {
        var _this = this;
        //Check if any data exist
        AsyncStorage.getItem('data', (err, data) => {
            //if it doesn't exist, extract from json file
            //save the initial data in Async
            if (data === null){
                AsyncStorage.setItem('data', JSON.stringify(Data.alerts));
                _this.props.getAlerts();
            }
        });
    }
 
    render() {
        return (
            <Router>
                <Scene key="root">
                    <Scene key="home" component={Home} title="Home" initial/>
                    <Scene key="new_alert" component={NewAlert} title="New Alert"/>
                </Scene>
            </Router>
        );
    }
}
 
//Connect everything
export default connect(null, { getAlerts })(Main);
