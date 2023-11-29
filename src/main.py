import os

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.realpath(__file__)))
print("Current Working Directory:", os.getcwd())

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import mysql.connector

# Database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="todo_app"
)
db_cursor = db_connection.cursor()

# Create table if not exists
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        status ENUM('open', 'in_progress', 'finished') NOT NULL DEFAULT 'open'
    )
""")
db_connection.commit()

class TodoHandler(http.server.BaseHTTPRequestHandler):
    # ... (existing code)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        if 'task' in params:
            task = params['task'][0]
            db_cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
            db_connection.commit()

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

        # Redirect to the root to show the updated task list

    def render_task_list(self):
        db_cursor.execute("SELECT * FROM todos")
        todos = db_cursor.fetchall()

        # Generate the HTML for the task list
        task_list_html = ""
        for todo in todos:
            task_list_html += f"<tr><th scope='row'>{todo[0]}</th><td>{todo[1]}</td><td>{todo[2]}</td><td class='d-flex'><form class='w-50'><button type='submit' class='btn btn-danger'>Delete</button></form><form class='w-50'><button type='submit' class='btn btn-success ms-1'>Start</button></form></td></tr>"

        return task_list_html

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/index.html', 'rb') as file:
                html_content = file.read()

                # Add the rendered task list to the HTML content
                task_list_html = self.render_task_list()
                html_content = html_content.replace(b'<!-- task_list_placeholder -->', task_list_html.encode('utf-8'))

                self.wfile.write(html_content)
        else:
            self.send_error(404)


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        if 'task' in params:
            task = params['task'][0]
            db_cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
            db_connection.commit()

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

def run(server_class=http.server.HTTPServer, handler_class=TodoHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
