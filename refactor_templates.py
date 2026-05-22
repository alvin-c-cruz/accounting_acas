#!/usr/bin/env python
"""Script to refactor templates to extend base templates"""
import os
import re

def refactor_report_template(filepath):
    """Refactor a report template to extend base_report.html"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?) - Accounting System</title>', content)
    title = title_match.group(1) if title_match else "Report"

    # Extract the styles block
    styles_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    styles = styles_match.group(1) if styles_match else ""

    # Find the main content (after nav-links div, before </body>)
    # Extract everything between the report-header and the end
    content_match = re.search(r'(<div class="report-header">.*?)</body>', content, re.DOTALL)
    if not content_match:
        print(f"Could not extract content from {filepath}")
        return

    main_content = content_match.group(1).strip()

    # Build new template
    new_template = f"""{{% extends 'base_report.html' %}}

{{% block title %}}{title} - Accounting System{{% endblock %}}

{{% block extra_css %}}
<style>
{styles.strip()}
</style>
{{% endblock %}}

{{% block content %}}
{main_content}
{{% endblock %}}
"""

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_template)

    print(f"[OK] Refactored: {filepath}")

if __name__ == "__main__":
    reports_dir = "reports/templates/reports"

    for filename in ['balance_sheet.html', 'income_statement.html', 'trial_balance.html', 'cash_flow.html']:
        filepath = os.path.join(reports_dir, filename)
        if os.path.exists(filepath):
            refactor_report_template(filepath)
        else:
            print(f"[ERROR] Not found: {filepath}")
