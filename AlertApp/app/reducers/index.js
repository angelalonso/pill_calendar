import { combineReducers } from 'redux';

import { ALERTS_AVAILABLE, ADD_ALERT, UPDATE_ALERT, DELETE_ALERT } from "../actions/" //Import the actions types constant we defined in our actions

let dataState = { alerts: [], loading:true };

const dataReducer = (state = dataState, action) => {
    switch (action.type) {
        case ADD_ALERT:{
            let alerts =  cloneObject(state.alerts) //clone the current state
            alerts.unshift(action.alertitem); //add the new quote to the top
            state = Object.assign({}, state, { alerts: alerts});
            return state;
        }

        case ALERTS_AVAILABLE:
            state = Object.assign({}, state, { alerts: action.alerts, loading:false });
            return state;

        case UPDATE_ALERT:{
            let alertitem = action.alertitem;
            let alerts =  cloneObject(state.alerts) //clone the current state
            let index = getIndex(alerts, alertitem.id); //find the index of the quote with the quote id passed
            if (index !== -1) {
                alerts[index]['hour'] = alertitem.hour;
                alerts[index]['minutes'] = alertitem.minutes;
                alerts[index]['alertstatus'] = alertitem.alertstatus;
            }
            state = Object.assign({}, state, { alerts: alerts});
            return state;
        }

        case DELETE_ALERT:{
            let alerts =  cloneObject(state.alerts) //clone the current state
            let index = getIndex(alerts, action.id); //find the index of the quote with the id passed
            if(index !== -1) alerts.splice(index, 1);//if yes, undo, remove the QUOTE
            state = Object.assign({}, state, { alerts: alerts});
            return state;
        }

        default:
            return state;
    }
};


function cloneObject(object){
    return JSON.parse(JSON.stringify(object));
}

function getIndex(data, id){
    let clone = JSON.parse(JSON.stringify(data));
    return clone.findIndex((obj) => parseInt(obj.id) === parseInt(id));
}

// Combine all the reducers
const rootReducer = combineReducers({
    dataReducer
})

export default rootReducer;
