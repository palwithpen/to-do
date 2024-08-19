# ToDo App Setup

## Fast API backend Setup

This guide will walk you through setting up a FastAPI backend using a virtual environment.

### Prerequisites

- Python 3.6 or higher installed on your system
- Git (optional, for cloning this repository)   

### Setup Instructions

1. **Clone the Repository** (if you haven't already):

   ```bash
   git clone https://github.com/palwithpen/to-do.git -b master
   cd to-do/backend
   ```

2. **Create virtual environment**
    ``` bash
    python3 -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - On Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies**:
    With the virtual environment activated, install the necessary dependencies:
    ``` bash
    pip install -r requirements.txt
    ```

5. **Run FastAPI Server**:
    Start the FastAPI server by running the following command:
    ```bash
    python3 main.py
    ```


## NextJS Application Setup


### Prerequisites

- Node.js (version 14.x or higher) installed on your system
- npm (comes with Node.js) or Yarn (optional)

### Setup Instructions


1. **Clone the Repository** (if you haven't already):

   ```bash
   git clone https://github.com/palwithpen/to-do.git -b master
   cd to-do/ui
   ```

2. **Install nodejs(if not installed)**

3. **Install dependencies**:
    ```bash
    npm install
    ```

4. **Run NextJS App**:
    ```bash
    npm run dev
    ```

5. **Routes**
    Please follow following routes:
    - /login
    - /todo

