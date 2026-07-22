# services/pdf_service.py

import pandas as pd
from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

class PDFWithChartsService:
    def __init__(self):
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)
        self.temp_dir = "temp_charts"
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def create_chart_images(self, df, insights):
        """Create chart images for PDF"""
        chart_paths = []
        
        # 1. Department Distribution Chart
        if insights.get('departments'):
            dept_data = pd.DataFrame(list(insights['departments'].items()), columns=['Department', 'Count'])
            fig = px.bar(dept_data, x='Department', y='Count', title="Employees by Department", color='Count', color_continuous_scale='Blues')
            fig.update_layout(height=350, template='plotly_white')
            path = f"{self.temp_dir}/dept_chart.png"
            fig.write_image(path, scale=2)
            chart_paths.append(path)
        
        # 2. Performance Distribution
        perf_data = df['performance_rating'].value_counts().sort_index().reset_index()
        perf_data.columns = ['Rating', 'Count']
        fig = px.bar(perf_data, x='Rating', y='Count', title="Performance Distribution", color='Count', color_continuous_scale='Greens')
        fig.update_layout(height=350, template='plotly_white')
        path = f"{self.temp_dir}/perf_chart.png"
        fig.write_image(path, scale=2)
        chart_paths.append(path)
        
        # 3. Attrition by Department
        if insights.get('attrition_by_dept'):
            att_data = pd.DataFrame(list(insights['attrition_by_dept'].items()), columns=['Department', 'Count'])
            fig = px.bar(att_data, x='Department', y='Count', title="Attrition by Department", color='Count', color_continuous_scale='Reds')
            fig.update_layout(height=350, template='plotly_white')
            path = f"{self.temp_dir}/attrition_chart.png"
            fig.write_image(path, scale=2)
            chart_paths.append(path)
        
        # 4. Gender Distribution
        if insights.get('gender'):
            gender_data = pd.DataFrame(list(insights['gender'].items()), columns=['Gender', 'Count'])
            fig = px.pie(gender_data, values='Count', names='Gender', title="Gender Distribution", hole=0.4)
            fig.update_layout(height=350, template='plotly_white')
            path = f"{self.temp_dir}/gender_chart.png"
            fig.write_image(path, scale=2)
            chart_paths.append(path)
        
        # 5. Salary Distribution
        fig = px.histogram(df, x='monthly_income', title="Salary Distribution", nbins=30, color_discrete_sequence=['#3B82F6'])
        fig.update_layout(height=350, template='plotly_white')
        path = f"{self.temp_dir}/salary_chart.png"
        fig.write_image(path, scale=2)
        chart_paths.append(path)
        
        return chart_paths
    
    def generate_report_with_charts(self, df, insights):
        """Generate PDF report with charts"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/report_with_charts_{timestamp}.pdf"
        
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
        story.append(Paragraph(f"Total Records: {len(df)}", styles['Normal']))
        story.append(Spacer(1, 30))
        
        # KPIs
        story.append(Paragraph("Key Performance Indicators", styles['Heading2']))
        kpi_data = [
            ['Metric', 'Value'],
            ['Total Employees', f"{insights['total_employees']:,}"],
            ['Attrition Count', f"{insights['attrition_count']:,}"],
            ['Attrition Rate', f"{insights['attrition_rate']:.1f}%"],
            ['Retention Rate', f"{100 - insights['attrition_rate']:.1f}%"],
            ['Average Age', f"{insights['avg_age']:.1f} years"],
            ['Average Salary', f"${insights['avg_salary']:,.2f}"],
            ['High Performers', f"{insights['high_performers']}"],
            ['Low Performers', f"{insights['low_performers']}"]
        ]
        kpi_table = Table(kpi_data, colWidths=[2*inch, 2*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A5F')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(kpi_table)
        story.append(PageBreak())
        
        # Charts
        story.append(Paragraph("Dashboard Visualizations", styles['Heading1']))
        story.append(Spacer(1, 20))
        
        # Generate charts
        chart_paths = self.create_chart_images(df, insights)
        
        for i, chart_path in enumerate(chart_paths):
            if os.path.exists(chart_path):
                try:
                    img = Image(chart_path, width=6*inch, height=3.5*inch)
                    story.append(img)
                    story.append(Spacer(1, 15))
                except:
                    pass
        
        # Build PDF
        doc.build(story)
        
        # Clean up temp files
        for path in chart_paths:
            try:
                os.remove(path)
            except:
                pass
        
        return filename