from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home():

    return """
    <html>
        <head>
            <title>Andrew Thesis OAuth Login</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 60px;
                    background-color: #f9f9f9;
                }
                .login-btn {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    padding: 12px 24px;
                    margin: 12px;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                    text-decoration: none;
                    color: white;
                    cursor: pointer;
                    width: 250px;
                }
                .google { background-color: #db4437; }
                .facebook { background-color: #3b5998; }
                .github { background-color: #333; }
                .fa-brands { font-size: 20px; }
            </style>
        </head>
        <body>
            <h1>Andrew Thesis OAuth</h1>
            <br>
            <h1>Login with OAuth</h1>

            <a href="/auth/google" class="login-btn google">
                <i class="fab fa-google"></i> Log in with Google
            </a><br>

            <a href="/auth/facebook" class="login-btn facebook">
                <i class="fab fa-facebook-f"></i> Log in with Facebook
            </a><br>

            <a href="/auth/github" class="login-btn github">
                <i class="fab fa-github"></i> Log in with GitHub
            </a>
        </body>
    </html>
    """
