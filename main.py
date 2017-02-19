#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def username_valid(username_post):
    if USER_RE.match(username_post):
        return True
    else:
        return False

PASS_RE = re.compile(r"^.{3,20}$")
def password_valid(password_post):
    if PASS_RE.match(password_post):
        return True
    else:
        return False

def verify_valid(password_post, verify_post):
    if password_post == verify_post:
        return True
    else:
        return False

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def email_valid(email_post):
    if EMAIL_RE.match(email_post) or email_post == '':
        return True
    else:
        return False

def build_page(username_entry, password_entry, verify_entry, email_entry, get_or_post):

    username_label = "<label>Username:</label>"
    username_input = "<input name='username' type='text' value='%s'/>"
    username_invalid = "<span class=error type='text' style=color:red>%s</span>"
    username_error = ''
    if get_or_post == 1 and username_valid(username_entry) == False:
        username_error = ' Invalid username - must be between 3-20 characters containing only alphanumeric characters (- and _ allowed)'
    else:
        username_error = ''


    password_label = "<label>Password:</label>"
    password_input = "<input name='password' type='password'/>"
    password_invalid = "<span class=error type='text' style=color:red>%s</span>"
    password_error = ''
    if get_or_post == 1 and password_valid(password_entry) == False:
        password_error = ' Invalid password - must be between 3-20 characters'
    else:
        password_error = ''


    verify_label = "<label>Verify Password:</label>"
    verify_input = "<input name='verify' type='password'/>"
    verify_invalid = "<span class=error type='text' style=color:red>%s</span>"
    verify_error = ''
    if get_or_post == 1 and password_valid(password_entry) == True and password_entry != verify_entry:
        verify_error = ' Passwords entered did not match'
    else:
        verify_error = ''


    email_label = "<label>E-mail (optional):"
    email_input = "<input name='email' value='%s'/>"
    email_invalid = "<span class=error type='text' style=color:red>%s</span>"
    email_error = ''
    if get_or_post == 1 and len(email_entry) > 0 and email_valid(email_entry) == False:
        email_error = ' Invalid e-mail address'
    else:
        email_error = ''


    submit = "<input type='submit'/>"
    form = ("<form method='post'>" +
        ("&nbsp")*11 + username_label + (username_input % username_entry) + (username_invalid % username_error) + ("<br>")*2 +
        ("&nbsp")*12 + password_label + password_input + (password_invalid % password_error) + ("<br>")*2 +
        "&nbsp" + verify_label + verify_input + (verify_invalid % verify_error) + ("<br>")*2 +
        email_label + (email_input % email_entry) + (email_invalid % email_error) + ("<br>")*2 +
        submit + "</form>")
    header = "<h2>User Signup</h2>"

    return header + form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        content = build_page("", "", "", "", 0)
        self.response.write(content)

    def post(self):
        errors_present = False

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if username_valid(username) == True and password_valid(password) == True and verify_valid(password, verify) == True and email_valid(email) == True:
            errors_present = False
        else:
            errors_present = True

        if errors_present == True:
            user_entries = build_page(username, password, verify, email, 1)
            self.response.write(user_entries)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(MainHandler):

    def get(self):
        username = self.request.get("username")
        content = ("<h1>Welcome, %s!</h1>" % username)
        self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
