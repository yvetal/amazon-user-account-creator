# amazon-user-creation
This is a selenium-based python script to create users on amazon.com.

## Prerequisites:

### Python Packages:
**Python3 needs to be installed. Use pip install for following packages**
- requests
- openpyxl
- selenium
- deathbycaptcha (https://github.com/codevance/python-deathbycaptcha)

### Other Requirements:

#### Mail Settings: 
- Enable IMAP from all GMAIL accounts: https://mail.google.com/mail/u/0/#settings/fwdandpop
- Allow access for less secure apps: https://myaccount.google.com/lesssecureapps

#### Installations:
- Chromedriver download is required, and it **MUST BE COMPATIBLE** to chrome browser. The path to the same must be assigned to chromedriver_path in main.py. 
Example: chromedriver_path="C:\\software\\chromedriver\\chromedriver.exe"
- Git (default settings is fine)

## Execution:
1. **Ensure the following excel files are present in the credentials_details folder.**
  - **amazon_credentials.xlsx**: The list of username and password for your amazon accounts. You must add the new accounts to be created.
  - **email_credentials.xlsx**: The list of emails which are used for the accounts. You can change this list at any time.
  - **created_accounts.xlsx**: These accounts have already been created by automation.   **Please do not delete or replace this file. It may cause issues with our algorithm.**
2. **Run the main.py file from cmd.** You may double click on the same file, but the logs won't be available in that case.
3. **GIF Captcha** has not yet been handled. If it is encountered, just type the answer in the text box. **Do not press submit** and press enter in the cmd window to continue.

## Algorithm:

1. Read all excel files, determine which accounts need to be created.
2. For each account, try each email address until one succeeds.
3. Create account, pass non gif captcha to deathbycaptcha and await user input on gif captcha. Continue until the step is passed.
4. Poll the configured email for otp and type it in the concerned box.
5. The account should now be created. Navigate to address section and enter the provided dummy address.

## Common issues
1. **Email authentication issue**: This is most likely due to the above prerequisite steps not being performed.

Please inform us regarding any other issues, we will handle them and update here.
