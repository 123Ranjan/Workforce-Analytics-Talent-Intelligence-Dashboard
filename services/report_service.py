# services/report_service.py

import pandas as pd
from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io

class ReportService:
    def __init__(self):
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_attrition_report(self, insights, filters=None):
        """Generate a PDF report for attrition insights"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/attrition_report_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E3A5F'),
            spaceAfter=30
        )
        story.append(Paragraph("AI Workforce Intelligence Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # KPIs
        story.append(Paragraph("Key Performance Indicators", styles['Heading2']))
        kpi_data = [
            ['Metric', 'Value'],
            ['Total Employees', f"{insights['total_employees']:,}"],
            ['Attrition Count', f"{insights['attrition_count']:,}"],
            ['Attrition Rate', f"{insights['attrition_rate']:.1f}%"],
            ['Retention Rate', f"{100 - insights['attrition_rate']:.1f}%"]
        ]
        kpi_table = Table(kpi_data, colWidths=[2*inch, 2*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A5F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 20))
        
        # Top Departments
        story.append(Paragraph("Top Attrition Departments", styles['Heading2']))
        if insights.get('top_attrition_departments'):
            dept_data = [['Department', 'Attrition Count']]
            for dept, count in insights['top_attrition_departments'].items():
                dept_data.append([dept, str(count)])
            dept_table = Table(dept_data, colWidths=[3*inch, 1.5*inch])
            dept_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC3545')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(dept_table)
        
        story.append(Spacer(1, 20))
        
        # Key Factors
        story.append(Paragraph("Key Factors Comparison", styles['Heading2']))
        factor_data = [['Factor', 'Attrited', 'Non-Attrited']]
        for factor, values in insights['key_factors'].items():
            factor_name = factor.replace('avg_', '').replace('_', ' ').title()
            factor_data.append([
                factor_name,
                f"{values['attrited']:.1f}",
                f"{values['non_attrited']:.1f}"
            ])
        factor_table = Table(factor_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        factor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28A745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(factor_table)
        
        # Recommendations
        story.append(Spacer(1, 20))
        story.append(Paragraph("Recommendations", styles['Heading2']))
        recommendations = [
            "1. Focus retention efforts on departments with highest attrition",
            "2. Review compensation packages for roles with high turnover",
            "3. Improve work-life balance initiatives",
            "4. Implement career development programs",
            "5. Conduct exit interviews to understand root causes"
        ]
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filename
    
    def generate_employee_report(self, df, filters=None):
        """Generate a comprehensive employee report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/employee_report_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E3A5F'),
            spaceAfter=30
        )
        story.append(Paragraph("Employee Data Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}", styles['Normal']))
        story.append(Paragraph(f"Total Employees: {len(df)}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Employee Table
        story.append(Paragraph("Employee Details", styles['Heading2']))
        
        # Prepare data for table
        table_data = [['ID', 'Department', 'Job Role', 'Gender', 'Age', 'Salary', 'Attrition']]
        for _, row in df.head(20).iterrows():
            table_data.append([
                str(row.get('employee_id', '')),
                row.get('department', ''),
                row.get('job_role', ''),
                row.get('gender', ''),
                str(row.get('age', '')),
                f"${row.get('monthly_income', 0):,.0f}",
                row.get('attrition_status', '')
            ])
        
        table = Table(table_data, colWidths=[0.8*inch, 1.2*inch, 1.5*inch, 0.8*inch, 0.6*inch, 1*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A5F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        if len(df) > 20:
            story.append(Paragraph(f"Showing top 20 of {len(df)} employees", styles['Normal']))
        
        doc.build(story)
        return filename