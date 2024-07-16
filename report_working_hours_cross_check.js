// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Report-Working Hours Cross Check"] = {
	"filters": [
		{
			fieldname: "start_date",
			label: __("Start Date"),
			fieldtype: "Date",
			reqd: 1,
		},
		{
			fieldname: "end_date",
			label: __("End Date"),
			fieldtype: "Date",
			reqd: 1,
		},
	]
};
