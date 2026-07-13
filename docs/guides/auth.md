# Authentication & Error Handling

Learn how to authenticate your clients and handle exceptions gracefully.

---

## 🔑 Authentication Methods

The SDK supports two ways to authenticate requests:

### 1. API Key Authentication (Recommended)
Pass your API Key generated from the Reactive Resume settings panel. This key is included in the `x-api-key` header of every request:

```python
from reactive_resume import RxResumeClient

client = RxResumeClient(base_url="https://rxresu.me", api_key="rx_api_key_xxx")
```

### 2. Bearer Token (JWT) Authentication
If you are integrating authentication flows (e.g., login with email/password), you can initialize the client using a JWT token:

```python
from reactive_resume import RxResumeClient

client = RxResumeClient(base_url="https://rxresu.me", token="eyJhbGciOi...")
```

---

## 🔒 Session Management (Login Flow)

You can programmatically authenticate using email and password, retrieve the JWT, and dynamically configure the client session:

```python
from reactive_resume import RxResumeClient

# 1. Initialize empty client
client = RxResumeClient(base_url="https://rxresu.me")

# 2. Login programmatically
token, user = client.auth.login(email="user@example.com", password="password123")
print(f"Logged in as: {user.name}")

# 3. Dynamic header updating
client.set_token(token)
```

---

## ⚠️ Error Handling

All HTTP error responses (4xx, 5xx) and connection issues are mapped to custom Python exceptions:

| Exception | HTTP Status Code / Cause | Description |
| :--- | :--- | :--- |
| `ReactiveResumeError` | *Parent Base Exception* | Base class for all SDK errors. |
| `AuthenticationError` | `401`, `403` | Invalid API Key or expired Bearer Token. |
| `NotFoundError` | `404` | Requested resume or resource not found. |
| `ReactiveResumeAPIError`| `400`, `500` etc. | Any other generic API or server error. |
| `ValidationError` | *Client-Side Validation* | Failed Pydantic payload verification. |

### Error Catching Pattern

```python
from reactive_resume import RxResumeClient, AuthenticationError, NotFoundError, ReactiveResumeError

try:
    with RxResumeClient(base_url="https://rxresu.me", api_key="invalid") as client:
        client.resumes.get("resume-id")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except NotFoundError as e:
    print(f"Resume not found: {e}")
except ReactiveResumeError as e:
    print(f"General SDK or Connection failure: {e}")
```
