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

username_error_text = ''
password_error_text = ''
verify_error_text = ''
email_error_text = ''

def build_page(username_entry, password_entry, verify_entry, email_entry):
    username_label = "<label>Username:</label>"
    username_input = "<input name='username' type='text' value='%s' required/>"
    username_error = "<span class=error>%s</span>"

    password_label = "<label>Password:</label>"
    password_input = "<input name='password' type='password' required/>"
    password_error = "<span class=error>%s</span>"

    verify_label = "<label>Verify Password:</label>"
    verify_input = "<input name='verify' type='password' required/>"
    verify_error = "<span class=error>%s</span>"

    email_label = "<label>E-mail (optional):"
    email_input = "<input name='email' type='email' value='%s'/>"
    email_error = "<span class=error>%s</span>"

    submit = "<input type='submit'/>"
    form = ("<form method='post'>" +
        ("&nbsp")*11 + username_label + (username_input % username_entry) + (username_error % '') + ("<br>")*2 +
        ("&nbsp")*12 + password_label + password_input + (password_error % password_error_text) + ("<br>")*2 +
        "&nbsp" + verify_label + verify_input + (verify_error % verify_error_text) + ("<br>")*2 +
        email_label + (email_input % email_entry) + (email_error % email_error_text) + ("<br>")*2 +
        submit + "</form>")
    header = "<h2>User Signup</h2>"

    return header + form

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("", "", "", "")
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        user_entries = build_page(username, password, verify, email)
        self.response.write(user_entries)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
