import { connect } from "react-redux";
import { login, logoff } from "../../redux/action";

const mapStateToProps = (state) => ({ isLogin: state.isLogin, userData: state.userData });
const mapDispatchToProps = (dispatch) => ({
    login: (userData) => dispatch(login(userData)),
    logoff: () => dispatch(logoff()),
});

export default function Container(wrappedComponent) {
    return connect(mapStateToProps, mapDispatchToProps)(wrappedComponent);
}
