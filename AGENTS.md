# AGENTS.md - py-iec-api Project Knowledge Base

## Project Overview

**py-iec-api** is a Python async wrapper library for the Israel Electric Company (IEC) API. It provides programmatic access to customer data, contracts, meter readings, invoices, and other utility-related information from the IEC.

**Repository**: https://github.com/GuyKh/py-iec-api  
**Language**: Python 3.10+  
**Build System**: Poetry  
**Testing**: pytest with 100% coverage requirement  
**Linting**: Ruff (line-length: 120, selected rules: E, F, W, I, N)

---

## Architecture Overview

### Dependency Map

```
iec_client (Main facade)
├── login (OKTA authentication)
├── data (API endpoints & models)
├── masa_data (MASA API integration)
├── static_data (Static reference data)
├── fault_portal_data (Fault portal integration)
├── commons (Utilities & helpers)
└── models/ (Data classes)
    ├── exceptions
    ├── contracts, invoices, devices
    ├── jwt, account, customer
    └── masa_api_models/, fault_portal_models/
```

### Core Modules

| Module | Purpose | Key Exports |
|--------|---------|------------|
| **iec_client.py** | Main async client for IEC API | `IecClient` class with all public methods |
| **login.py** | OKTA-based authentication flow | Authorization, session tokens, OTP handling |
| **data.py** | API endpoint definitions & response parsing | Constants for all IEC endpoints |
| **commons.py** | HTTP utilities, validation, logging | `send_json_post_request`, `is_valid_israeli_id` |
| **const.py** | Configuration constants | Base URLs, timeouts, default values |
| **models/exceptions.py** | Exception hierarchy | `IECError`, `IECLoginError` |

---

## Module-by-Module Breakdown

### `iec_api/iec_client.py` - Main Client Interface

**Responsibility**: Central facade for all IEC API operations.

**Key Class**: `IecClient`
- **Constructor**: `__init__(user_id: str|int, session: Optional[ClientSession] = None)`
  - Validates Israeli ID format
  - Initializes aiohttp session with debug tracing
  - Manages session lifecycle with `atexit`

**State Management**:
- `_state_token`: Session state token
- `_factor_id`: Multi-factor auth identifier
- `_session_token`: Current session token
- `_otp_factor_type`: OTP delivery method (sms/email)
- `_token`: JWT (access, refresh, id tokens)
- `logged_in`: Boolean login state
- `_bp_number`, `_contract_id`, `_account_id`: Customer identifiers

**Key Methods** (by category):

**Authentication**:
- `async manual_login()` - Interactive login flow
- `async login_with_otp(otp_code: str, remember: bool = False)` - OTP submission
- `async login_with_file(file_path: str)` - Load credentials from file
- `_refresh_token()` - Token refresh logic

**Customer Data**:
- `async get_customer() -> Optional[Customer]` - Get customer profile
- `async get_contracts() -> List[Contract]` - Get all contracts
- `async get_account(bp_number: str) -> Account` - Get account details

**Meter & Reading Data**:
- `async get_last_meter_reading(bp_number, contract_id) -> MeterReadings` - Last meter reading
- `async get_meter_readings(bp_number, contract_id, resolution, start_date, end_date)` - Historical readings
- `async get_remote_reading(bp_number, contract_id) -> RemoteReadingResponse` - Remote reading request

**Bills & Invoices**:
- `async get_electric_bills(bp_number) -> List[ElectricBill]` - Get bills
- `async get_invoices(bp_number, get_invoices_body) -> List[Invoice]` - Get invoices
- `async send_consumption_to_mail(bp_number, contract_id, email)` - Email consumption data

**Device Management**:
- `async get_devices() -> List[Device]` - Get customer devices
- `async get_device_details(device_id) -> DeviceDetails` - Device info
- `async get_device_in(device_type) -> DeviceInResponse` - Device input data

**System Status**:
- `async get_outages() -> List[Outage]` - Planned outages
- `async check_contract(contract_id) -> ContractCheck` - Validate contract
- `async get_service_status(service_type) -> dict` - Service status

**MASA Integration** (property management):
- `async get_masa_user_profile()` - Property owner profile
- `async get_masa_cities() -> List[City]` - Available cities
- `async get_masa_lookup()` - Lookup reference data
- `async get_masa_titles() -> List[GetTitleResponse]` - Property titles
- `async get_masa_equipment() -> GetEquipmentResponse` - Equipment data

**Fault Portal**:
- `async get_fault_portal_outages() -> List[FaultPortalOutage]` - Outages
- `async get_fault_portal_user_profile() -> UserProfile` - User profile

**Utilities**:
- `async check_social_discount(bp_number) -> SocialDiscount` - Discount eligibility
- `get_usage_calculator(bp_number, contract_id) -> UsageCalculator` - Usage calculator
- `async _shutdown()` - Session cleanup

---

### `iec_api/login.py` - Authentication

**Responsibility**: OKTA-based OAuth2 + Multi-factor authentication flow.

**Constants**:
```python
APP_CLIENT_ID = "0oaqf6zr7yEcQZqqt2p7"
CODE_CHALLENGE_METHOD = "S256"
APP_REDIRECT_URI = "com.iecrn:/"
IEC_OKTA_BASE_URL = "https://iec-ext.okta.com"
```

**Key Functions**:
- `async authorize_session(session, session_token) -> str` - Get authorization code
- `async get_token(session, code, state) -> JWT` - Exchange code for tokens
- `async authenticate(session, user_id, password, **kwargs) -> Tuple[session_token, factor_id, otp_factor_type]` - Primary authentication
- `async verify_otp(session, state_token, factor_id, otp_code) -> Tuple[session_token, success]` - OTP verification
- `async get_id_token_from_session_token(session, session_token) -> str` - Session token to ID token

**PKCE Flow**:
- Generates code verifier/challenge for OAuth2 security
- Uses S256 (SHA-256) challenge method
- Automatically includes in authorization requests

---

### `iec_api/data.py` - API Endpoints & Data Classes

**Responsibility**: Centralized endpoint definitions and API response parsing.

**API Endpoint Groups**:

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/api/customer` | Get customer profile | GET |
| `/api/consumerdetails` | Get account details | GET |
| `/api/contracts` | Get contracts list | GET |
| `/api/remotereading` | Request remote reading | POST |
| `/api/meterreadings` | Get historical readings | POST |
| `/api/invoices` | Get invoices | POST |
| `/api/bills` | Get electric bills | GET |
| `/api/devices` | Get devices | GET |
| `/api/devices/{device_id}` | Get device details | GET |
| `/api/checkcontract` | Validate contract | POST |
| `/api/servicestatus` | Get service status | POST |
| `/api/outages` | Get planned outages | GET |
| `/api/socialdiscount/check` | Check discount eligibility | GET |

**Response Model Imports**:
- `Customer`, `Contract`, `Account` - Core customer data
- `MeterReadings`, `RemoteReadingResponse` - Meter data
- `ElectricBill`, `Invoice` - Billing data
- `Device`, `Devices` - Device info
- `Outage`, `ContractCheck` - System status
- `SocialDiscount`, `TouzCompatibility`, `EfsMessage` - Utilities

---

### `iec_api/commons.py` - Shared Utilities

**Responsibility**: HTTP handling, validation, logging, and common utilities.

**Key Functions**:

**HTTP Helpers**:
- `async send_json_post_request(session, url, json_data, **kwargs)` - POST with JSON body
- `async send_json_get_request(session, url, **kwargs)` - GET with JSON support
- `async send_non_json_get_request(session, url, encoding, **kwargs)` - GET with custom encoding
- `async check_response_for_errors(response)` - Parse IEC error responses

**Validation**:
- `is_valid_israeli_id(user_id: str|int) -> bool` - Validate Israeli ID format
- `get_bp_number(response_dict)` - Extract BP number from response
- `get_contract_id(response_dict)` - Extract contract ID from response

**Logging** (aiohttp trace callbacks):
- `on_request_start_debug(session, context, params)` - Log request start
- `on_request_chunk_sent_debug(session, context, params)` - Log request body
- `on_request_end_debug(session, context, params)` - Log response

**Other**:
- `get_local_date(dt: datetime) -> str` - Format datetime for API
- `read_json_file(file_path)` - Load JSON file

---

### `iec_api/models/` - Data Classes

**Subdirectories**:
- `models/` - IEC API models
- `masa_api_models/` - MASA (property management) API models
- `fault_portal_models/` - Fault portal API models
- `usage_calculator/` - Usage calculation logic

### Model Structure Nuances (Implementation Rules)

**Folder placement by endpoint family**:
- IEC endpoints (`https://iecapi.iec.co.il/api/...`) -> `iec_api/models/`
- MASA endpoints (`https://masa-mainportalapi.iec.co.il/api/...`, `https://masaapi-wa.azurewebsites.net/...`) -> `iec_api/masa_api_models/`
- Fault portal endpoints -> `iec_api/fault_portal_models/`

**File structure by endpoint**:
- Prefer one file per endpoint/request-response shape in MASA and Fault Portal models.
- Use endpoint-oriented names, e.g.:
  - `manage_shared_accounts.py`
  - `remove_contact_from_shared_account.py`
  - `send_shared_account_invitation.py`
- Avoid collecting unrelated request/response models in a single generic file.

**Dataclass + mashumaro conventions**:
- Use `@dataclass` with `DataClassDictMixin`.
- Map API fields with `field_options(alias="...")` when Python names differ.
- For request models that must serialize API keys exactly (e.g. `Id`, `primaryContact`), use:
  - `class Config(BaseConfig): serialize_by_alias = True`
- Keep model fields minimal and typed; avoid speculative fields.

**Sanitization and privacy rules**:
- Strip/normalize IDs and tokens in `__post_init__` (for example: `value.strip()`).
- Do not include private/personally identifying fields in model classes unless required by behavior.
- If API response includes private fields (name/government ID/phone/email), model only required non-sensitive fields by default.

**Required endpoint comment examples in model files**:
- Each new model file should include a top comment block with:
  - HTTP method
  - Full endpoint URL with placeholders
  - Request example (if applicable)
  - Response example
- Example data must be sanitized (placeholder UUIDs, masked/synthetic values, no real personal data).
- Match the existing repository style used in other model files (plain `#` comment blocks above classes).

**Core Models** (using `mashumaro` for JSON serialization):

| Model | Purpose |
|-------|---------|
| `Customer` | Customer profile (name, contact, account status) |
| `Contract` | Customer contract (ID, status, address, device info) |
| `Account` | Account details (balance, consumption, discounts) |
| `MeterReadings` | Historical meter readings with resolution (hourly/daily/monthly) |
| `RemoteReadingResponse` | Remote meter reading request response |
| `ElectricBill` | Electric bill record with consumption & cost |
| `Invoice` | Invoice document with payment details |
| `Device` | Smart meter device info |
| `DeviceDetails` | Device configuration and state |
| `Outage` | Planned outage event |
| `ContractCheck` | Contract validation result |
| `SocialDiscount` | Social discount eligibility |
| `TouzCompatibility` | Touz (property registry) compatibility |
| `EfsMessage` | EFS system messages |
| `JWT` | OAuth2 JWT token container |

**Exception Hierarchy**:
```
Exception
├── IECError(code, error) - Base IEC exception
└── IECLoginError(code, error) - Login-specific error
```

---

### `iec_api/const.py` - Configuration

**Key Constants**:
```python
# Base URLs
BASE_URL: API base endpoint
OKTA_BASE_URL: OKTA authentication endpoint
MASA_API_BASE_URL: Property management API
FAULT_PORTAL_BASE_URL: Fault portal API

# Timeouts
DEFAULT_TIMEOUT: Request timeout (seconds)

# Default Values
DEFAULT_RESOLUTION: Meter reading resolution (hourly/daily)
```

---

### `iec_api/masa_data.py` - MASA API Integration

**Responsibility**: Property management (MASA) API operations.

**Base URL**: `https://iec-public-api.iec.co.il/masa-public`

**Endpoints**:
- `GET /user-profile` - Get property owner profile
- `GET /cities` - Get available cities list
- `GET /lookup?entity=X` - Get reference data
- `GET /titles` - Get property titles
- `GET /equipment` - Get equipment data
- `GET /voltage-levels` - Get voltage levels

**Models Used**:
- `MasaUserProfile`, `City`, `VoltLevel`, `GetTitleResponse`, `GetEquipmentResponse`, `GetLookupResponse`

---

### `iec_api/fault_portal_data.py` - Fault Portal Integration

**Responsibility**: Outage and fault information.

**Base URL**: `https://www.ernaot.co.il/api`

**Endpoints**:
- `GET /outages` - Get planned outages
- `GET /user-profile/{user_id}` - Get user profile

**Models Used**:
- `FaultPortalOutage`, `UserProfile`

---

### `iec_api/usage_calculator/calculator.py` - Usage Calculation

**Responsibility**: Calculate consumption patterns from meter readings.

**Class**: `UsageCalculator`
- Aggregates meter readings by time period
- Calculates average consumption
- Generates usage statistics

---

## Data Flow Diagrams

### Login Flow
```
manual_login()
  ↓
authenticate(user_id, password)
  ↓ [OKTA API]
session_token + factor_id + otp_factor_type
  ↓
login_with_otp(otp_code)
  ↓
verify_otp(session_token, factor_id, otp_code)
  ↓ [OKTA API]
new session_token
  ↓
authorize_session(session_token)
  ↓ [OAuth2]
authorization_code
  ↓
get_token(authorization_code)
  ↓ [OKTA Token Endpoint]
JWT (access_token, refresh_token, id_token)
  ↓
logged_in = True
```

### Customer Data Flow
```
IecClient.get_customer()
  ↓
commons.send_json_get_request("/api/customer")
  ↓ [HTTP GET with JWT auth header]
IEC API
  ↓
JSON response
  ↓
commons.check_response_for_errors()
  ↓
mashumaro.from_dict(Customer)
  ↓
Customer object
```

---

## Testing Structure

**Test Directory**: `/tests/`
- `commons_test.py` - Tests for utility functions
- `e2e_test.py` - End-to-end integration tests

**Coverage Requirements**:
- **Minimum**: 100% branch coverage
- **Exclusions**: Tests, example.py
- **Tool**: pytest-cov

**Running Tests**:
```bash
pytest tests/
pytest --cov=iec_api --cov-report=html tests/
```

---

## Key Design Patterns

### 1. **Async-First Architecture**
- All I/O operations are `async`
- aiohttp for HTTP requests
- Enables concurrent operations with `asyncio.gather()`

### 2. **Session Lifecycle Management**
- Single `ClientSession` per `IecClient`
- Auto-cleanup via `atexit` handler
- Optional session injection for connection pooling

### 3. **State Token Management**
- Multi-token system: state, session, OTP factor, JWT
- Separate refresh token handling
- Automatic token expiration/refresh logic

### 4. **Error Handling Strategy**
- Custom exception hierarchy (`IECError`, `IECLoginError`)
- Centralized error parsing in `commons.check_response_for_errors()`
- HTTP status code mapping to domain exceptions

### 5. **Data Model Separation**
- Three API models directories: IEC, MASA, Fault Portal
- Mashumaro for automatic JSON serialization/deserialization
- Type-safe model inheritance

### 6. **Request Logging**
- aiohttp TraceConfig callbacks
- Debug-level logging of requests/responses
- Helpful for troubleshooting API integration

---

## Common Workflows

### 1. **Authenticate and Get Customer Data**
```python
client = IecClient("123456789")
await client.manual_login()  # Interactive login
customer = await client.get_customer()
contracts = await client.get_contracts()
```

### 2. **Get Meter Readings**
```python
readings = await client.get_meter_readings(
    bp_number=customer.bp_number,
    contract_id=contracts[0].contract_id,
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 1, 31),
    resolution=ReadingResolution.DAILY
)
```

### 3. **Get Invoices**
```python
body = GetInvoicesBody(...)
invoices = await client.get_invoices(bp_number, body)
```

### 4. **Check Social Discount**
```python
discount = await client.check_social_discount(bp_number)
if discount.eligible:
    # Apply discount logic
```

### 5. **Get Property Management Data (MASA)**
```python
user_profile = await client.get_masa_user_profile()
cities = await client.get_masa_cities()
equipment = await client.get_masa_equipment()
```

---

## Dependencies

**Core**:
- `aiohttp` - Async HTTP client
- `aiofiles` - Async file I/O
- `PyJWT` - JWT token parsing
- `pkce` - OAuth2 PKCE code generation
- `mashumaro` - JSON serialization
- `pytz` - Timezone handling
- `requests` - Sync HTTP fallback

**Development**:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `ruff` - Linting & formatting
- `pre-commit` - Git hooks

---

## Notes for Future Maintenance

1. **Token Refresh**: Check `_refresh_token()` implementation for edge cases during long-running operations
2. **OKTA Endpoints**: OKTA configuration is hardcoded (APP_CLIENT_ID, IEC_OKTA_BASE_URL) - monitor for changes
3. **API Stability**: IEC API endpoints may change - monitor error responses for deprecation notices
4. **MASA Integration**: Property management API has separate base URL - consider factoring if additional integrations added
5. **Logging**: Debug traces can be verbose - consider environment-based log level control
6. **Type Safety**: All models use mashumaro - ensure type hints are accurate for client SDK generation

---

## Project Standards

**Code Style**:
- Python 3.10+ type hints required
- Line length: 120 characters
- Linting: E, F, W, I, N rules (Ruff)
- Async/await preferred for I/O

**Testing**:
- 100% branch coverage required
- Unit tests for utilities
- E2E tests for full workflows

**Documentation**:
- Docstrings on all public methods
- Type hints on all parameters/returns
- Comments for complex logic
- New endpoint model files must include method/URL/request/response comment examples with sanitized data

**Tooling and Workflow Standards**:
- Use `ruff` for linting and import ordering; fix `I001` and style issues before committing.
- Validate model parsing/serialization behavior with focused pytest cases under `tests/`.
- When adding endpoints, update all required layers together:
  1. `const.py` (URL constant)
  2. model file(s)
  3. `data.py` method
  4. `iec_client.py` facade method
  5. tests
- Keep changes surgical: avoid unrelated refactors in endpoint/model PRs.

**Git**:
- Pre-commit hooks enabled
- Atomic, meaningful commits
- Branch protection on main

## PR Checklist

Use this checklist before opening or merging a PR (especially endpoint/model work):

- [ ] Endpoint constants added/updated in `iec_api/const.py`
- [ ] Model files placed in the correct folder (`models/`, `masa_api_models/`, `fault_portal_models/`)
- [ ] For MASA/Fault Portal: models split by endpoint file (no unrelated model bundling)
- [ ] Request models serialize API keys correctly (`field_options(alias=...)`, `serialize_by_alias` when needed)
- [ ] Sensitive/private fields are excluded unless strictly required
- [ ] ID/token/date normalization/sanitization logic added where relevant (`__post_init__`)
- [ ] Each new model file includes sanitized HTTP comment examples:
  - [ ] Method
  - [ ] URL
  - [ ] Request (if applicable)
  - [ ] Response
- [ ] Data layer wired in `iec_api/data.py`
- [ ] Client facade wired in `iec_api/iec_client.py`
- [ ] Focused tests added/updated in `tests/`
- [ ] `ruff check` passes
- [ ] Relevant `pytest` tests pass
