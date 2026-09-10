# Web_Lab_API

<img width="1803" height="969" alt="image" src="https://github.com/user-attachments/assets/4044f9e6-03b2-4685-ad58-ae989211f661" />
<br/>
Executed successfully with all variables.

<img width="1838" height="965" alt="image" src="https://github.com/user-attachments/assets/8236793e-82dc-48ab-bcdb-610669f8bdd0" />
<br/>
Testing without the location variable still returns a result because a default value of "other" was assigned to it when the function was created.
<br/>

<img width="679" height="648" alt="image" src="https://github.com/user-attachments/assets/15a2fcc2-9c11-42d2-9f06-3e15a74ec0c4" />
<br/>
Testing without the area variable results in a 422 error code because the server did not receive the required data (specifically, the area variable).
<br/>

The relative URL works because the frontend and backend run on the same server 127.0.0.1:8000

# How to use this repo

1. Open your terminal and activate your virtual environment (e.g., `source .venv/bin/activate`(Linux) or `.venv\Scripts\activate`(Windows)).
2. Navigate into the backend directory: `cd backend`
3. Start the server using Uvicorn: `uvicorn main:app --reload`
4. Access the API documentation at: `http://127.0.0.1:8000/docs`
5. Access the interactive web form at: `http://127.0.0.1:8000/static/house_form.html`
