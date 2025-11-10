# Tourism Guide Installation Instructions

## Step 1: Download the Project
1. Visit the GitHub repository: https://github.com/H1n2zo/tourism_guide_fastapi
2. Download the ZIP file of the project
3. Extract zip file to C:\xampp\htdocs\tourism_guide_fastapi 

## Step 2: Setup Database
1. Start XAMPP Control Panel
2. Activate Apache and MySQL services
3. Open your web browser
4. Navigate to http://localhost/phpmyadmin/

## Step 3: Import Database
1. In phpMyAdmin, click on the "Import" tab
2. Choose the `tourism_guide.sql` file
3. Click "Go" to execute the import

*Note: Alternatively, you can open `tourism_guide.sql`, copy its contents and paste into the SQL tab*

## Step 4: Access the Application
1. Open CMD by clicking "ctrl + r" and type cmd.
2. Copy this "cd C:\xampp\htdocs\tourism_guide_fastapi"
3. type python main.py 
4. Open your web browser
5. Navigate to (http://localhost:8000)
6. The tourism guide interface should appear

## Step 5: Setup Administrator and User Access
1. Register a new user account:
   - Click "Login" then "Register"
   - Complete the registration form
2. Set administrator privileges:
   - Go to http://localhost/phpmyadmin/
   - Select the `tourism_guide` database
   - Navigate to the users table
   - Edit your user record
   - Change the role from "user" to "admin"

If welling to help You can push "pikas" branch or create your own
<<<<<<< HEAD
   - Save changes
=======
   - Save changes
>>>>>>> 63e15e215d7bf8e17fefb4a98d0df2b4201b9fc9
