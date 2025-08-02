# OAuth Benchmark API

A comprehensive FastAPI application for benchmarking and analyzing OAuth 2.0 authentication flows across multiple providers (Google, Facebook, GitHub). This tool measures response times, tracks authentication metrics, and automatically saves results to Google Sheets for analysis.

## Features

### 🔐 Multi-Provider OAuth Support
- **Google OAuth 2.0** - OpenID Connect with offline access
- **Facebook OAuth** - Graph API integration 
- **GitHub OAuth** - User profile and email access

### 📊 Performance Benchmarking
- **Token Exchange Timing** - Measures OAuth token request/response times
- **User Info API Timing** - Tracks user profile retrieval performance
- **Server Latency Tracking** - End-to-end callback processing time
- **Scope Analysis** - Records granted vs requested permissions

### 📈 Data Export & Analysis
- **Google Sheets Integration** - Automatic result logging
- **CSV Export** - Local data storage option
- **Structured Metrics** - Timestamp, error tracking, and performance data

## Architecture

```
app/
├── main.py                 # FastAPI application entry point
├── routes/
│   ├── base.py            # Configuration and OAuth settings
│   └── auth_routes.py     # Authentication endpoints
└── utils/
    └── config.py          # Environment configuration
```

## API Endpoints

### Authentication Flow
- `GET /auth/{provider}` - Initiate OAuth flow for specified provider
- `GET /auth/{provider}/callback` - Handle OAuth callback and collect metrics

### Supported Providers
- `google` - Google OAuth 2.0
- `facebook` - Facebook Login
- `github` - GitHub OAuth

## Configuration

Create a `.env` file in the project root:

```bash
# Application Settings
APP_TITLE=OAuth Benchmark API
APP_VERSION=1.0.0

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REFRESH_TOKEN=your_refresh_token

# Facebook OAuth
FACEBOOK_CLIENT_ID=your_facebook_app_id
FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_facebook_token

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_ACCESS_TOKEN=your_github_token

# Google Sheets Integration
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=your_sheet_name

# Data Export
CSV_FILE=benchmark_results.csv
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd oauth-benchmark-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OAuth applications**
   - Create OAuth apps in Google Cloud Console, Facebook Developers, and GitHub
   - Configure redirect URIs to `http://localhost:8000/auth/{provider}/callback`

4. **Configure Google Sheets** (optional)
   - Download service account credentials as `credentials.json`
   - Create a Google Sheet and share it with the service account email

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## Usage

### Basic OAuth Flow Testing
```bash
# Initiate Google OAuth
curl "http://localhost:8000/auth/google"

# The application will redirect to Google, then back to callback
# Metrics are automatically collected and saved
```

### Benchmark Data Structure
Each OAuth flow generates metrics including:
- `provider` - OAuth provider name
- `token_response_time` - Token exchange duration (seconds)
- `user_info_response_time` - User profile API call duration
- `latency` - Total server processing time
- `token_expires_in` - Token validity period
- `scopes_granted` - Actual permissions received
- `timestamp` - ISO formatted completion time
- `error` - Any error messages encountered

## Technical Details

### OAuth Flow Implementation
- **State Parameter Security** - CSRF protection with secure state generation
- **Session Management** - Temporary session storage for OAuth state
- **Error Handling** - Comprehensive error tracking and logging
- **Async Operations** - Non-blocking HTTP requests with httpx

### Performance Measurement
- **Precision Timing** - Microsecond-level performance tracking
- **API Call Monitoring** - Individual endpoint response time measurement
- **Scope Validation** - Compares requested vs granted permissions

### Data Persistence
- **Multiple Export Options** - Google Sheets and CSV support
- **Structured Schema** - Consistent data format across all providers
- **Real-time Logging** - Immediate result capture and storage

## Development

### Project Structure
The application follows a modular FastAPI architecture with clear separation of concerns for configuration, routing, and utilities.

### Dependencies
- **FastAPI** - Modern Python web framework
- **httpx** - Async HTTP client for OAuth requests
- **python-dotenv** - Environment variable management
- **SQLAlchemy** - Database ORM (if using database storage)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OAuth 2.0 specification and provider documentation
- FastAPI community for excellent async web framework
- Google Sheets API for seamless data integration
