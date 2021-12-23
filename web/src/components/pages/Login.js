import { Box, Button, Paper, TextField, Link } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useInput } from "../../utils/hooks";
import axios from "axios";
export default function LoginForm() {
    const { values, onChange } = useInput({ email: "", password: "" });
    const navigate = useNavigate();

    function onClick(e) {
        e.preventDefault();
        async function login() {
            const res = await axios.post(
                "http://localhost:5000/auth/login",
                {
                    id: values.email,
                    password: values.password,
                },
                { withCredentials: true }
            );

            if (res.data.success === true) {
                console.log(res);
                navigate("/mypage");
            } else {
                window.alert("로그인 실패");
            }
        }
        login();
    }
    return (
        <Box sx={{ mx: "auto", width: 400 }}>
            <Paper>
                <Box
                    sx={{
                        display: "grid",
                        gap: 2,
                        mt: 1,
                        p: 3,
                        gridTemplateColumns: "repeat(1, 1fr)",
                    }}
                >
                    <TextField label="Username/Email" autoFocus name="email" value={values.email} onChange={onChange} />
                    <TextField
                        label="Password"
                        type="password"
                        name="password"
                        value={values.password}
                        onChange={onChange}
                    />
                    <Box sx={{ display: "flex", gap: 2, flexDirection: "row-reverse" }}>
                        <Button variant="contained" color="primary" onClick={onClick}>
                            Login
                        </Button>
                        <Link
                            href="#"
                            onClick={(event) => {
                                event.preventDefault();
                                navigate("/");
                            }}
                        >
                            Forgot password?
                        </Link>
                    </Box>
                </Box>
            </Paper>
        </Box>
    );
}
