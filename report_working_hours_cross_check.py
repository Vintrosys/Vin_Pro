# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, flt

def execute(filters=None):
    if not filters:
        filters = {}
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
			"label" : "Date",
            "fieldname" : "date",
            "fieldtype" : "Date",
            "width" : 120
		},
        {
			"label" : "Employee ID",
            "fieldname" : "employee_id",
            "fieldtype" : "Data",
            "width" : 150
		},
        {
			"label" : "Employee Name",
            "fieldname" : "employee_name",
            "fieldtype" : "Data",
            "width" : 150
		},
        {
			"label" : "Hours (Checkin)",
            "fieldname" : "hrs_checkin",
            "fieldtype" : "Float",
            "width" : 150
		},
        {
			"label" : "Hours (Timesheet)",
            "fieldname" : "hrs_timesheet",
            "fieldtype" : "Float",
            "width" : 150
		},
        {
			"label" : "Hours (Difference)",
            "fieldname" : "hrs_difference",
            "fieldtype" : "Float",
            "width" : 150
		},
    ]

def get_data(filters):
    from_date = filters.get('start_date')
    to_date = filters.get('end_date')
    #frappe.msgprint(f"from date: {from_date}")
    #frappe.msgprint(f"To date: {to_date}")

    employee_checkins = get_employee_checkins(from_date, to_date)
    employee_timesheets = get_employee_timesheets(from_date, to_date)

    data = []

    for employee_id, checkin_data in employee_checkins.items():
        timesheet_data = employee_timesheets.get(employee_id, {})

        for date, hrs_checkin in checkin_data.items():
            hrs_timesheet = timesheet_data.get(date, 0)
            hrs_difference = hrs_checkin - hrs_timesheet

            data.append({
                "date": date,
                "employee_id": employee_id,
                "employee_name": frappe.get_value("Employee", employee_id, "employee_name"),
                "hrs_checkin": hrs_checkin,
                "hrs_timesheet": hrs_timesheet,
                "hrs_difference": hrs_difference
            })
    #frappe.msgprint(f"Data: {data}")
    return data
def get_employee_checkins(from_date, to_date):  
    checkins = frappe.db.sql("""
        SELECT
            employee,
            DATE(time) as date,
            TIMESTAMPDIFF(HOUR, MIN(time), MAX(time)) as hrs
        FROM `tabEmployee Checkin`
        WHERE DATE(time) BETWEEN %s AND %s
        GROUP BY employee, DATE(time)
    """, (from_date, to_date), as_dict=1)
    
    employee_checkins = {}
    for checkin in checkins:
        if checkin.employee not in employee_checkins:
            employee_checkins[checkin.employee] = {}
        employee_checkins[checkin.employee][checkin.date] = flt(checkin.hrs)
    #frappe.msgprint(f"employee checkins {employee_checkins}")
    return employee_checkins

def get_employee_timesheets(from_date, to_date):
    timesheets = frappe.db.sql("""
        SELECT
            t.employee,
            DATE(td.from_time) as date,
            SUM(td.hours) as hrs
        FROM `tabTimesheet Detail` td
        JOIN `tabTimesheet` t ON t.name = td.parent
        WHERE DATE(td.from_time) BETWEEN %s AND %s
        GROUP BY t.employee, DATE(td.from_time)
    """, (from_date, to_date), as_dict=1)
    
    employee_timesheets = {}
    for timesheet in timesheets:
        if timesheet.employee not in employee_timesheets:
            employee_timesheets[timesheet.employee] = {}
        employee_timesheets[timesheet.employee][timesheet.date] = flt(timesheet.hrs)
    #frappe.msgprint(f"employee timesheet {employee_timesheets}")
    
    return employee_timesheets
    
