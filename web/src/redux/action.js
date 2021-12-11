export const LOGIN = "LOGIN",
    LOGOFF = "LOGOFF",
    UPDATE_USERDATA = "UPDATE_USERDATA",
    UPDATE_LIKEKEYWORD = "UPDATE_LIKEKEYWORD",
    UPDATE_HATEKEYWORD = "UPDATE_HATEKEYWORD",
    SETSEARCHITEM = "SETSEARCHITEM",
    SETPRODUCTLIST = "SETPRODUCTLIST";

export const login = (userData) => {
    return {
        type: LOGIN,
        userData,
    };
};

export const logoff = () => {
    return { type: LOGOFF };
};

export const updateUserdata = (userData) => {
    return {
        type: UPDATE_USERDATA,
        userData,
    };
};

export const updateLikeKeyword = (keywords) => {
    return {
        type: UPDATE_LIKEKEYWORD,
        keywords,
    };
};

export const updateHateKeyword = (keywords) => {
    return {
        type: UPDATE_HATEKEYWORD,
        keywords,
    };
};

export const setSearchItem = (searchItem) => {
    return {
        type: SETSEARCHITEM,
        searchItem,
    };
};

export const setProductlist = (productlists) => {
    return {
        type: SETPRODUCTLIST,
        productlists,
    };
};
