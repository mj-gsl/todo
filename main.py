from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from tenacity import retry, stop_after_delay, wait_fixed
import mysql.connector


app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

# Database connection details
db_config = {
    'user': 'todouser',
    'password': 'Passw0rd',  # Use the actual password you specified during user creation
    'host': 'mysql',
    'database': 'todo_app',  # Replace with the actual database name
    'auth_plugin': 'mysql_native_password',  # Specify the authentication plugin
}

@retry(stop=stop_after_delay(30), wait=wait_fixed(1))
def establish_mysql_connection():
    try:
        # Establish a connection
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        raise

# Wait for the MySQL server to become available
conn = establish_mysql_connection()

# Establish a connection
conn = mysql.connector.connect(**db_config)

# Mount the "static" directory as a static directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Establish a database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Fetch data from the database
    query = "SELECT * FROM todos;"
    cursor.execute(query)
    result = cursor.fetchall()

    # Extract column names
    columns = [desc[0] for desc in cursor.description]

    # Combine column names and rows into a list of dictionaries
    data = [dict(zip(columns, row)) for row in result]

    # Construct the relative path to the template file
    template_path = "index.html"
    return templates.TemplateResponse(template_path, {"request": request, "data": data})

@app.post("/save-task/")
async def save_task(request: Request, task: str = Form(...)):
    try:
        # Update the query to use the correct column names
        query = "INSERT INTO todos (`Todo item`, `Status`) VALUES (%s, 'in process');"

        # Create a buffered cursor
        cursor_insert = conn.cursor(buffered=True)

        # Execute the query with the task_name parameter
        cursor_insert.execute(query, (task,))
        conn.commit()

        # Close the cursor after the query
        cursor_insert.close()
        
        response = RedirectResponse(url="http://localhost:8000/", status_code=302)
        return response

    except Exception as e:
        return {"message": f"Error saving task: {str(e)}"}
    
@app.post("/delete")
async def delete_task(request: Request, No: list = Form(...)):
    try:
        # Update the query to delete the task by task_id
        query = "DELETE FROM todos WHERE No = %s;"

        # Create a buffered cursor
        cursor_delete = conn.cursor(buffered=True)

        # Execute the query with the task_id parameter
        cursor_delete.execute(query, (No))
        conn.commit()
        print(No)
        # Close the cursor after the query
        cursor_delete.close()
        response = RedirectResponse(url="http://localhost:8000/", status_code=302)
        return response
    except Exception as e:
        return {"message": f"Error deleting task: {str(e)}"}
    
@app.post("/update")
async def update_status(request: Request, No: list = Form(...)):
    try:
        query = "UPDATE todos SET Status = 'Task Finished' WHERE No = %s;"
        cursor_update = conn.cursor(buffered=True)
        cursor_update.execute(query, (No))
        conn.commit()
        cursor_update.close
        response = RedirectResponse(url="http://localhost:8000/", status_code=302)
        return response
    except Exception as e:
        return {"message": f"Error updating task: {str(e)}"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)