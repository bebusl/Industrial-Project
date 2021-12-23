import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import AccountCircle from "@mui/icons-material/AccountCircle";
import Switch from "@mui/material/Switch";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import LockOpenIcon from "@mui/icons-material/LockOpen";
import axios from "axios";
axios.defaults.withCredentials = true;
export default function MenuAppBar() {
    const navigate = useNavigate();
    // useEffect(() => {
    //     async function get_auth() {
    //         await axios
    //             .get("http://localhost:5000/auth/status")
    //             .then((res) => setAuth(true))
    //             .catch((e) => {
    //                 console.log(e);
    //                 if (e.response.status === 404) {
    //                     setAuth(false);
    //                 }
    //             });
    //     }
    //     get_auth();
    // });
    const onClick = (e) => {
        e.preventDefault();
        axios
            .get("http://localhost:5000/auth/status")
            .then((res) => {
                console.log(res);
                navigate("/mypage");
            })
            .catch((e) => navigate("/login"));
    };
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{ flexGrow: 1 }}
                        onClick={(e) => {
                            e.preventDefault();
                            navigate("/");
                        }}
                        style={{ cursor: "pointer" }}
                    >
                        키북키북
                    </Typography>
                    {
                        <div>
                            <IconButton size="large" onClick={onClick}>
                                <LockOpenIcon />
                            </IconButton>
                        </div>
                    }
                </Toolbar>
            </AppBar>
        </Box>
    );
}
