# Copyright (c) 2025, Zeiad Madboly and contributors
# For license information, please see license.txt

import frappe
import re
import json
from frappe.model.document import Document
from frappe.utils import validate_email_address


class StudentReg(Document):
    def validate(self):
    
        if not self.student_name:
            frappe.throw("Please Enter Your Name")
     
        # can use standard function to validate email address also
        if not self.email:
            frappe.throw("Please Enter Email Address")
        else:
            # Validate email format using regex ( regular expression)
            email_format = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email)
            if not email_format:
                frappe.throw("You Have Entered Invalid Format For Email Address")

        if not self.course_interest:
            frappe.throw("Please Select Your Course of Interest")
        
        if not self.phone_number:
            frappe.throw("Please Enter Phone Number")
        else:
            # Validate phone number format using regex
            # phone_format = re.match(r'^\d{11}$', self.phone_number)
            # if not phone_format:
            #     frappe.throw("You Have Entered Invalid Format For Phone Number")
            if not self.phone_number.isdigit() or len(self.phone_number) < 11:
                frappe.throw("You Have Entered Invalid Format For Phone Number")
    
    
        if not self.expect_start_date:
            frappe.throw("Please Enter Expected Start Date")
   
   
@frappe.whitelist(allow_guest=True)
def list_registrations():
    try:
        data = frappe.get_all(
            "Student Reg",
            fields=["*"]
        )
        return {
            
                'Status Code':200,
                "message": data
                
                }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "List Student Registrations Has Error")
        return {
            "status": "ُError",
            "status_code": 500,
            "message": str(e)
        }
@frappe.whitelist(allow_guest=True)
def submit_registration():
    try:
        # data = frappe.local.form_dict
        data = json.loads(frappe.request.data)

        student_name = data.get("student_name")
        email = data.get("email")
        course_interest = data.get("course_interest")
        phone_number = data.get("phone_number")
        expect_start_date = data.get("expect_start_date")

        if not frappe.utils.validate_email_address(email):
            return {
                "status": "Error",
                "status_code": 400,
                "message": "Invalid email format."
            }

        if not phone_number.isdigit() or len(phone_number) < 8:
            return {
                "status": "Error",
                "status_code": 400,
                "message": "Invalid phone number."
            }

        doc = frappe.get_doc({
            "doctype": "Student Reg",
            "student_name": student_name,
            "email": email,
            "course_interest": course_interest,
            "phone_number": phone_number,
            "expect_start_date": expect_start_date
        })
        doc.insert(ignore_permissions=True)

        return {
            "message": "Registration submitted successfully.",
            "status": "success",
            "data": doc.as_dict()
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Submit Registration Error")
        return {
            "status": "Error",
            "status_code": 500,
            "message": str(e)
        }