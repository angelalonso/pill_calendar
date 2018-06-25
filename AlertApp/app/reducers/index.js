import { combineReducers } from 'redux';

import { ALARMS_AVAILABLE } from "../actions/" //Import the actions types constant we defined in our actions    

let dataState = { alarms: [], loading:true };

const dataReducer = (state = dataState, action) => {
    switch (action.type) {
        case ALARMS_AVAILABLE:
            state = Object.assign({}, state, { alarms: action.alarms, loading:false });
            return state;

        default:
            return state;
    }
};

// Combine all the reducers
const rootReducer = combineReducers({
    dataReducer
})

export default rootReducer;
