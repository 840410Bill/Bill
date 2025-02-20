# Short URL Service API

## **API 1: Create Short URL**

### **URL**
POST /api/origin_url

### **Description**  
This API accepts an original URL and generates a short URL. The generated short URL will expire after 30 days.

### **Request Example**  

#### **Request Body (JSON)**  
{
    "original_url": "https://example.com"
}

### **Success Response**  

#### **HTTP Status Code**  
200 OK  

#### **Response Format (JSON)**  
{
    "success": true,
    "short_url": "http://127.0.0.1:8000/api/r/shortcode123",
    "expiration_date": "2025-03-22 14:00:00"
}

### **Error Responses**

#### **1. Missing `original_url`**  
- **HTTP Status Code**: 400 Bad Request  
- **Response Format (JSON)**  
{
    "success": false,
    "reason": "Missing 'original_url'"
}

#### **2. `original_url` exceeds 2048 characters**  
- **HTTP Status Code**: 400 Bad Request  
- **Response Format (JSON)**  
{
    "success": false,
    "reason": "'Original_url' is too long."
}

#### **3. Invalid URL format**  
- **HTTP Status Code**: 400 Bad Request  
- **Response Format (JSON)**  
{
    "success": false,
    "reason": "Invalid URL format"
}

#### **Rate Limiting**
- Maximum 5 requests per minute.
- Exceeding the limit will return the following error message:

    **HTTP Status Code**: 429 Too Many Requests  
    **Response Format (JSON)**  
    {
        "detail": "You do not have permission to perform this action."
    }

---

## **API 2: Redirect Using Short URL**

### **URL**  
GET /api/r/{short_url}

### **Description**  
This API allows users to access the "short_url", which will automatically redirect them to the original URL.

### **Success Response**  

#### **HTTP Status Code**  
302 Found (Redirect)  

The user will be redirected to the original URL.

### **Error Responses**

#### **1. Short URL has expired**  
- **HTTP Status Code**: 410 Gone  
- **Response Format (JSON)**  
{
    "success": false,
    "reason": "This short URL has expired."
}


#### **Invalid URL**  
- **HTTP Status Code**: 404 Not Found  
- **Response Format (JSON)**  
{
    "detail": "Not found."
}

---

## **Error Codes & Responses Overview**

| **API Endpoint**                         | **Method** | **Success Response**                                                                                                  | **Error Response**                                             | **HTTP Status Code**          |
|------------------------------------------|------------|-----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|-------------------------------|
| `http://127.0.0.1:8000/api/origin_url`   | POST       | `{"success": true, "short_url": "http://127.0.0.1:8000/api/r/shortcode123", "expiration_date": "2025-03-22 14:00:00"}`| `{"success": false, "reason": "Missing 'original_url'"} `      | 200 OK / 400 Bad Request      |
| `http://127.0.0.1:8000/api/origin_url`   | POST       |                                                                                                                       | `{"success": false, "reason": "'Original_url' is too long."}`  | 400 Bad Request               |
| `http://127.0.0.1:8000/api/origin_url`   | POST       |                                                                                                                       | `{"success": false, "reason": "Invalid URL format"}`           | 400 Bad Request               |
| `http://127.0.0.1:8000/api/r/{short_url}`| GET        | Redirects to the original URL (302 Found)                                                                             | `{"success": false, "reason": "This short URL has expired."}`  | 302 Found / 404 Not Found     |
| `http://127.0.0.1:8000/api/{short_url}`  | GET        |                                                                                                                       | `{"detail": "Not found."}`                                     | 404 Not Found                 |



## **How to Run**

### 1. Clone the GitHub Repository  
```bash
git clone https://github.com/840410Bill/Bill

### 2. In the directory containing the specified docker-compose.yml file, run the following command to build and start the services in detached mode:
docker-compose up --build -d