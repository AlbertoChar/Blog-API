# Blog API and Frontend

This project consists of a Flask-based backend API for managing blog posts and a simple frontend to interact with the API. It enables users to perform CRUD (Create, Read, Update, Delete) operations on blog posts.

## Features

- **Create and Read Posts:** Add new blog posts with a title and content, and retrieve a list of existing posts.

- **Update and Delete Posts:** Modify the title and content of existing posts, or remove them altogether.

- **Sorting and Searching:** Sort posts based on title or content in ascending or descending order. Search for posts based on title or content.

## Technologies Used

- **Backend:** Flask, Flask-CORS
- **Frontend:** HTML, CSS, JavaScript
- **Data Storage:** JSON file (`blog_posts.json`)

## Getting Started

### Prerequisites

- Python 3.x
- Flask (`pip install Flask`)
- Flask-CORS (`pip install Flask-CORS`)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/blog-api-frontend.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd blog-api-frontend
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Flask API:**

    ```bash
    python backend.py
    ```

    The API will run on `http://localhost:5002/api`.

2. **Start the frontend:**

    ```bash
    python frontend.py
    ```

    The frontend will be accessible at `http://localhost:5001`.

3. **Open the frontend in your browser and interact with the blog posts.

## API Endpoints

- **GET /api/posts:** Retrieve all blog posts.
- **POST /api/posts:** Add a new blog post.
- **GET /api/posts/add:** (HTML form) Add a new blog post.
- **DELETE /api/posts/<int:id>:** Delete a blog post by ID.
- **PUT /api/posts/<int:id>:** Update a blog post by ID.
- **GET /api/posts/search:** Search for posts based on title or content.