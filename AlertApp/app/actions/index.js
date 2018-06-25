export const ALARMS_AVAILABLE = 'ALARMS_AVAILABLE';  
export const UPDATE_ALARM = 'UPDATE_ALARM';


import {AsyncStorage} from "react-native";                                                                                                                                                            
 
export function getAlarms(){
    return (dispatch) => {
        AsyncStorage.getItem('data', (err, alarms) => {
            if (alarms !== null){
                dispatch({type: ALARMS_AVAILABLE, alarms:JSON.parse(alarms)});
            }
        });
    };
}

 
export function updateAlarm(alarm){
    return (dispatch) => {
        AsyncStorage.getItem('data', (err, alarms) => {
            if (alarms !== null){
                alarms = JSON.parse(alarms);
                var index = getIndex(alarms, alarm.id); //find the index of the quote with the id passed
                if (index !== -1) {
                    alarms[index]['hour'] = alarm.hour;
                    alarms[index]['minutes'] = alarm.minutes;
                    alarms[index]['alertstatus'] = alarm.alertstatus;
                }
                AsyncStorage.setItem('data', JSON.stringify(alarms), () => {
                    dispatch({type: UPDATE_ALARM, alarm:alarm});
                });
            }
        });
    };
}

 
function getIndex(data, id){
    let clone = JSON.parse(JSON.stringify(data));
    return clone.findIndex((obj) => parseInt(obj.id) === parseInt(id));
}       
 

