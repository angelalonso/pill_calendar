export const ALERTS_AVAILABLE = 'ALERTS_AVAILABLE';
export const ADD_ALERT = 'ADD_ALERT';
export const UPDATE_ALERT = 'UPDATE_ALERT';
export const DELETE_ALERT = 'DELETE_ALERT';

import {AsyncStorage} from "react-native";


// Add Quote - CREATE (C)
export function addAlert(alertitem){
    return (dispatch) => {
        AsyncStorage.getItem('data', (err, alerts) => {
            if (alerts !== null){
                alerts = JSON.parse(alerts);
                alerts.unshift(alertitem); //add the new quote to the top
                AsyncStorage.setItem('data', JSON.stringify(alerts), () => {
                    dispatch({type: ADD_ALERT, alertitem:alertitem});
                });
            }
        });
    };
}

// Get Data - READ (R)
export function getAlerts(){
    return (dispatch) => {
        AsyncStorage.getItem('data', (err, alerts) => {
            if (alerts !== null){
                dispatch({type: ALERTS_AVAILABLE, alerts:JSON.parse(alerts)});
            }
        });
    };
}

// Update Alert - UPDATE (U)
export function updateAlert(alertitem){
    return (dispatch) => {
        AsyncStorage.getItem('data', (err, alerts) => {
            if (alerts !== null){
                alerts = JSON.parse(alerts);
                var index = getIndex(alerts, alertitem.id); //find the index of the quote with the id passed
                if (index !== -1) {
                    alerts[index]['hour'] = alertitem.hour;
                    alerts[index]['minutes'] = alertitem.minutes;
                    alerts[index]['alertstatus'] = alertitem.alertstatus;
                }
                AsyncStorage.setItem('data', JSON.stringify(alerts), () => {
                    dispatch({type: UPDATE_ALERT, alertitem:alertitem});
                });
            }
        });
    };
}

// Delete Quote - DELETE (D)
export function deleteAlert(id){
    return (dispatch) => {
        AsyncStorage.getItem('data', (err, alerts) => {
            if (alerts !== null){
                alerts = JSON.parse(alerts);

                var index = getIndex(alerts, id); //find the index of the quote with the id passed
                if(index !== -1) alerts.splice(index, 1);//if yes, undo, remove the QUOTE
                AsyncStorage.setItem('data', JSON.stringify(alerts), () => {
                    dispatch({type: DELETE_ALERT, id:id});
                });
            }
        });
    };
}

function getIndex(data, id){
    let clone = JSON.parse(JSON.stringify(data));
    return clone.findIndex((obj) => parseInt(obj.id) === parseInt(id));
}
