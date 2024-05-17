const initialState = {
    userName: ''
};
  
export const setUserName = (name) => ({
    type: 'SET_USER_NAME',
    payload: name
});
  
const authReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_USER_NAME':
            return {
                ...state,
                userName: action.payload
            };
        default:
            return state;
    }
};
  
export default authReducer;

